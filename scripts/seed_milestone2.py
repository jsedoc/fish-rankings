"""
Milestone 2 Database Seeding Script

Seeds the database with:
- FDA Food Recalls
- Open Food Facts data (barcode support)
- EPA Fish Advisories (future)
- NOAA Sustainability Ratings (future)
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.db.models import Base, FoodRecall, Source
from app.core.config import settings
from scrapers.fda_recalls_scraper import FDARecallsScraper


async def create_tables(engine):
    """Create all database tables"""
    print("\n🗄️  Creating Milestone 2 tables...")
    async with engine.begin() as conn:
        # Only create new tables (idempotent)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created/verified")


async def add_fda_recalls_source(session: AsyncSession):
    """Add FDA Recalls as a data source"""
    print("\n📚 Adding FDA Recalls data source...")

    # Check if already exists
    result = await session.execute(
        select(Source).where(Source.name == "FDA Food Recalls")
    )
    source = result.scalar_one_or_none()

    if source:
        print("✅ FDA Recalls source already exists")
        return source

    source = Source(
        name="FDA Food Recalls",
        url="https://api.fda.gov/food/enforcement.json",
        source_type="government",
        credibility_score=10,
        last_updated=datetime.now(),
        update_frequency="real-time"
    )

    session.add(source)
    await session.commit()
    await session.refresh(source)

    print("✅ Added FDA Recalls data source")
    return source


async def seed_fda_recalls(session: AsyncSession):
    """Fetch and seed FDA recall data"""
    print("\n📋 Fetching FDA Food Recalls...")

    scraper = FDARecallsScraper()

    try:
        # Fetch recalls from last 180 days
        recalls_data = await scraper.search_recalls_by_product("food")

        if not recalls_data:
            print("⚠️  No recalls found")
            return 0

        print(f"📥 Retrieved {len(recalls_data)} recalls from FDA")

        # Filter to get more recalls
        all_recalls = []

        # Get recalls for common food categories
        categories = ["salad", "meat", "chicken", "beef", "seafood", "cheese", "milk", "eggs"]

        for category in categories:
            category_recalls = await scraper.search_recalls_by_product(category)
            all_recalls.extend(category_recalls)
            print(f"  ├─ {category}: {len(category_recalls)} recalls")

        # Deduplicate by recall_number
        unique_recalls = {}
        for recall in all_recalls:
            recall_num = recall.get("recall_number")
            if recall_num and recall_num not in unique_recalls:
                unique_recalls[recall_num] = recall

        print(f"\n📊 Total unique recalls: {len(unique_recalls)}")

        # Insert into database
        inserted = 0
        skipped = 0

        for recall_data in unique_recalls.values():
            # Check if already exists
            recall_num = recall_data.get("recall_number")
            if not recall_num:
                continue

            result = await session.execute(
                select(FoodRecall).where(FoodRecall.recall_number == recall_num)
            )
            existing = result.scalar_one_or_none()

            if existing:
                skipped += 1
                continue

            # Helper function to truncate strings
            def truncate(value, max_length):
                if value and len(value) > max_length:
                    return value[:max_length-3] + "..."
                return value

            # Get state, filter out invalid values
            state_value = recall_data.get("state")
            if state_value and (len(state_value) != 2 or state_value.lower() == "n/a"):
                state_value = None

            # Create recall record
            recall = FoodRecall(
                recall_number=recall_num[:50] if recall_num else None,
                product_description=recall_data.get("product_description", ""),  # TEXT field, no limit
                reason_for_recall=recall_data.get("reason_for_recall"),  # TEXT field
                recall_date=recall_data.get("recall_date"),
                report_date=recall_data.get("report_date"),
                company_name=truncate(recall_data.get("company_name"), 255),
                distribution_pattern=recall_data.get("distribution_pattern"),  # TEXT field
                product_quantity=truncate(recall_data.get("product_quantity"), 100),
                status=truncate(recall_data.get("status"), 50),
                classification=truncate(recall_data.get("classification"), 20),
                code_info=recall_data.get("code_info"),  # TEXT field
                voluntary_mandated=truncate(recall_data.get("voluntary_mandated"), 50),
                city=truncate(recall_data.get("city"), 100),
                state=state_value,
                country=truncate(recall_data.get("country"), 100),
                event_id=truncate(recall_data.get("event_id"), 50),
            )

            session.add(recall)
            inserted += 1

            # Commit in batches
            if inserted % 50 == 0:
                await session.commit()
                print(f"  ├─ Inserted {inserted} recalls...")

        # Final commit
        await session.commit()

        print(f"\n✅ Seeded {inserted} recalls (skipped {skipped} existing)")

        # Show classification breakdown
        result = await session.execute(select(FoodRecall))
        all_db_recalls = result.scalars().all()

        class_counts = {}
        for recall in all_db_recalls:
            classification = recall.classification or "Unknown"
            class_counts[classification] = class_counts.get(classification, 0) + 1

        print("\n📊 Recalls by Classification:")
        for classification in sorted(class_counts.keys()):
            count = class_counts[classification]
            print(f"  ├─ {classification}: {count}")

        return inserted

    finally:
        await scraper.close()


async def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("🌱 MILESTONE 2 - DATABASE SEEDING")
    print("="*60)

    # Get database URL
    database_url = os.getenv("DATABASE_URL") or settings.DATABASE_URL

    print(f"\n📍 Database: {database_url.split('@')[1] if '@' in database_url else 'local'}")

    # Create engine
    engine = create_async_engine(database_url, echo=False)

    # Create tables
    await create_tables(engine)

    # Create session factory
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Add data sources
        await add_fda_recalls_source(session)

        # Seed FDA recalls
        recalls_count = await seed_fda_recalls(session)

    print("\n" + "="*60)
    print("✅ MILESTONE 2 SEEDING COMPLETE!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"  ├─ FDA Recalls: {recalls_count}")
    print(f"  └─ Total new records: {recalls_count}")
    print("\n🎉 Ready for Milestone 2 features!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
