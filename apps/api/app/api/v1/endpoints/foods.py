"""
Food endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.db import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Food])
async def list_foods(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all foods with optional filtering
    """
    query = select(models.Food).options(joinedload(models.Food.category))

    if category:
        # Join with category and filter
        query = query.join(models.FoodCategory).where(models.FoodCategory.slug == category)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    foods = result.unique().scalars().all()

    return foods


@router.get("/{food_id}", response_model=schemas.FoodDetail)
async def get_food(
    food_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about a specific food
    """
    query = select(models.Food).where(models.Food.id == food_id).options(
        joinedload(models.Food.category),
        joinedload(models.Food.contaminant_levels).joinedload(models.FoodContaminantLevel.contaminant),
        joinedload(models.Food.contaminant_levels).joinedload(models.FoodContaminantLevel.source),
        joinedload(models.Food.nutrients).joinedload(models.FoodNutrient.source)
    )
    result = await db.execute(query)
    food = result.unique().scalar_one_or_none()

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    return food


@router.get("/slug/{slug}", response_model=schemas.FoodDetail)
async def get_food_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get food by slug (URL-friendly identifier)
    """
    query = select(models.Food).where(models.Food.slug == slug).options(
        joinedload(models.Food.category),
        joinedload(models.Food.contaminant_levels).joinedload(models.FoodContaminantLevel.contaminant),
        joinedload(models.Food.contaminant_levels).joinedload(models.FoodContaminantLevel.source),
        joinedload(models.Food.nutrients).joinedload(models.FoodNutrient.source)
    )
    result = await db.execute(query)
    food = result.unique().scalar_one_or_none()

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    return food


@router.get("/barcode/{barcode}", response_model=schemas.FoodDetail)
async def get_food_by_barcode(
    barcode: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Look up food by barcode (UPC/EAN)
    """
    query = select(models.Food).where(models.Food.barcode == barcode).options(
        joinedload(models.Food.category),
        joinedload(models.Food.contaminant_levels).joinedload(models.FoodContaminantLevel.contaminant),
        joinedload(models.Food.contaminant_levels).joinedload(models.FoodContaminantLevel.source),
        joinedload(models.Food.nutrients).joinedload(models.FoodNutrient.source)
    )
    result = await db.execute(query)
    food = result.unique().scalar_one_or_none()

    if not food:
        raise HTTPException(status_code=404, detail="Food not found for this barcode")

    return food
