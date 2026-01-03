import asyncio
import sys
from pathlib import Path

# Add apps/api to path
sys.path.append(str(Path(__file__).parent.parent / "apps" / "api"))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Food

async def inspect():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Food))
        foods = result.scalars().all()
        print(f"Total Foods: {len(foods)}")
        for f in foods:
            print(f" - {f.name} (slug: {f.slug})")

if __name__ == "__main__":
    asyncio.run(inspect())
