"""
Meal Planning endpoints - create, manage, and track meal plans
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.db import models, schemas
from app.core.deps import get_current_active_user

router = APIRouter()


@router.post("", response_model=schemas.MealPlan, status_code=status.HTTP_201_CREATED)
async def create_meal_plan(
    meal_plan_in: schemas.MealPlanCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new meal plan

    - **name**: Name of the meal plan
    - **description**: Optional description
    - **date**: Planned date for the meal
    - **meal_type**: Type of meal (breakfast, lunch, dinner, snack)
    """
    db_meal_plan = models.MealPlan(
        user_id=current_user.id,
        name=meal_plan_in.name,
        description=meal_plan_in.description,
        date=meal_plan_in.date,
        meal_type=meal_plan_in.meal_type
    )

    db.add(db_meal_plan)
    await db.commit()
    await db.refresh(db_meal_plan)

    return db_meal_plan


@router.get("", response_model=List[schemas.MealPlan])
async def list_meal_plans(
    meal_type: str | None = Query(None, description="Filter by meal type"),
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all meal plans for the current user

    - **meal_type**: Optional filter by meal type
    """
    query = (
        select(models.MealPlan)
        .options(
            selectinload(models.MealPlan.foods).selectinload(models.MealPlanFood.food)
        )
        .where(models.MealPlan.user_id == current_user.id)
    )

    if meal_type:
        query = query.where(models.MealPlan.meal_type == meal_type)

    query = query.order_by(models.MealPlan.date.desc().nulls_last(), models.MealPlan.created_at.desc())

    result = await db.execute(query)
    meal_plans = result.scalars().all()

    return meal_plans


@router.get("/{meal_plan_id}", response_model=schemas.MealPlan)
async def get_meal_plan(
    meal_plan_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific meal plan by ID

    - **meal_plan_id**: ID of the meal plan
    """
    result = await db.execute(
        select(models.MealPlan)
        .options(
            selectinload(models.MealPlan.foods).selectinload(models.MealPlanFood.food)
        )
        .where(
            models.MealPlan.id == meal_plan_id,
            models.MealPlan.user_id == current_user.id
        )
    )
    meal_plan = result.scalar_one_or_none()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    return meal_plan


@router.put("/{meal_plan_id}", response_model=schemas.MealPlan)
async def update_meal_plan(
    meal_plan_id: UUID,
    meal_plan_update: schemas.MealPlanUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a meal plan

    - **meal_plan_id**: ID of the meal plan
    - **name**: New name (optional)
    - **description**: New description (optional)
    - **date**: New date (optional)
    - **meal_type**: New meal type (optional)
    """
    result = await db.execute(
        select(models.MealPlan).where(
            models.MealPlan.id == meal_plan_id,
            models.MealPlan.user_id == current_user.id
        )
    )
    meal_plan = result.scalar_one_or_none()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    # Update fields
    if meal_plan_update.name is not None:
        meal_plan.name = meal_plan_update.name
    if meal_plan_update.description is not None:
        meal_plan.description = meal_plan_update.description
    if meal_plan_update.date is not None:
        meal_plan.date = meal_plan_update.date
    if meal_plan_update.meal_type is not None:
        meal_plan.meal_type = meal_plan_update.meal_type

    await db.commit()
    await db.refresh(meal_plan)

    # Load foods
    result = await db.execute(
        select(models.MealPlan)
        .options(
            selectinload(models.MealPlan.foods).selectinload(models.MealPlanFood.food)
        )
        .where(models.MealPlan.id == meal_plan_id)
    )
    meal_plan = result.scalar_one()

    return meal_plan


@router.delete("/{meal_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal_plan(
    meal_plan_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a meal plan

    - **meal_plan_id**: ID of the meal plan to delete
    """
    result = await db.execute(
        select(models.MealPlan).where(
            models.MealPlan.id == meal_plan_id,
            models.MealPlan.user_id == current_user.id
        )
    )
    meal_plan = result.scalar_one_or_none()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    await db.delete(meal_plan)
    await db.commit()

    return None


# ==================
# Meal Plan Foods
# ==================

@router.post("/{meal_plan_id}/foods", response_model=schemas.MealPlanFoodInPlan, status_code=status.HTTP_201_CREATED)
async def add_food_to_meal_plan(
    meal_plan_id: UUID,
    food_in: schemas.MealPlanFoodCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a food to a meal plan

    - **meal_plan_id**: ID of the meal plan
    - **food_id**: ID of the food to add
    - **serving_size**: Serving size (e.g., "100g", "1 cup")
    - **servings**: Number of servings
    - **notes**: Optional notes
    """
    # Check if meal plan exists and belongs to user
    result = await db.execute(
        select(models.MealPlan).where(
            models.MealPlan.id == meal_plan_id,
            models.MealPlan.user_id == current_user.id
        )
    )
    meal_plan = result.scalar_one_or_none()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    # Check if food exists
    result = await db.execute(
        select(models.Food).where(models.Food.id == food_in.food_id)
    )
    food = result.scalar_one_or_none()

    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )

    # Add food to meal plan
    db_meal_plan_food = models.MealPlanFood(
        meal_plan_id=meal_plan_id,
        food_id=food_in.food_id,
        serving_size=food_in.serving_size,
        servings=food_in.servings,
        notes=food_in.notes
    )

    db.add(db_meal_plan_food)
    await db.commit()
    await db.refresh(db_meal_plan_food)

    # Load the food relationship
    result = await db.execute(
        select(models.MealPlanFood)
        .options(selectinload(models.MealPlanFood.food))
        .where(models.MealPlanFood.id == db_meal_plan_food.id)
    )
    db_meal_plan_food = result.scalar_one()

    return db_meal_plan_food


@router.delete("/{meal_plan_id}/foods/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_food_from_meal_plan(
    meal_plan_id: UUID,
    food_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a food from a meal plan

    - **meal_plan_id**: ID of the meal plan
    - **food_id**: ID of the food to remove
    """
    # Check if meal plan exists and belongs to user
    result = await db.execute(
        select(models.MealPlan).where(
            models.MealPlan.id == meal_plan_id,
            models.MealPlan.user_id == current_user.id
        )
    )
    meal_plan = result.scalar_one_or_none()

    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )

    # Find the meal plan food
    result = await db.execute(
        select(models.MealPlanFood).where(
            models.MealPlanFood.meal_plan_id == meal_plan_id,
            models.MealPlanFood.food_id == food_id
        )
    )
    meal_plan_food = result.scalar_one_or_none()

    if not meal_plan_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found in meal plan"
        )

    await db.delete(meal_plan_food)
    await db.commit()

    return None
