"""
Source endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.db import models, schemas

router = APIRouter()

@router.get("", response_model=List[schemas.Source])
async def list_sources(
    db: AsyncSession = Depends(get_db)
):
    """
    List all data sources
    """
    query = select(models.Source)
    result = await db.execute(query)
    sources = result.scalars().all()
    
    return sources
