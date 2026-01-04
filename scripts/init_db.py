"""
Initialize database and seed with data from local JSONs and available scrapers.
"""
import sys
import json
import os
import asyncio
import re
from pathlib import Path
from datetime import datetime

# Add parent directories to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "apps" / "api"))
sys.path.append(str(PROJECT_ROOT / "packages"))

from sqlalchemy import text, select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.session import engine, AsyncSessionLocal
from app.db.models import Base, Food, FoodCategory, Contaminant, Source, FoodContaminantLevel, FoodNutrient, ResearchPaper
from app.core.config import settings

# Import scrapers (optional, wrapped in try blocks later)
try:
    from scrapers.ewg_produce_scraper import scrape_ewg_produce
    from scrapers.pubmed_scraper import collect_food_safety_papers
except ImportError as e:
    print(f"Warning: Could not import scrapers: {e}")

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

async def create_tables():
    """Create all database tables"""
    print("🗄️  Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # Enable pg_trgm extension for fuzzy search
        try:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        except Exception as e:
            print(f"  ⚠️  Could not enable pg_trgm extension: {e}")
    print("✅ Tables created successfully")

async def seed_categories():
    """Create food categories"""
    print("📁 Seeding categories...")
    async with AsyncSessionLocal() as session:
        categories = [
            FoodCategory(name="Seafood", slug="seafood", description="Fish, shellfish, and other seafood"),
            FoodCategory(name="Produce", slug="produce", description="Fruits and vegetables"),
            FoodCategory(name="Meat & Poultry", slug="meat-poultry", description="Beef, pork, chicken, and other meats"),
            FoodCategory(name="Dairy", slug="dairy", description="Milk, cheese, yogurt, and dairy products"),
            FoodCategory(name="Grains", slug="grains", description="Rice, wheat, oats, and grain products"),
            FoodCategory(name="Processed Foods", slug="processed", description="Packaged and processed food items"),
        ]
        session.add_all(categories)
        await session.commit()
    print(f"✅ Created {len(categories)} categories")

async def seed_contaminants():
    """Create contaminant types"""
    print("☣️  Seeding contaminants...")
    async with AsyncSessionLocal() as session:
        contaminants = [
            Contaminant(name="Mercury", chemical_name="Methylmercury", unit="ppm", description="Toxic heavy metal"),
            Contaminant(name="Pesticides", chemical_name="Various", unit="ppm", description="Agricultural chemicals"),
            Contaminant(name="PCBs", chemical_name="Polychlorinated Biphenyls", unit="ppb", description="Industrial chemicals"),
            Contaminant(name="Microplastics", unit="particles/g", description="Tiny plastic particles"),
            Contaminant(name="Lead", unit="ppm", description="Toxic heavy metal"),
        ]
        session.add_all(contaminants)
        await session.commit()
    print(f"✅ Created {len(contaminants)} contaminants")

async def seed_sources():
    """Create data sources"""
    print("📚 Seeding data sources...")
    async with AsyncSessionLocal() as session:
        sources = [
            Source(name="FDA Fish Advice", url="https://www.fda.gov/food/consumers/advice-about-eating-fish", source_type="government"),
            Source(name="EWG Shopper's Guide", url="https://www.ewg.org/consumer-guides/ewgs-consumer-guide-seafood", source_type="ngo"),
            Source(name="USDA FoodData Central", url="https://fdc.nal.usda.gov/", source_type="government"),
            Source(name="PubMed/NCBI", url="https://pubmed.ncbi.nlm.nih.gov/", source_type="academic"),
        ]
        session.add_all(sources)
        await session.commit()
    print(f"✅ Created {len(sources)} data sources")

async def seed_fish_data():
    """Seed fish data from local JSON (preferred for stability)"""
    print("🐟 Seeding fish data (from JSON)...")

    # Path to robust data (resolve relative to script location)
    root_dir = Path(__file__).parent.parent
    fda_file = root_dir / "data" / "fda_mercury_1990_2012.json"
    ewg_file = root_dir / "data" / "ewg_seafood.json"

    print(f"DEBUG: Checking FDA file: {fda_file} (Exists: {fda_file.exists()})")
    print(f"DEBUG: Checking EWG file: {ewg_file} (Exists: {ewg_file.exists()})")

    if not fda_file.exists() and not ewg_file.exists():
        print(f"⚠️  No JSON data found at {root_dir / 'data'}. Skipping fish seed.")
        return

    async with AsyncSessionLocal() as session:
        # Get References
        seafood_cat = (await session.execute(select(FoodCategory).where(FoodCategory.slug == 'seafood'))).scalar_one()
        fda_src = (await session.execute(select(Source).where(Source.name.like('FDA%')))).scalar_one()
        ewg_src = (await session.execute(select(Source).where(Source.name.like('EWG%')))).scalar_one()
        mercury = (await session.execute(select(Contaminant).where(Contaminant.name == 'Mercury'))).scalar_one()

        existing_foods = {}

        async def get_or_create_food(name, description=""):
            if name in existing_foods: return existing_foods[name]
            result = await session.execute(select(Food).where(Food.name == name))
            food = result.scalar_one_or_none()
            if not food:
                food = Food(name=name, slug=slugify(name), description=description, category_id=seafood_cat.id)
                session.add(food)
                await session.flush()
            existing_foods[name] = food
            return food

        count = 0
        # FDA Data
        print(f"DEBUG: Processing FDA Data from {fda_file}")
        if fda_file.exists():
            with open(fda_file) as f:
                data = json.load(f)
                print(f"DEBUG: Loaded {len(data)} items from FDA JSON")
                for item in data:
                    try:
                        print(f"DEBUG: Processing FDA Item: {item.get('name')}")
                        food = await get_or_create_food(item["name"], "Source: FDA (1990-2012)")
                        level = FoodContaminantLevel(
                            food_id=food.id, contaminant_id=mercury.id, level_value=item["mercury_mean_ppm"],
                            level_unit="ppm", source_id=fda_src.id, measurement_date=datetime.now()
                        )
                        session.add(level)
                        count += 1
                    except Exception as e:
                        print(f"ERROR processing item {item}: {e}")

        # EWG Data
        print(f"DEBUG: Processing EWG Data from {ewg_file}")
        if ewg_file.exists():
            with open(ewg_file) as f:
                data = json.load(f)
                print(f"DEBUG: Loaded {len(data)} items from EWG JSON")
                for item in data:
                    try:
                        print(f"DEBUG: Processing EWG Item: {item.get('name')}")
                        desc = f"EWG: {item['category']}. Omega-3: {item.get('omega_3_level')}. Sustainable: {item.get('sustainable')}"
                        food = await get_or_create_food(item["name"], desc)
                        if "Source: FDA" in food.description:
                            food.description += f" | {desc}"
                            session.add(food)
                    except Exception as e:
                        print(f"ERROR processing item {item}: {e}")

        print(f"DEBUG: Committing {count} records...")
        await session.commit()
        print("DEBUG: Commit successful.")
    print(f"✅ Seeded fish data ({count} FDA records processed).")

async def seed_produce_data_dynamic():
    """Seed produce data using the new scrapers if available"""
    print("🥗 Seeding produce data (Dynamic Scraper)...")
    try:
        from scrapers.ewg_produce_scraper import scrape_ewg_produce
        produce_data = await scrape_ewg_produce()

        async with AsyncSessionLocal() as session:
            produce_cat = (await session.execute(select(FoodCategory).where(FoodCategory.slug == 'produce'))).scalar_one()
            ewg_src = (await session.execute(select(Source).where(Source.name.like('EWG%')))).scalar_one()
            pesticides = (await session.execute(select(Contaminant).where(Contaminant.name == 'Pesticides'))).scalar_one()

            count = 0
            for item in produce_data:
                food = Food(
                    name=item["name"], slug=slugify(item["name"]), category_id=produce_cat.id,
                    description=f"{item['list_type']}. {item['advice']}"
                )
                session.add(food)
                await session.flush()

                lvl = FoodContaminantLevel(
                    food_id=food.id, contaminant_id=pesticides.id, level_value=None, level_unit="relative",
                    risk_category=item["risk_category"], source_id=ewg_src.id, measurement_date=datetime.now(),
                    notes=item["advice"]
                )
                session.add(lvl)
                count += 1
            await session.commit()
            print(f"✅ Created {count} produce entries")
    except Exception as e:
        print(f"⚠️  produce scrape failed or skipped: {e}")

async def seed_research_papers_dynamic():
    print("📄 Seeding research papers (Dynamic Scraper)...")
    try:
        from scrapers.pubmed_scraper import collect_food_safety_papers
        papers = await collect_food_safety_papers(max_per_topic=5) # Reduced limit for speed

        async with AsyncSessionLocal() as session:
            count = 0
            for p in papers:
                title = p.get("title", "No Title")
                # Deduplicate
                exists = (await session.execute(select(ResearchPaper).where(ResearchPaper.title == title))).scalar_one_or_none()
                if exists: continue

                paper = ResearchPaper(
                    title=title, authors=p.get("authors", []), abstract=p.get("abstract", ""),
                    journal=p.get("journal", ""), url=p.get("url", ""), doi=p.get("doi")
                )
                session.add(paper)
                count += 1
            await session.commit()
            print(f"✅ Created {count} research papers")
    except Exception as e:
        print(f"⚠️  Research paper scrape failed or skipped: {e}")

async def main():
    print("\n🌱 INITIALIZING DATABASE...")
    await create_tables()
    await seed_categories()
    await seed_contaminants()
    await seed_sources()

    # Core Data (Reliable)
    await seed_fish_data()

    # Feature Data (Best Effort)
    await seed_produce_data_dynamic()
    await seed_research_papers_dynamic()

    print("\n✅ DONE.")

if __name__ == "__main__":
    asyncio.run(main())
