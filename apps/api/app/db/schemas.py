"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from uuid import UUID


# Food Category Schemas
class FoodCategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class FoodCategoryCreate(FoodCategoryBase):
    parent_id: Optional[int] = None

class FoodCategory(FoodCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: Optional[int] = None


# Contaminant Schemas
class ContaminantBase(BaseModel):
    name: str
    chemical_name: Optional[str] = None
    description: Optional[str] = None
    health_effects: Optional[str] = None
    unit: Optional[str] = None

class Contaminant(ContaminantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    acceptable_daily_intake: Optional[float] = None


# Source Schemas
class SourceBase(BaseModel):
    name: str
    url: Optional[str] = None
    source_type: str
    credibility_score: int = Field(ge=1, le=10, default=5)

class Source(SourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: Optional[datetime] = None
    update_frequency: Optional[str] = None


# Food Contaminant Level Schemas
class FoodContaminantLevelBase(BaseModel):
    contaminant_id: int
    level_value: Optional[float] = None
    level_unit: Optional[str] = None
    risk_score: Optional[int] = Field(None, ge=1, le=100)
    risk_category: Optional[str] = None
    notes: Optional[str] = None

class FoodContaminantLevel(FoodContaminantLevelBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    food_id: UUID
    source_id: Optional[int] = None
    measurement_date: Optional[datetime] = None
    created_at: datetime
    contaminant: Contaminant
    source: Optional[Source] = None


# Food Nutrient Schemas
class FoodNutrientBase(BaseModel):
    nutrient_name: str
    amount: Optional[float] = None
    unit: Optional[str] = None
    per_serving_size: Optional[str] = None

class FoodNutrient(FoodNutrientBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    food_id: UUID
    source_id: Optional[int] = None
    source: Optional[Source] = None


# State Advisory Schemas
class StateAdvisoryBase(BaseModel):
    state_code: str
    state_name: str
    waterbody_name: Optional[str] = None
    fish_species: str
    contaminant_type: Optional[str] = None
    advisory_text: Optional[str] = None
    consumption_limit: Optional[str] = None
    advisory_level: Optional[str] = None

class StateAdvisory(StateAdvisoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    effective_date: Optional[datetime] = None


# Sustainability Rating Schemas
class SustainabilityRatingBase(BaseModel):
    rating: str
    rating_score: Optional[int] = None
    source: str
    fishing_method: Optional[str] = None
    location: Optional[str] = None
    is_farmed: Optional[bool] = None
    is_wild_caught: Optional[bool] = None

class SustainabilityRating(SustainabilityRatingBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    certification: List[str] = []
    habitat_impact: Optional[str] = None


# Food Schemas
class FoodBase(BaseModel):
    name: str
    common_names: List[str] = []
    description: Optional[str] = None
    image_url: Optional[str] = None
    barcode: Optional[str] = None

class FoodCreate(FoodBase):
    category_id: Optional[int] = None
    slug: str

class Food(FoodBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    category_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[FoodCategory] = None


class FoodDetail(Food):
    """Extended food schema with contaminants and nutrients"""
    contaminant_levels: List[FoodContaminantLevel] = []
    nutrients: List[FoodNutrient] = []
    advisories: List[StateAdvisory] = []
    sustainability_ratings: List[SustainabilityRating] = []


# Search Schemas
class FoodSearchParams(BaseModel):
    q: Optional[str] = Field(None, description="Search query")
    category: Optional[str] = Field(None, description="Category slug")
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)

class FoodSearchResult(BaseModel):
    total: int
    foods: List[Food]


# Research Paper Schemas
class ResearchPaperBase(BaseModel):
    title: str
    authors: List[str] = []
    abstract: Optional[str] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    keywords: List[str] = []
    related_contaminants: List[str] = []
    related_foods: List[str] = []

class ResearchPaper(ResearchPaperBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    publication_date: Optional[datetime] = None
    created_at: datetime


# ====================
# User & Authentication Schemas (Issue #25)
# ====================

# User Schemas
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    preferences: Optional[dict] = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_verified: bool
    is_active: bool
    preferences: Optional[dict] = None

class UserInDB(User):
    hashed_password: str


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None


# Saved Food Schemas
class SavedFoodBase(BaseModel):
    food_id: UUID
    notes: Optional[str] = None

class SavedFoodCreate(SavedFoodBase):
    pass

class SavedFood(SavedFoodBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    saved_at: datetime
    food: Optional[Food] = None


# Meal Plan Schemas
class MealPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    date: Optional[datetime] = None
    meal_type: Optional[str] = None

class MealPlanCreate(MealPlanBase):
    pass

class MealPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    meal_type: Optional[str] = None


# Meal Plan Food Schemas
class MealPlanFoodBase(BaseModel):
    food_id: UUID
    serving_size: Optional[str] = None
    servings: float = 1.0
    notes: Optional[str] = None

class MealPlanFoodCreate(MealPlanFoodBase):
    pass

class MealPlanFoodInPlan(MealPlanFoodBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    meal_plan_id: UUID
    added_at: datetime
    food: Optional[Food] = None


class MealPlan(MealPlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    foods: List[MealPlanFoodInPlan] = []


# LLM Query Schemas
class NaturalLanguageQuery(BaseModel):
    query: str
    context: Optional[str] = None  # user, advisory, sustainability, etc.

class NaturalLanguageResponse(BaseModel):
    answer: str
    sources: List[Food] = []
    recalls: List[dict] = []
    advisories: List[dict] = []
