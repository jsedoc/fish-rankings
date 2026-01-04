"""
LLM Service for natural language queries using Anthropic Claude
"""
from typing import List, Optional
import anthropic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.core.config import settings
from app.db import models


class LLMService:
    """Service for processing natural language queries about food safety"""

    def __init__(self):
        self.client = None
        if settings.ANTHROPIC_API_KEY:
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def process_food_query(
        self,
        query: str,
        db: AsyncSession,
        context: Optional[str] = None
    ) -> dict:
        """
        Process a natural language query about foods, safety, and nutrition

        Args:
            query: User's natural language question
            db: Database session
            context: Optional context (food, advisory, sustainability, etc.)

        Returns:
            Dictionary with answer, relevant foods, recalls, and advisories
        """
        if not self.client:
            return {
                "answer": "LLM service is not configured. Please set ANTHROPIC_API_KEY in your environment.",
                "sources": [],
                "recalls": [],
                "advisories": []
            }

        # Extract keywords from query for database search
        keywords = self._extract_keywords(query)

        # Search database for relevant foods
        foods = await self._search_foods(keywords, db)
        recalls = await self._search_recalls(keywords, db)
        advisories = await self._search_advisories(keywords, db)

        # Build context for LLM
        food_context = self._build_food_context(foods, recalls, advisories)

        # Create prompt for Claude
        system_prompt = """You are a food safety expert assistant. You help users understand food safety,
nutrition, contaminants, recalls, and sustainability. Provide accurate, helpful information based on
the database context provided. If the database doesn't have relevant information, say so clearly.

Format your response as a clear, helpful answer. Be concise but thorough."""

        user_prompt = f"""User question: {query}

Available database information:
{food_context}

Please provide a helpful answer based on this information. If asking about specific foods, mention
any relevant safety concerns, recalls, or advisories. Be specific and cite the data when possible."""

        # Get response from Claude
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            answer = message.content[0].text

            return {
                "answer": answer,
                "sources": foods[:5],  # Return top 5 relevant foods
                "recalls": recalls[:5],  # Return top 5 relevant recalls
                "advisories": advisories[:5]  # Return top 5 relevant advisories
            }

        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": foods[:5],
                "recalls": recalls[:5],
                "advisories": advisories[:5]
            }

    def _extract_keywords(self, query: str) -> List[str]:
        """Extract potential keywords from the query"""
        # Simple keyword extraction - split on common words
        stop_words = {
            'is', 'are', 'what', 'which', 'how', 'when', 'where', 'who',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'about', 'safe', 'eat',
            'food', 'should', 'can', 'i', 'my', 'me', 'tell'
        }

        words = query.lower().split()
        keywords = [w.strip('?,!.') for w in words if w.lower() not in stop_words and len(w) > 2]

        return keywords[:10]  # Return max 10 keywords

    async def _search_foods(self, keywords: List[str], db: AsyncSession) -> List[models.Food]:
        """Search for foods matching keywords"""
        if not keywords:
            return []

        # Build query with OR conditions for each keyword
        conditions = []
        for keyword in keywords:
            conditions.append(models.Food.name.ilike(f"%{keyword}%"))
            conditions.append(models.Food.description.ilike(f"%{keyword}%"))

        result = await db.execute(
            select(models.Food)
            .where(or_(*conditions))
            .limit(10)
        )

        return list(result.scalars().all())

    async def _search_recalls(self, keywords: List[str], db: AsyncSession) -> List[dict]:
        """Search for recalls matching keywords"""
        if not keywords:
            return []

        conditions = []
        for keyword in keywords:
            conditions.append(models.FoodRecall.product_description.ilike(f"%{keyword}%"))
            conditions.append(models.FoodRecall.reason_for_recall.ilike(f"%{keyword}%"))

        result = await db.execute(
            select(models.FoodRecall)
            .where(or_(*conditions))
            .limit(10)
        )

        recalls = result.scalars().all()

        return [
            {
                "recall_number": r.recall_number,
                "product": r.product_description[:200],
                "reason": r.reason_for_recall[:200] if r.reason_for_recall else None,
                "classification": r.classification,
                "company": r.company_name
            }
            for r in recalls
        ]

    async def _search_advisories(self, keywords: List[str], db: AsyncSession) -> List[dict]:
        """Search for state advisories matching keywords"""
        if not keywords:
            return []

        conditions = []
        for keyword in keywords:
            conditions.append(models.StateAdvisory.fish_species.ilike(f"%{keyword}%"))
            conditions.append(models.StateAdvisory.waterbody_name.ilike(f"%{keyword}%"))
            conditions.append(models.StateAdvisory.advisory_text.ilike(f"%{keyword}%"))

        result = await db.execute(
            select(models.StateAdvisory)
            .where(or_(*conditions))
            .limit(10)
        )

        advisories = result.scalars().all()

        return [
            {
                "state": a.state_name,
                "fish_species": a.fish_species,
                "waterbody": a.waterbody_name,
                "contaminant": a.contaminant_type,
                "advisory_level": a.advisory_level,
                "consumption_limit": a.consumption_limit
            }
            for a in advisories
        ]

    def _build_food_context(
        self,
        foods: List[models.Food],
        recalls: List[dict],
        advisories: List[dict]
    ) -> str:
        """Build context string from database results"""
        context_parts = []

        if foods:
            food_info = "\n".join([
                f"- {f.name}: {f.description[:200] if f.description else 'No description'}"
                for f in foods
            ])
            context_parts.append(f"Relevant Foods:\n{food_info}")

        if recalls:
            recall_info = "\n".join([
                f"- {r['product']} (Class {r['classification']}): {r['reason']}"
                for r in recalls
            ])
            context_parts.append(f"\nRecent Recalls:\n{recall_info}")

        if advisories:
            advisory_info = "\n".join([
                f"- {a['state']} - {a['fish_species']}: {a['advisory_level']} ({a['consumption_limit']})"
                for a in advisories
            ])
            context_parts.append(f"\nState Advisories:\n{advisory_info}")

        if not context_parts:
            return "No relevant data found in database."

        return "\n\n".join(context_parts)


# Global service instance
llm_service = LLMService()
