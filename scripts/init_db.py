"""Database initialization script."""
import asyncio
import sys
import json
import os
from pathlib import Path

# Add apps/api to path to import from app
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from app.db.models import Base, Source, Food, Contaminant, FoodContaminantLevel, FoodNutrient, FoodCategory
from app.core.config import settings

def slugify(text: str) -> str:
    return text.lower().replace(" ", "-").replace("/", "-")

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

        # 2. Add Contaminants
        mercury = Contaminant(
            name="Mercury",
            chemical_name="Methylmercury",
            unit="ppm",
            description="A heavy metal that can accumulate in fish."
        )
        
        session.add(mercury)
        await session.commit()

        # 3. Add Category
        seafood_category = FoodCategory(
            name="Seafood",
            slug="seafood",
            description="Fish and shellfish"
        )
        session.add(seafood_category)
        await session.commit()

        # Helper to get or create food
        existing_foods = {} # name -> Food object

        async def get_or_create_food(name, description=""):
            # Simple normalization: duplicate singular/plural handling would need more logic
            # For now, treat exact name matches.
            if name in existing_foods:
                return existing_foods[name]
            
            # Check DB
            stmt = select(Food).where(Food.name == name)
            result = await session.execute(stmt)
            food = result.scalar_one_or_none()
            
            if not food:
                food = Food(
                    name=name,
                    slug=slugify(name),
                    description=description,
                    category_id=seafood_category.id
                )
                session.add(food)
                await session.flush()
            
            existing_foods[name] = food
            return food

        # 4. Load FDA Data
        fda_file = Path("data/fda_mercury_1990_2012.json")
        if fda_file.exists():
            print(f"Loading FDA data from {fda_file}...")
            with open(fda_file) as f:
                fda_data = json.load(f)
                
            count = 0
            for item in fda_data:
                name = item["name"]
                mean_ppm = item["mercury_mean_ppm"]
                
                food = await get_or_create_food(name, f"Source: FDA (1990-2012)")
                
                # Add Mercury Level
                level = FoodContaminantLevel(
                    food_id=food.id,
                    contaminant_id=mercury.id,
                    level_value=mean_ppm,
                    level_unit="ppm",
                    source_id=fda_source.id,
                    measurement_date=func.now()
                )
                session.add(level)
                count += 1
            print(f"Loaded {count} FDA records.")
        else:
            print(f"Warning: {fda_file} not found.")

        # 5. Load EWG Data
        ewg_file = Path("data/ewg_seafood.json")
        if ewg_file.exists():
            print(f"Loading EWG data from {ewg_file}...")
            with open(ewg_file) as f:
                ewg_data = json.load(f)
            
            count = 0
            for item in ewg_data:
                name = item["name"]
                category = item["category"]
                mercury_level = item["mercury_level"]
                omega3 = item["omega_3_level"]
                sustainable = item["sustainable"]
                
                # EWG names like "Wild salmon" vs FDA "Salmon"
                # We won't do fuzzy match for now, just create new entries if mismatch
                
                desc = f"EWG Category: {category}."
                if omega3:
                    desc += f" Omega-3: {omega3}."
                if sustainable is not None:
                    desc += " Sustainable." if sustainable else " Unsustainable."
                
                food = await get_or_create_food(name, desc)
                
                # Update description if it was generic
                if "Source: FDA" in food.description:
                     food.description += f" | {desc}"
                     session.add(food)
                
                # We can't easily add exact contaminant levels since EWG gives categories (Low/High)
                # But we validly loaded the food entity.
                
                count += 1
            print(f"Loaded {count} EWG records.")
        else:
            print(f"Warning: {ewg_file} not found.")

        await session.commit()

        # Verify
        result = await session.execute(select(func.count(Food.id)))
        count = result.scalar()
        print(f"\nTotal foods in database: {count}")

    await engine.dispose()
    print("\nDatabase initialization complete!")


if __name__ == "__main__":
    asyncio.run(init_database())
