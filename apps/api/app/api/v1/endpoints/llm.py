"""
LLM-powered natural language query endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db import schemas
from app.services.llm_service import llm_service
from app.core.deps import get_current_user_optional
from app.db import models

router = APIRouter()


@router.post("/query", response_model=schemas.NaturalLanguageResponse)
async def natural_language_query(
    query: schemas.NaturalLanguageQuery,
    db: AsyncSession = Depends(get_db),
    current_user: models.User | None = Depends(get_current_user_optional)
):
    """
    Ask a natural language question about food safety, nutrition, recalls, or advisories

    This endpoint uses AI to understand your question and search the database for relevant information.

    **Examples:**
    - "Is tuna safe to eat during pregnancy?"
    - "What are the mercury levels in salmon?"
    - "Are there any recalls for romaine lettuce?"
    - "Which fish are most sustainable?"
    - "What foods should I avoid if I'm concerned about pesticides?"

    **Parameters:**
    - **query**: Your natural language question
    - **context**: Optional context hint (food, advisory, sustainability, recall)

    **Returns:**
    - **answer**: AI-generated answer based on database information
    - **sources**: Relevant foods from the database
    - **recalls**: Relevant recalls
    - **advisories**: Relevant state advisories

    **Note:** This endpoint works without authentication, but may have rate limits for anonymous users.
    """
    if not query.query or len(query.query.strip()) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query must be at least 3 characters long"
        )

    # Process query with LLM service
    result = await llm_service.process_food_query(
        query=query.query,
        db=db,
        context=query.context
    )

    return result


@router.get("/examples")
async def get_query_examples():
    """
    Get example queries to help users understand what they can ask

    Returns a list of example questions with their categories.
    """
    return {
        "examples": [
            {
                "category": "Safety & Contaminants",
                "queries": [
                    "What fish have the lowest mercury levels?",
                    "Is it safe to eat tuna during pregnancy?",
                    "Which vegetables have the most pesticide residue?",
                    "What are the health effects of methylmercury?"
                ]
            },
            {
                "category": "Recalls",
                "queries": [
                    "Are there any recalls for chicken?",
                    "What products were recalled for salmonella?",
                    "Show me critical food recalls this month",
                    "Has romaine lettuce been recalled recently?"
                ]
            },
            {
                "category": "Sustainability",
                "queries": [
                    "Which seafood is most sustainable?",
                    "What fish should I avoid for environmental reasons?",
                    "Is farmed salmon sustainable?",
                    "What are the most overfished species?"
                ]
            },
            {
                "category": "State Advisories",
                "queries": [
                    "Are there fish advisories in California?",
                    "What fish are safe to eat from Florida waters?",
                    "Which states have mercury warnings for bass?",
                    "Can I eat fish from Lake Michigan?"
                ]
            },
            {
                "category": "Nutrition",
                "queries": [
                    "What are the health benefits of salmon?",
                    "Which foods are high in omega-3?",
                    "What's the nutritional value of kale?",
                    "Compare nutrition between wild and farmed fish"
                ]
            }
        ],
        "tips": [
            "Be specific about what you want to know",
            "Mention specific foods, contaminants, or locations",
            "Ask about safety, nutrition, recalls, or sustainability",
            "The AI will search the database and provide evidence-based answers"
        ]
    }
