"""
Category endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.db import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.FoodCategory])
async def list_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    List all food categories
    """
    query = select(models.FoodCategory).where(models.FoodCategory.parent_id == None)
    result = await db.execute(query)
    categories = result.scalars().all()

    return categories


@router.get("/{slug}", response_model=schemas.FoodCategory)
async def get_category(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get category by slug
    """
    query = select(models.FoodCategory).where(models.FoodCategory.slug == slug)
    result = await db.execute(query)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category
