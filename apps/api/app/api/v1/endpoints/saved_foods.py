"""
Saved Foods endpoints - save, list, and manage user's saved foods
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db import models, schemas
from app.core.deps import get_current_active_user

router = APIRouter()


@router.post("", response_model=schemas.SavedFood, status_code=status.HTTP_201_CREATED)
async def save_food(
    saved_food_in: schemas.SavedFoodCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Save a food to user's saved foods list

    - **food_id**: ID of the food to save
    - **notes**: Optional notes about this saved food
    """
    # Check if food exists
    result = await db.execute(
        select(models.Food).where(models.Food.id == saved_food_in.food_id)
    )
    food = result.scalar_one_or_none()

    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )

    # Check if already saved
    result = await db.execute(
        select(models.SavedFood).where(
            models.SavedFood.user_id == current_user.id,
            models.SavedFood.food_id == saved_food_in.food_id
        )
    )
    existing_saved = result.scalar_one_or_none()

    if existing_saved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food already saved"
        )

    # Create saved food
    db_saved_food = models.SavedFood(
        user_id=current_user.id,
        food_id=saved_food_in.food_id,
        notes=saved_food_in.notes
    )

    db.add(db_saved_food)
    await db.commit()
    await db.refresh(db_saved_food)

    # Load the food relationship
    result = await db.execute(
        select(models.SavedFood)
        .options(selectinload(models.SavedFood.food))
        .where(models.SavedFood.id == db_saved_food.id)
    )
    db_saved_food = result.scalar_one()

    return db_saved_food


@router.get("", response_model=List[schemas.SavedFood])
async def list_saved_foods(
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all saved foods for the current user
    """
    result = await db.execute(
        select(models.SavedFood)
        .options(selectinload(models.SavedFood.food))
        .where(models.SavedFood.user_id == current_user.id)
        .order_by(models.SavedFood.saved_at.desc())
    )
    saved_foods = result.scalars().all()

    return saved_foods


@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unsave_food(
    food_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a food from saved foods list

    - **food_id**: ID of the food to unsave
    """
    # Find saved food
    result = await db.execute(
        select(models.SavedFood).where(
            models.SavedFood.user_id == current_user.id,
            models.SavedFood.food_id == food_id
        )
    )
    saved_food = result.scalar_one_or_none()

    if not saved_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved food not found"
        )

    await db.delete(saved_food)
    await db.commit()

    return None


@router.put("/{food_id}", response_model=schemas.SavedFood)
async def update_saved_food_notes(
    food_id: UUID,
    notes: str,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update notes for a saved food

    - **food_id**: ID of the saved food
    - **notes**: New notes
    """
    # Find saved food
    result = await db.execute(
        select(models.SavedFood).where(
            models.SavedFood.user_id == current_user.id,
            models.SavedFood.food_id == food_id
        )
    )
    saved_food = result.scalar_one_or_none()

    if not saved_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved food not found"
        )

    saved_food.notes = notes
    await db.commit()
    await db.refresh(saved_food)

    # Load the food relationship
    result = await db.execute(
        select(models.SavedFood)
        .options(selectinload(models.SavedFood.food))
        .where(models.SavedFood.id == saved_food.id)
    )
    saved_food = result.scalar_one()

    return saved_food
