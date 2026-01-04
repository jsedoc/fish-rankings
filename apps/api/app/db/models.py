"""
SQLAlchemy database models
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, ARRAY, Text, JSON, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class FoodCategory(Base):
    __tablename__ = "food_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("food_categories.id"), nullable=True)
    description = Column(Text, nullable=True)

    # Relationships
    foods = relationship("Food", back_populates="category")
    parent = relationship("FoodCategory", remote_side=[id], backref="children")


class Food(Base):
    __tablename__ = "foods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    common_names = Column(ARRAY(String), default=list)
    category_id = Column(Integer, ForeignKey("food_categories.id"), nullable=True, index=True)
    description = Column(Text)
    image_url = Column(String(500))
    barcode = Column(String(50), index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("FoodCategory", back_populates="foods")
    contaminant_levels = relationship("FoodContaminantLevel", back_populates="food", cascade="all, delete-orphan")
    nutrients = relationship("FoodNutrient", back_populates="food", cascade="all, delete-orphan")

    # Note: Fuzzy search index (pg_trgm) can be added later with:
    # CREATE EXTENSION IF NOT EXISTS pg_trgm;
    # CREATE INDEX idx_food_name_trgm ON foods USING gin (name gin_trgm_ops);


class Contaminant(Base):
    __tablename__ = "contaminants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    chemical_name = Column(String(255))
    description = Column(Text)
    health_effects = Column(Text)
    acceptable_daily_intake = Column(Float)  # in mg/kg body weight
    unit = Column(String(20))  # ppm, ppb, mg/kg, etc.

    # Relationships
    food_levels = relationship("FoodContaminantLevel", back_populates="contaminant")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500))
    source_type = Column(String(50))  # government, academic, ngo, commercial
    credibility_score = Column(Integer, default=5)  # 1-10
    last_updated = Column(DateTime(timezone=True))
    update_frequency = Column(String(50))  # daily, weekly, monthly

    # Relationships
    contaminant_levels = relationship("FoodContaminantLevel", back_populates="source")
    nutrients = relationship("FoodNutrient", back_populates="source")


class FoodContaminantLevel(Base):
    __tablename__ = "food_contaminant_levels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_id = Column(UUID(as_uuid=True), ForeignKey("foods.id", ondelete="CASCADE"), nullable=False, index=True)
    contaminant_id = Column(Integer, ForeignKey("contaminants.id"), nullable=False, index=True)
    level_value = Column(Float)
    level_unit = Column(String(20))
    risk_score = Column(Integer)  # 1-100
    risk_category = Column(String(20))  # low, medium, high, critical
    source_id = Column(Integer, ForeignKey("sources.id"))
    measurement_date = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    food = relationship("Food", back_populates="contaminant_levels")
    contaminant = relationship("Contaminant", back_populates="food_levels")
    source = relationship("Source", back_populates="contaminant_levels")


class FoodNutrient(Base):
    __tablename__ = "food_nutrients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_id = Column(UUID(as_uuid=True), ForeignKey("foods.id", ondelete="CASCADE"), nullable=False, index=True)
    nutrient_name = Column(String(100), nullable=False)
    amount = Column(Float)
    unit = Column(String(20))
    per_serving_size = Column(String(50))
    source_id = Column(Integer, ForeignKey("sources.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    food = relationship("Food", back_populates="nutrients")
    source = relationship("Source", back_populates="nutrients")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    preferences = Column(JSONB, default=dict)  # dietary restrictions, concerns, etc.


class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    authors = Column(ARRAY(String))
    abstract = Column(Text)
    journal = Column(String(255))
    publication_date = Column(DateTime(timezone=True))
    doi = Column(String(100), unique=True, index=True)
    pmid = Column(String(50), unique=True, index=True)  # PubMed ID
    url = Column(String(500))
    keywords = Column(ARRAY(String))
    related_contaminants = Column(ARRAY(String))
    related_foods = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Note: GIN index for keywords can be added later if needed
    # CREATE INDEX idx_paper_keywords ON research_papers USING gin (keywords);


# ====================
# Milestone 2 Models
# ====================

class FoodRecall(Base):
    """FDA Food Recall data"""
    __tablename__ = "food_recalls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recall_number = Column(String(50), unique=True, nullable=False, index=True)
    product_description = Column(Text, nullable=False)
    reason_for_recall = Column(Text)
    recall_date = Column(DateTime(timezone=True))
    report_date = Column(DateTime(timezone=True))
    company_name = Column(String(255))
    distribution_pattern = Column(Text)
    product_quantity = Column(String(100))
    status = Column(String(50))  # Ongoing, Completed, Terminated
    classification = Column(String(20), index=True)  # Class I, II, or III
    code_info = Column(Text)
    voluntary_mandated = Column(String(50))
    city = Column(String(100))
    state = Column(String(2))
    country = Column(String(100))
    event_id = Column(String(50), index=True)

    # Link to food if we can match it
    food_id = Column(UUID(as_uuid=True), ForeignKey("foods.id", ondelete="SET NULL"), nullable=True, index=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StateAdvisory(Base):
    """EPA State Fish Advisory data"""
    __tablename__ = "state_advisories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state_code = Column(String(2), nullable=False, index=True)
    state_name = Column(String(100), nullable=False)
    waterbody_name = Column(String(255))
    waterbody_type = Column(String(50))  # lake, river, ocean, etc.
    fish_species = Column(String(255), nullable=False, index=True)
    contaminant_type = Column(String(100))  # mercury, PCBs, etc.
    contaminant_level = Column(Float)
    contaminant_unit = Column(String(20))
    advisory_text = Column(Text)
    consumption_limit = Column(String(255))  # e.g., "1 meal per week"
    advisory_level = Column(String(50))  # Do Not Eat, Limited Consumption, etc.
    sensitive_populations = Column(ARRAY(String))  # pregnant women, children, etc.
    effective_date = Column(DateTime(timezone=True))
    source_url = Column(String(500))

    # Link to food if we can match it
    food_id = Column(UUID(as_uuid=True), ForeignKey("foods.id", ondelete="SET NULL"), nullable=True, index=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SustainabilityRating(Base):
    """NOAA FishWatch / Seafood Watch sustainability ratings"""
    __tablename__ = "sustainability_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_id = Column(UUID(as_uuid=True), ForeignKey("foods.id", ondelete="CASCADE"), nullable=False, index=True)

    # Rating info
    rating = Column(String(50), nullable=False)  # Best Choice, Good Alternative, Avoid
    rating_score = Column(Integer)  # 1-10 numeric score
    source = Column(String(100), nullable=False)  # NOAA, Seafood Watch, etc.

    # Details
    fishing_method = Column(String(255))
    location = Column(String(255))
    is_farmed = Column(Boolean)
    is_wild_caught = Column(Boolean)
    overfished = Column(Boolean)
    overfishing_occurring = Column(Boolean)

    # Additional info
    habitat_impact = Column(String(50))  # low, moderate, high
    bycatch_impact = Column(String(50))  # low, moderate, high
    management_rating = Column(String(50))  # effective, moderately effective, etc.

    # Text details
    sustainability_notes = Column(Text)
    certification = Column(ARRAY(String))  # MSC, ASC, etc.

    # Dates
    last_updated = Column(DateTime(timezone=True))
    valid_until = Column(DateTime(timezone=True))

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    food = relationship("Food", backref="sustainability_ratings")
