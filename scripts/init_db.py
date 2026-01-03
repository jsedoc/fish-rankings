"""Database initialization script."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models import Base, Source, FishSpecies, ContaminantLevel, NutrientLevel, SafetyRating
from src.config import get_settings

settings = get_settings()


async def init_database():
    """Initialize the database with tables and sample data."""
    engine = create_async_engine(
        settings.database_url,
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
        # Add sources
        ewg_source = Source(
            name="EWG Shopper's Guide",
            url="https://www.ewg.org/consumer-guides/ewgs-consumer-guide-seafood",
            description="Environmental Working Group's Consumer Guide to Seafood"
        )
        
        fda_source = Source(
            name="FDA Fish Advice",
            url="https://www.fda.gov/food/consumers/advice-about-eating-fish",
            description="FDA and EPA advice about eating fish and shellfish"
        )
        
        session.add_all([ewg_source, fda_source])
        await session.commit()

        # Add fish species with comprehensive data
        fish_data = [
            {
                "name": "Wild Salmon",
                "scientific_name": "Oncorhynchus spp.",
                "description": "Wild-caught Pacific salmon, including varieties like Sockeye, Coho, and King salmon",
                "source": ewg_source,
                "contaminants": [
                    {"name": "Mercury", "level": 0.014, "unit": "ppm", "safety_threshold": 0.3},
                    {"name": "PCBs", "level": 2.0, "unit": "ppb", "safety_threshold": 2000.0},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 1.8, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 25.0, "unit": "g", "per_serving": "100g"},
                    {"name": "Vitamin D", "amount": 11.0, "unit": "mcg", "per_serving": "100g"},
                ],
                "rating": {
                    "overall_score": 95,
                    "safety_score": 95,
                    "nutrition_score": 98,
                    "sustainability_score": 92,
                    "recommendation": "Best Choice",
                    "notes": "Excellent source of omega-3s with low contaminant levels"
                }
            },
            {
                "name": "Sardines",
                "scientific_name": "Sardina pilchardus",
                "description": "Small, oily fish packed with nutrients",
                "source": ewg_source,
                "contaminants": [
                    {"name": "Mercury", "level": 0.013, "unit": "ppm", "safety_threshold": 0.3},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 1.5, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 25.0, "unit": "g", "per_serving": "100g"},
                    {"name": "Calcium", "amount": 382.0, "unit": "mg", "per_serving": "100g"},
                    {"name": "Vitamin B12", "amount": 8.9, "unit": "mcg", "per_serving": "100g"},
                ],
                "rating": {
                    "overall_score": 98,
                    "safety_score": 98,
                    "nutrition_score": 99,
                    "sustainability_score": 97,
                    "recommendation": "Best Choice",
                    "notes": "Among the healthiest fish choices with exceptional nutrient density"
                }
            },
            {
                "name": "Atlantic Mackerel",
                "scientific_name": "Scomber scombrus",
                "description": "Oily fish rich in omega-3 fatty acids",
                "source": ewg_source,
                "contaminants": [
                    {"name": "Mercury", "level": 0.050, "unit": "ppm", "safety_threshold": 0.3},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 2.6, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 19.0, "unit": "g", "per_serving": "100g"},
                    {"name": "Vitamin B12", "amount": 8.7, "unit": "mcg", "per_serving": "100g"},
                ],
                "rating": {
                    "overall_score": 92,
                    "safety_score": 90,
                    "nutrition_score": 96,
                    "sustainability_score": 90,
                    "recommendation": "Best Choice",
                    "notes": "High in omega-3s with acceptable mercury levels"
                }
            },
            {
                "name": "Farmed Rainbow Trout",
                "scientific_name": "Oncorhynchus mykiss",
                "description": "Freshwater fish typically farmed in the US",
                "source": fda_source,
                "contaminants": [
                    {"name": "Mercury", "level": 0.071, "unit": "ppm", "safety_threshold": 0.3},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 0.98, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 20.5, "unit": "g", "per_serving": "100g"},
                ],
                "rating": {
                    "overall_score": 85,
                    "safety_score": 85,
                    "nutrition_score": 88,
                    "sustainability_score": 82,
                    "recommendation": "Good Choice",
                    "notes": "Good nutritional profile with moderate environmental impact"
                }
            },
            {
                "name": "Albacore Tuna",
                "scientific_name": "Thunnus alalunga",
                "description": "White tuna with higher mercury levels than light tuna",
                "source": fda_source,
                "contaminants": [
                    {"name": "Mercury", "level": 0.350, "unit": "ppm", "safety_threshold": 0.3},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 1.5, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 30.0, "unit": "g", "per_serving": "100g"},
                ],
                "rating": {
                    "overall_score": 65,
                    "safety_score": 55,
                    "nutrition_score": 80,
                    "sustainability_score": 60,
                    "recommendation": "Moderate Consumption",
                    "notes": "Limit consumption due to elevated mercury levels"
                }
            },
            {
                "name": "King Mackerel",
                "scientific_name": "Scomberomorus cavalla",
                "description": "Large mackerel species with high mercury content",
                "source": fda_source,
                "contaminants": [
                    {"name": "Mercury", "level": 0.730, "unit": "ppm", "safety_threshold": 0.3},
                ],
                "nutrients": [
                    {"name": "Omega-3", "amount": 2.2, "unit": "g", "per_serving": "100g"},
                    {"name": "Protein", "amount": 21.0, "unit": "g", "per_serving": "100g"},
                ],
                "rating": {
                    "overall_score": 35,
                    "safety_score": 25,
                    "nutrition_score": 70,
                    "sustainability_score": 40,
                    "recommendation": "Avoid",
                    "notes": "High mercury levels make this fish unsuitable for regular consumption"
                }
            },
        ]

        # Create fish species with related data
        for fish in fish_data:
            species = FishSpecies(
                name=fish["name"],
                scientific_name=fish["scientific_name"],
                description=fish["description"],
                source_id=fish["source"].id
            )
            session.add(species)
            await session.flush()  # Get the species ID

            # Add contaminants
            for cont in fish["contaminants"]:
                contaminant = ContaminantLevel(
                    fish_species_id=species.id,
                    contaminant_name=cont["name"],
                    level=cont["level"],
                    unit=cont["unit"],
                    safety_threshold=cont["safety_threshold"]
                )
                session.add(contaminant)

            # Add nutrients
            for nutr in fish["nutrients"]:
                nutrient = NutrientLevel(
                    fish_species_id=species.id,
                    nutrient_name=nutr["name"],
                    amount=nutr["amount"],
                    unit=nutr["unit"],
                    per_serving=nutr["per_serving"]
                )
                session.add(nutrient)

            # Add rating
            rating = SafetyRating(
                fish_species_id=species.id,
                source_id=fish["source"].id,
                overall_score=fish["rating"]["overall_score"],
                safety_score=fish["rating"]["safety_score"],
                nutrition_score=fish["rating"]["nutrition_score"],
                sustainability_score=fish["rating"]["sustainability_score"],
                recommendation=fish["rating"]["recommendation"],
                notes=fish["rating"]["notes"]
            )
            session.add(rating)

        await session.commit()

        # Verify data was added
        result = await session.execute(select(Source).where(Source.name == "EWG Shopper's Guide"))
        ewg = result.scalar_one_or_none()
        print(f"\nAdded source: {ewg.name}")

        result = await session.execute(select(FishSpecies))
        species_list = result.scalars().all()
        print(f"\nAdded {len(species_list)} fish species:")
        for species in species_list:
            print(f"  - {species.name}")

    await engine.dispose()
    print("\nDatabase initialization complete!")


if __name__ == "__main__":
    asyncio.run(init_database())
