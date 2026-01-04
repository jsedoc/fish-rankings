"""
API endpoints for food recalls
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.db.session import get_db
from app.db.models import FoodRecall
from app.schemas.recalls import RecallResponse, RecallListResponse, RecallCreate
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=RecallListResponse)
async def get_recalls(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    classification: Optional[str] = Query(None, description="Filter by classification (Class I, II, or III)"),
    state: Optional[str] = Query(None, description="Filter by state code"),
    status: Optional[str] = Query(None, description="Filter by status"),
    days: Optional[int] = Query(None, ge=1, le=365, description="Recalls from last N days"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of food recalls

    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **classification**: Filter by FDA classification (Class I, II, or III)
    - **state**: Filter by US state code (e.g., 'CA', 'NY')
    - **status**: Filter by recall status
    - **days**: Only show recalls from last N days
    """
    try:
        # Build query
        query = select(FoodRecall).order_by(desc(FoodRecall.recall_date))

        # Apply filters
        if classification:
            query = query.where(FoodRecall.classification == classification)

        if state:
            query = query.where(FoodRecall.state == state.upper())

        if status:
            query = query.where(FoodRecall.status == status)

        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            query = query.where(FoodRecall.recall_date >= cutoff_date)

        # Get total count
        count_query = select(FoodRecall).where(*query.whereclause.clauses if hasattr(query.whereclause, 'clauses') else [])
        total_result = await db.execute(count_query)
        total = len(total_result.scalars().all())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(query)
        recalls = result.scalars().all()

        return {
            "recalls": recalls,
            "total": total,
            "skip": skip,
            "limit": limit
        }

    except Exception as e:
        logger.error(f"Error fetching recalls: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent", response_model=List[RecallResponse])
async def get_recent_recalls(
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get recent recalls from the last N days

    - **days**: Number of days to look back (default: 30)
    - **limit**: Maximum number of recalls to return
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)

        query = (
            select(FoodRecall)
            .where(FoodRecall.recall_date >= cutoff_date)
            .order_by(desc(FoodRecall.recall_date))
            .limit(limit)
        )

        result = await db.execute(query)
        recalls = result.scalars().all()

        return recalls

    except Exception as e:
        logger.error(f"Error fetching recent recalls: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/critical", response_model=List[RecallResponse])
async def get_critical_recalls(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get Class I (critical) recalls

    Class I: Dangerous or defective products that could cause serious health problems or death
    """
    try:
        query = (
            select(FoodRecall)
            .where(FoodRecall.classification == "Class I")
            .order_by(desc(FoodRecall.recall_date))
            .limit(limit)
        )

        result = await db.execute(query)
        recalls = result.scalars().all()

        return recalls

    except Exception as e:
        logger.error(f"Error fetching critical recalls: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=List[RecallResponse])
async def search_recalls(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Search recalls by product name or company

    - **q**: Search query (minimum 2 characters)
    - **limit**: Maximum number of results
    """
    try:
        search_term = f"%{q}%"

        query = (
            select(FoodRecall)
            .where(
                or_(
                    FoodRecall.product_description.ilike(search_term),
                    FoodRecall.company_name.ilike(search_term),
                    FoodRecall.reason_for_recall.ilike(search_term)
                )
            )
            .order_by(desc(FoodRecall.recall_date))
            .limit(limit)
        )

        result = await db.execute(query)
        recalls = result.scalars().all()

        return recalls

    except Exception as e:
        logger.error(f"Error searching recalls: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{recall_number}", response_model=RecallResponse)
async def get_recall(
    recall_number: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific recall by recall number

    - **recall_number**: FDA recall number (e.g., "F-0000-2024")
    """
    try:
        query = select(FoodRecall).where(FoodRecall.recall_number == recall_number)
        result = await db.execute(query)
        recall = result.scalar_one_or_none()

        if not recall:
            raise HTTPException(status_code=404, detail=f"Recall {recall_number} not found")

        return recall

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching recall {recall_number}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def get_recall_stats(
    days: int = Query(90, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """
    Get recall statistics for the last N days

    - **days**: Number of days to analyze
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)

        # Get all recalls in time period
        query = select(FoodRecall).where(FoodRecall.recall_date >= cutoff_date)
        result = await db.execute(query)
        recalls = result.scalars().all()

        # Calculate statistics
        total_recalls = len(recalls)

        classification_counts = {
            "Class I": 0,
            "Class II": 0,
            "Class III": 0
        }

        status_counts = {}
        state_counts = {}

        for recall in recalls:
            # Count by classification
            if recall.classification in classification_counts:
                classification_counts[recall.classification] += 1

            # Count by status
            status = recall.status or "Unknown"
            status_counts[status] = status_counts.get(status, 0) + 1

            # Count by state
            if recall.state:
                state_counts[recall.state] = state_counts.get(recall.state, 0) + 1

        # Top states
        top_states = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "period_days": days,
            "total_recalls": total_recalls,
            "by_classification": classification_counts,
            "by_status": status_counts,
            "top_states": dict(top_states),
            "critical_recalls": classification_counts["Class I"]
        }

    except Exception as e:
        logger.error(f"Error calculating recall stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
