"""
Initialize database and seed with data from scrapers
Run this script to populate the database with initial food safety data
"""
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "apps" / "api"))

from sqlalchemy import text
from app.db.session import engine, AsyncSessionLocal
from app.db.models import Base, Food, FoodCategory, Contaminant, Source, FoodContaminantLevel, FoodNutrient, ResearchPaper
from datetime import datetime
import re

# Import scrapers
sys.path.append(str(Path(__file__).parent))
from scrapers.fda_fish_scraper import scrape_fda_fish_data, scrape_fda_detailed_mercury
from scrapers.ewg_produce_scraper import scrape_ewg_produce
from scrapers.pubmed_scraper import collect_food_safety_papers
from scrapers.usda_api_client import get_nutrition_for_common_foods


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
        except:
            print("  ⚠️  Could not enable pg_trgm extension (optional)")
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
            Contaminant(
                name="Mercury",
                chemical_name="Methylmercury",
                description="Toxic heavy metal that accumulates in fish",
                health_effects="Neurological damage, developmental issues, especially harmful to pregnant women and children",
                acceptable_daily_intake=0.0001,  # 0.1 µg/kg body weight/day
                unit="ppm"
            ),
            Contaminant(
                name="Pesticides",
                chemical_name="Various organophosphates and other chemicals",
                description="Agricultural chemicals used to control pests",
                health_effects="Varies by chemical; some are neurotoxic, endocrine disruptors, or carcinogenic",
                unit="ppm"
            ),
            Contaminant(
                name="PCBs",
                chemical_name="Polychlorinated Biphenyls",
                description="Persistent organic pollutants found in fatty fish",
                health_effects="Carcinogenic, endocrine disruption, immune system effects",
                unit="ppb"
            ),
            Contaminant(
                name="Microplastics",
                description="Tiny plastic particles found in seafood and water",
                health_effects="Long-term effects unknown; potential inflammation and cellular damage",
                unit="particles/g"
            ),
            Contaminant(
                name="Lead",
                description="Toxic heavy metal from environmental contamination",
                health_effects="Neurological damage, developmental delays, kidney damage",
                acceptable_daily_intake=0.0036,
                unit="ppm"
            ),
        ]
        session.add_all(contaminants)
        await session.commit()
    print(f"✅ Created {len(contaminants)} contaminants")


async def seed_sources():
    """Create data sources"""
    print("📚 Seeding data sources...")
    async with AsyncSessionLocal() as session:
        sources = [
            Source(
                name="FDA Fish Advice",
                url="https://www.fda.gov/food/consumers/advice-about-eating-fish",
                source_type="government",
                credibility_score=10,
                last_updated=datetime.now(),
                update_frequency="annually"
            ),
            Source(
                name="EWG Shopper's Guide",
                url="https://www.ewg.org/foodnews/",
                source_type="ngo",
                credibility_score=8,
                last_updated=datetime.now(),
                update_frequency="annually"
            ),
            Source(
                name="USDA FoodData Central",
                url="https://fdc.nal.usda.gov/",
                source_type="government",
                credibility_score=10,
                last_updated=datetime.now(),
                update_frequency="monthly"
            ),
            Source(
                name="PubMed/NCBI",
                url="https://pubmed.ncbi.nlm.nih.gov/",
                source_type="academic",
                credibility_score=9,
                last_updated=datetime.now(),
                update_frequency="daily"
            ),
        ]
        session.add_all(sources)
        await session.commit()
    print(f"✅ Created {len(sources)} data sources")


async def seed_fish_data():
    """Seed fish data from FDA"""
    print("🐟 Seeding fish data...")

    # Get seafood category
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT id FROM food_categories WHERE slug = 'seafood'"))
        seafood_category_id = result.scalar_one()

        result = await session.execute(text("SELECT id FROM sources WHERE name = 'FDA Fish Advice'"))
        fda_source_id = result.scalar_one()

        result = await session.execute(text("SELECT id FROM contaminants WHERE name = 'Mercury'"))
        mercury_id = result.scalar_one()

    # Scrape data
    fish_data = await scrape_fda_fish_data()
    mercury_levels = await scrape_fda_detailed_mercury()

    async with AsyncSessionLocal() as session:
        food_count = 0

        for fish_info in fish_data:
            # Create food entry
            food = Food(
                name=fish_info["name"],
                slug=slugify(fish_info["name"]),
                category_id=seafood_category_id,
                description=f"{fish_info['consumption_advice']}. Source: FDA Fish Advice 2024",
                common_names=[fish_info["name"].lower()]
            )
            session.add(food)
            await session.flush()  # Get the ID

            # Add mercury contaminant level
            mercury_ppm = mercury_levels.get(fish_info["name"], fish_info.get("mercury_ppm", 0.1))

            contaminant_level = FoodContaminantLevel(
                food_id=food.id,
                contaminant_id=mercury_id,
                level_value=mercury_ppm,
                level_unit="ppm",
                risk_score=fish_info["risk_score"],
                risk_category=fish_info["risk_category"],
                source_id=fda_source_id,
                measurement_date=datetime.now(),
                notes=fish_info["consumption_advice"]
            )
            session.add(contaminant_level)
            food_count += 1

        await session.commit()

    print(f"✅ Created {food_count} fish entries")


async def seed_produce_data():
    """Seed produce data from EWG"""
    print("🥗 Seeding produce data...")

    # Get produce category
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT id FROM food_categories WHERE slug = 'produce'"))
        produce_category_id = result.scalar_one()

        result = await session.execute(text("SELECT id FROM sources WHERE name = 'EWG Shopper''s Guide'"))
        ewg_source_id = result.scalar_one()

        result = await session.execute(text("SELECT id FROM contaminants WHERE name = 'Pesticides'"))
        pesticides_id = result.scalar_one()

    # Scrape data
    produce_data = await scrape_ewg_produce()

    async with AsyncSessionLocal() as session:
        food_count = 0

        for produce_info in produce_data:
            # Create food entry
            food = Food(
                name=produce_info["name"],
                slug=slugify(produce_info["name"]),
                category_id=produce_category_id,
                description=f"{produce_info['list_type']}. {produce_info['advice']}",
                common_names=[produce_info["name"].lower()]
            )
            session.add(food)
            await session.flush()

            # Add pesticide contaminant level
            contaminant_level = FoodContaminantLevel(
                food_id=food.id,
                contaminant_id=pesticides_id,
                level_value=None,  # EWG doesn't provide exact levels
                level_unit="relative",
                risk_score=produce_info["risk_score"],
                risk_category=produce_info["risk_category"],
                source_id=ewg_source_id,
                measurement_date=datetime.now(),
                notes=produce_info["advice"]
            )
            session.add(contaminant_level)
            food_count += 1

        await session.commit()

    print(f"✅ Created {food_count} produce entries")


async def seed_research_papers():
    """Seed research papers from PubMed"""
    print("📄 Seeding research papers...")

    # Collect papers (limit to avoid long runtime)
    papers = await collect_food_safety_papers(max_per_topic=20)

    async with AsyncSessionLocal() as session:
        paper_count = 0

        for paper_data in papers:
            # Extract keywords from title and abstract
            text = f"{paper_data.get('title', '')} {paper_data.get('abstract', '')}"
            keywords = []

            # Simple keyword extraction
            keyword_terms = ["mercury", "pesticide", "contamination", "microplastic",
                           "safety", "toxicity", "heavy metal", "PCB", "nutrition"]
            for term in keyword_terms:
                if term.lower() in text.lower():
                    keywords.append(term)

            paper = ResearchPaper(
                title=paper_data["title"],
                authors=paper_data.get("authors", []),
                abstract=paper_data.get("abstract", ""),
                journal=paper_data.get("journal", ""),
                publication_date=datetime.fromisoformat(paper_data["publication_date"]) if paper_data.get("publication_date") else None,
                doi=paper_data.get("doi"),
                pmid=paper_data.get("pmid"),
                url=paper_data.get("url", ""),
                keywords=keywords,
                related_contaminants=keywords  # Simplified
            )
            session.add(paper)
            paper_count += 1

        await session.commit()

    print(f"✅ Created {paper_count} research paper entries")


async def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("🌱 FOOD SAFETY PLATFORM - DATABASE INITIALIZATION")
    print("="*60 + "\n")

    try:
        # Create tables
        await create_tables()

        # Seed reference data
        await seed_categories()
        await seed_contaminants()
        await seed_sources()

        # Seed food data
        await seed_fish_data()
        await seed_produce_data()

        # Seed research papers
        await seed_research_papers()

        print("\n" + "="*60)
        print("✅ DATABASE INITIALIZATION COMPLETE!")
        print("="*60)
        print("\nYour database now contains:")
        print("  - Food categories")
        print("  - Contaminant types")
        print("  - Trusted data sources")
        print("  - 60+ fish species with mercury data")
        print("  - 30+ produce items with pesticide data")
        print("  - Research papers on food safety")
        print("\nNext steps:")
        print("  1. Start the API server: cd apps/api && uvicorn main:app --reload")
        print("  2. Start the web app: cd apps/web && npm run dev")
        print("  3. Visit http://localhost:3000")
        print()

    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
