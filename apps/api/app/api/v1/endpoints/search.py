"""
Search endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import List

from app.db.session import get_db
from app.db import models, schemas

router = APIRouter()

@router.get("/", response_model=schemas.FoodSearchResult)
async def search_foods(
    q: str = Query(..., description="Search query", min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Search foods by name using full-text search
    """
    # Build search query - case-insensitive LIKE search
    search_term = f"%{q}%"

    # Count total matches
    count_query = select(func.count()).select_from(models.Food).where(
        or_(
            models.Food.name.ilike(search_term),
            func.array_to_string(models.Food.common_names, ',').ilike(search_term)
        )
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    # Get paginated results
    query = select(models.Food).where(
        or_(
            models.Food.name.ilike(search_term),
            func.array_to_string(models.Food.common_names, ',').ilike(search_term)
        )
    ).offset(offset).limit(limit)

    result = await db.execute(query)
    foods = result.scalars().all()

    return schemas.FoodSearchResult(
        total=total,
        foods=foods
    )
