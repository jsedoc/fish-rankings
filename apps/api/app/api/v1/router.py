"""
API v1 router - aggregates all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    foods, search, categories, recalls, barcode,
    sources, research, auth, saved_foods, meal_plans, llm
)

api_router = APIRouter()

# Core endpoints
api_router.include_router(foods.router, prefix="/foods", tags=["foods"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(research.router, prefix="/research", tags=["research"])

# Milestone 2 endpoints
api_router.include_router(recalls.router, prefix="/recalls", tags=["recalls"])
api_router.include_router(barcode.router, prefix="/barcode", tags=["barcode"])

# Issue #25 - New user features
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(saved_foods.router, prefix="/saved-foods", tags=["saved-foods"])
api_router.include_router(meal_plans.router, prefix="/meal-plans", tags=["meal-plans"])
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
