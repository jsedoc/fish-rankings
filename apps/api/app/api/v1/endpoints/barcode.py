"""
API endpoints for barcode scanning and product lookup
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional
import logging

from app.db.session import get_db
from app.db.models import Food, FoodCategory, FoodRecall
from scrapers.openfoodfacts_scraper import OpenFoodFactsScraper

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/lookup/{barcode}")
async def lookup_barcode(
    barcode: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Look up a product by barcode

    This endpoint:
    1. Checks if the product exists in our database
    2. If not, fetches from Open Food Facts
    3. Checks for any recalls related to the product
    4. Returns comprehensive food safety information

    - **barcode**: UPC/EAN barcode (e.g., "5449000000996")
    """
    try:
        # Clean barcode
        barcode = barcode.replace(" ", "").replace("-", "")

        # Check if product exists in our database
        query = select(Food).where(Food.barcode == barcode)
        result = await db.execute(query)
        food = result.scalar_one_or_none()

        if food:
            logger.info(f"Found product in database: {food.name}")

            # Check for recalls
            recall_query = select(FoodRecall).where(
                or_(
                    FoodRecall.food_id == food.id,
                    FoodRecall.product_description.ilike(f"%{food.name}%")
                )
            ).limit(5)
            recall_result = await db.execute(recall_query)
            recalls = recall_result.scalars().all()

            return {
                "source": "database",
                "found": True,
                "product": {
                    "id": str(food.id),
                    "name": food.name,
                    "slug": food.slug,
                    "barcode": food.barcode,
                    "category": food.category.name if food.category else None,
                    "description": food.description,
                    "image_url": food.image_url,
                },
                "recalls": [
                    {
                        "recall_number": r.recall_number,
                        "reason": r.reason_for_recall,
                        "classification": r.classification,
                        "date": r.recall_date.isoformat() if r.recall_date else None,
                    }
                    for r in recalls
                ],
                "recall_count": len(recalls),
                "has_active_recalls": len(recalls) > 0
            }

        # Product not in our database - fetch from Open Food Facts
        logger.info(f"Fetching from Open Food Facts: {barcode}")
        scraper = OpenFoodFactsScraper()

        try:
            product_data = await scraper.get_product_by_barcode(barcode)

            if not product_data:
                return {
                    "source": "openfoodfacts",
                    "found": False,
                    "barcode": barcode,
                    "message": "Product not found in Open Food Facts database"
                }

            # Check for recalls by product name
            product_name = product_data.get("product_name", "")
            recall_query = select(FoodRecall).where(
                FoodRecall.product_description.ilike(f"%{product_name}%")
            ).limit(5)
            recall_result = await db.execute(recall_query)
            recalls = recall_result.scalars().all()

            return {
                "source": "openfoodfacts",
                "found": True,
                "product": {
                    "name": product_data.get("product_name"),
                    "barcode": product_data.get("barcode"),
                    "brands": product_data.get("brands"),
                    "categories": product_data.get("categories", []),
                    "ingredients": product_data.get("ingredients"),
                    "allergens": product_data.get("allergens", []),
                    "nutriscore_grade": product_data.get("nutriscore_grade"),
                    "nova_group": product_data.get("nova_group"),
                    "ecoscore_grade": product_data.get("ecoscore_grade"),
                    "image_url": product_data.get("image_url"),
                    "nutrients": product_data.get("nutrients", {}),
                    "openfoodfacts_url": product_data.get("openfoodfacts_url"),
                },
                "recalls": [
                    {
                        "recall_number": r.recall_number,
                        "reason": r.reason_for_recall,
                        "classification": r.classification,
                        "date": r.recall_date.isoformat() if r.recall_date else None,
                    }
                    for r in recalls
                ],
                "recall_count": len(recalls),
                "has_active_recalls": len(recalls) > 0,
                "can_import": True,
                "message": "Product found in Open Food Facts. You can import it to our database."
            }

        finally:
            await scraper.close()

    except Exception as e:
        logger.error(f"Error looking up barcode {barcode}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_products(
    q: str = Query(..., min_length=2, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50)
):
    """
    Search for products in Open Food Facts

    - **q**: Search query (minimum 2 characters)
    - **page**: Page number (default: 1)
    - **page_size**: Results per page (default: 10, max: 50)
    """
    try:
        scraper = OpenFoodFactsScraper()

        try:
            products = await scraper.search_products(q, page=page, page_size=page_size)

            return {
                "query": q,
                "page": page,
                "page_size": page_size,
                "results": products,
                "count": len(products)
            }

        finally:
            await scraper.close()

    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/{barcode}")
async def import_product(
    barcode: str,
    category_id: Optional[int] = Query(None, description="Food category ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Import a product from Open Food Facts into our database

    - **barcode**: Product barcode
    - **category_id**: Optional category ID to assign
    """
    try:
        # Clean barcode
        barcode = barcode.replace(" ", "").replace("-", "")

        # Check if already exists
        query = select(Food).where(Food.barcode == barcode)
        result = await db.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            return {
                "success": False,
                "message": f"Product already exists in database: {existing.name}",
                "food_id": str(existing.id)
            }

        # Fetch from Open Food Facts
        scraper = OpenFoodFactsScraper()

        try:
            product_data = await scraper.get_product_by_barcode(barcode)

            if not product_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {barcode} not found in Open Food Facts"
                )

            # Create slug
            from slugify import slugify
            product_name = product_data.get("product_name", "")
            slug = slugify(product_name) if product_name else barcode

            # Make slug unique
            base_slug = slug
            counter = 1
            while True:
                check_query = select(Food).where(Food.slug == slug)
                check_result = await db.execute(check_query)
                if not check_result.scalar_one_or_none():
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1

            # Create food entry
            food = Food(
                name=product_name,
                barcode=barcode,
                slug=slug,
                description=product_data.get("ingredients"),
                image_url=product_data.get("image_url"),
                category_id=category_id
            )

            db.add(food)
            await db.commit()
            await db.refresh(food)

            logger.info(f"Imported product: {product_name}")

            return {
                "success": True,
                "message": f"Successfully imported: {product_name}",
                "food_id": str(food.id),
                "slug": food.slug,
                "product": {
                    "name": food.name,
                    "barcode": food.barcode,
                    "slug": food.slug,
                    "image_url": food.image_url
                }
            }

        finally:
            await scraper.close()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error importing product {barcode}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info/nutriscore/{grade}")
async def get_nutriscore_info(grade: str):
    """
    Get information about a Nutri-Score grade

    - **grade**: Nutri-Score grade (A, B, C, D, or E)
    """
    scraper = OpenFoodFactsScraper()
    info = scraper.get_nutriscore_info(grade)
    await scraper.close()
    return info


@router.get("/info/nova/{group}")
async def get_nova_info(group: int):
    """
    Get information about a NOVA processing group

    - **group**: NOVA group (1-4)
    """
    if group < 1 or group > 4:
        raise HTTPException(status_code=400, detail="NOVA group must be between 1 and 4")

    scraper = OpenFoodFactsScraper()
    info = scraper.get_nova_info(group)
    await scraper.close()
    return info
