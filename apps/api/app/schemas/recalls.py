"""
Pydantic schemas for food recalls
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class RecallBase(BaseModel):
    """Base schema for food recalls"""
    recall_number: str
    product_description: str
    reason_for_recall: Optional[str] = None
    recall_date: Optional[datetime] = None
    report_date: Optional[datetime] = None
    company_name: Optional[str] = None
    distribution_pattern: Optional[str] = None
    product_quantity: Optional[str] = None
    status: Optional[str] = None
    classification: Optional[str] = None
    code_info: Optional[str] = None
    voluntary_mandated: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    event_id: Optional[str] = None


class RecallCreate(RecallBase):
    """Schema for creating a recall"""
    food_id: Optional[UUID] = None


class RecallResponse(RecallBase):
    """Schema for recall response"""
    id: UUID
    food_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Computed fields
    @property
    def severity(self) -> str:
        """Get severity based on classification"""
        severity_map = {
            "Class I": "critical",
            "Class II": "high",
            "Class III": "moderate"
        }
        return severity_map.get(self.classification, "unknown")

    @property
    def severity_color(self) -> str:
        """Get color for UI"""
        color_map = {
            "Class I": "red",
            "Class II": "orange",
            "Class III": "yellow"
        }
        return color_map.get(self.classification, "gray")

    class Config:
        from_attributes = True


class RecallListResponse(BaseModel):
    """Schema for paginated recall list"""
    recalls: List[RecallResponse]
    total: int
    skip: int
    limit: int
