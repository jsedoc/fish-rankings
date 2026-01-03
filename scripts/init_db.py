"""Database initialization script."""
import asyncio
import sys
from pathlib import Path

# Add apps/api to path to import from app
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from app.db.models import Base, Source, Food, Contaminant, FoodContaminantLevel, FoodNutrient, FoodCategory
from app.core.config import settings


async def init_database():
    """Initialize the database with tables and sample data."""
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # 1. Add sources
        ewg_source = Source(
            name="EWG Shopper's Guide",
            url="https://www.ewg.org/consumer-guides/ewgs-consumer-guide-seafood",
            source_type="ngo"
        )
        
        fda_source = Source(
            name="FDA Fish Advice",
            url="https://www.fda.gov/food/consumers/advice-about-eating-fish",
            source_type="government"
        )
        
        session.add_all([ewg_source, fda_source])
        await session.commit()

        # 2. Add Contaminants (Prerequisite for FoodContaminantLevel)
        mercury = Contaminant(
            name="Mercury",
            chemical_name="Methylmercury",
            unit="ppm",
            description="A heavy metal that can accumulate in fish."
        )
        pcbs = Contaminant(
            name="PCBs",
            chemical_name="Polychlorinated Biphenyls",
            unit="ppb",
            description="Industrial chemicals that bioaccumulate."
        )
        
        session.add_all([mercury, pcbs])
        await session.commit()

        # 3. Add Category
        seafood_category = FoodCategory(
            name="Seafood",
            slug="seafood",
            description="Fish and shellfish"
        )
        session.add(seafood_category)
        await session.commit()

        # 4. Add fish species (Foods)
        fish_data = [
            {
                "name": "Wild Salmon",
                "slug": "wild-salmon",
                "description": "Wild-caught Pacific salmon, including varieties like Sockeye, Coho, and King salmon",
                "source": ewg_source,
                "contaminants": [
                    {"contaminant": mercury, "level": 0.014},
                    {"contaminant": pcbs, "level": 2.0, "unit": "ppb"},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 1.8, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 25.0, "unit": "g", "per_serving": "100g"},
                    {"name": "Vitamin D", "amount": 11.0, "unit": "mcg", "per_serving": "100g"},
                ],
            },
            {
                "name": "Sardines",
                "slug": "sardines",
                "description": "Small, oily fish packed with nutrients",
                "source": ewg_source,
                "contaminants": [
                    {"contaminant": mercury, "level": 0.013},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 1.5, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 25.0, "unit": "g", "per_serving": "100g"},
                    {"name": "Calcium", "amount": 382.0, "unit": "mg", "per_serving": "100g"},
                    {"name": "Vitamin B12", "amount": 8.9, "unit": "mcg", "per_serving": "100g"},
                ],
            },
            {
                "name": "Atlantic Mackerel",
                "slug": "atlantic-mackerel",
                "description": "Oily fish rich in omega-3 fatty acids",
                "source": ewg_source,
                "contaminants": [
                    {"contaminant": mercury, "level": 0.050},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 2.6, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 19.0, "unit": "g", "per_serving": "100g"},
                    {"name": "Vitamin B12", "amount": 8.7, "unit": "mcg", "per_serving": "100g"},
                ],
            },
            {
                "name": "Farmed Rainbow Trout",
                "slug": "farmed-rainbow-trout",
                "description": "Freshwater fish typically farmed in the US",
                "source": fda_source,
                "contaminants": [
                    {"contaminant": mercury, "level": 0.071},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 0.98, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 20.5, "unit": "g", "per_serving": "100g"},
                ],
            },
            {
                "name": "Albacore Tuna",
                "slug": "albacore-tuna",
                "description": "White tuna with higher mercury levels than light tuna",
                "source": fda_source,
                "contaminants": [
                    {"contaminant": mercury, "level": 0.350},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 1.5, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 30.0, "unit": "g", "per_serving": "100g"},
                ],
            },
            {
                "name": "King Mackerel",
                "slug": "king-mackerel",
                "description": "Large mackerel species with high mercury content",
                "source": fda_source,
                "contaminants": [
                    {"contaminant": mercury, "level": 0.730},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 2.2, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 21.0, "unit": "g", "per_serving": "100g"},
                ],
            },
        ]

        for fish in fish_data:
            food = Food(
                name=fish["name"],
                slug=fish["slug"],
                description=fish["description"],
                category_id=seafood_category.id
            )
            session.add(food)
            await session.flush()  # Get ID

            # Add contaminants
            for cont in fish["contaminants"]:
                level = FoodContaminantLevel(
                    food_id=food.id,
                    contaminant_id=cont["contaminant"].id,
                    level_value=cont["level"],
                    level_unit=cont.get("unit", cont["contaminant"].unit),
                    source_id=fish["source"].id,
                    measurement_date=func.now()
                )
                session.add(level)

            # Add nutrients
            for nutr in fish["nutrients"]:
                nutrient = FoodNutrient(
                    food_id=food.id,
                    nutrient_name=nutr["name"],
                    amount=nutr["amount"],
                    unit=nutr["unit"],
                    per_serving_size=nutr["per_serving"],
                    source_id=fish["source"].id
                )
                session.add(nutrient)

        await session.commit()

        # Verify data was added
        result = await session.execute(select(Source).where(Source.name == "EWG Shopper's Guide"))
        ewg = result.scalar_one_or_none()
        print(f"\nAdded source: {ewg.name}")

        result = await session.execute(select(Food))
        foods_list = result.scalars().all()
        print(f"\nAdded {len(foods_list)} foods:")
        for f in foods_list:
            print(f"  - {f.name}")

    await engine.dispose()
    print("\nDatabase initialization complete!")


if __name__ == "__main__":
    asyncio.run(init_database())
