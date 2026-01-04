"""
Research endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.db import models, schemas

router = APIRouter()

@router.get("", response_model=List[schemas.ResearchPaper])
async def list_research_papers(
    db: AsyncSession = Depends(get_db)
):
    """
    List all research papers
    """
    query = select(models.ResearchPaper).order_by(models.ResearchPaper.publication_date.desc())
    result = await db.execute(query)
    papers = result.scalars().all()
    
    return papers
