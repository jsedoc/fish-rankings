"""
API v1 router - aggregates all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1.endpoints import foods, search, categories, recalls, barcode
from app.api.v1.endpoints import foods, search, categories, sources, research

api_router = APIRouter()

api_router.include_router(foods.router, prefix="/foods", tags=["foods"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(recalls.router, prefix="/recalls", tags=["recalls"])
api_router.include_router(barcode.router, prefix="/barcode", tags=["barcode"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(research.router, prefix="/research", tags=["research"])
