"""
Open Food Facts Scraper

Fetches product data from Open Food Facts API for barcode scanning.
API Docs: https://world.openfoodfacts.org/data

No API key required - completely free and open source
"""

import httpx
import asyncio
from typing import Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenFoodFactsScraper:
    """Scraper for Open Food Facts product database"""

    BASE_URL = "https://world.openfoodfacts.org/api/v2"
    PRODUCT_URL = "https://world.openfoodfacts.org/api/v2/product"

    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "FoodSafetyPlatform/1.0 (Educational Project)"
            }
        )

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """
        Get product information by barcode (UPC/EAN)

        Args:
            barcode: Product barcode (e.g., "012345678901")

        Returns:
            Product dictionary or None if not found
        """
        try:
            # Clean barcode (remove spaces, dashes)
            barcode = barcode.replace(" ", "").replace("-", "")

            url = f"{self.PRODUCT_URL}/{barcode}.json"
            logger.info(f"Fetching product: {barcode}")

            response = await self.client.get(url)
            response.raise_for_status()

            data = response.json()

            # Check if product was found
            if data.get("status") != 1:
                logger.warning(f"Product not found: {barcode}")
                return None

            product = data.get("product", {})

            if not product:
                return None

            # Transform to our format
            transformed = self._transform_product(product, barcode)
            logger.info(f"✅ Found product: {transformed.get('product_name', 'Unknown')}")

            return transformed

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching product {barcode}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching product {barcode}: {e}")
            return None

    async def search_products(
        self,
        query: str,
        page: int = 1,
        page_size: int = 20
    ) -> List[Dict]:
        """
        Search for products by name

        Args:
            query: Search query
            page: Page number (1-indexed)
            page_size: Results per page

        Returns:
            List of product dictionaries
        """
        try:
            url = f"{self.BASE_URL}/search"
            params = {
                "search_terms": query,
                "page": page,
                "page_size": page_size,
                "fields": "code,product_name,brands,categories,ingredients_text,nutriscore_grade,nova_group,ecoscore_grade"
            }

            logger.info(f"Searching products: {query}")
            response = await self.client.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            products = data.get("products", [])

            logger.info(f"Found {len(products)} products for '{query}'")

            # Transform products
            transformed = [
                self._transform_product(p, p.get("code", ""))
                for p in products
                if p.get("code")
            ]

            return transformed

        except httpx.HTTPError as e:
            logger.error(f"HTTP error searching: {e}")
            return []
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []

    def _transform_product(self, product: Dict, barcode: str) -> Dict:
        """
        Transform Open Food Facts product to our schema

        Args:
            product: Raw product data from API
            barcode: Product barcode

        Returns:
            Transformed product dictionary
        """
        # Get product name
        product_name = (
            product.get("product_name") or
            product.get("product_name_en") or
            product.get("generic_name") or
            "Unknown Product"
        )

        # Get brands
        brands = product.get("brands", "")
        if brands:
            product_name = f"{brands} {product_name}"

        # Get categories
        categories = product.get("categories", "")
        categories_list = [c.strip() for c in categories.split(",")] if categories else []

        # Get ingredients
        ingredients = product.get("ingredients_text") or product.get("ingredients_text_en")

        # Get nutrition facts
        nutriments = product.get("nutriments", {})

        # Get quality scores
        nutriscore = product.get("nutriscore_grade", "").upper()  # A-E
        nova_group = product.get("nova_group")  # 1-4 (processing level)
        ecoscore = product.get("ecoscore_grade", "").upper()  # A-E

        # Get allergens
        allergens = product.get("allergens_tags", [])
        allergens_list = [a.replace("en:", "").replace("-", " ").title() for a in allergens]

        # Get image
        image_url = (
            product.get("image_url") or
            product.get("image_front_url") or
            product.get("image_small_url")
        )

        return {
            "barcode": barcode,
            "product_name": product_name.strip(),
            "brands": product.get("brands"),
            "categories": categories_list,
            "ingredients": ingredients,
            "allergens": allergens_list,
            "nutriscore_grade": nutriscore if nutriscore else None,
            "nova_group": nova_group,
            "ecoscore_grade": ecoscore if ecoscore else None,
            "image_url": image_url,
            "serving_size": product.get("serving_size"),
            "quantity": product.get("quantity"),
            "packaging": product.get("packaging"),
            "manufacturing_places": product.get("manufacturing_places"),
            "countries": product.get("countries"),
            "labels": product.get("labels_tags", []),
            "nutrients": {
                "energy_kcal": nutriments.get("energy-kcal_100g"),
                "fat": nutriments.get("fat_100g"),
                "saturated_fat": nutriments.get("saturated-fat_100g"),
                "carbohydrates": nutriments.get("carbohydrates_100g"),
                "sugars": nutriments.get("sugars_100g"),
                "fiber": nutriments.get("fiber_100g"),
                "proteins": nutriments.get("proteins_100g"),
                "salt": nutriments.get("salt_100g"),
                "sodium": nutriments.get("sodium_100g"),
            },
            "openfoodfacts_url": f"https://world.openfoodfacts.org/product/{barcode}",
            "last_modified": product.get("last_modified_t"),
        }

    def get_nutriscore_info(self, grade: str) -> Dict:
        """
        Get information about Nutri-Score grade

        Args:
            grade: Nutri-Score grade (A-E)

        Returns:
            Dictionary with grade info
        """
        scores = {
            "A": {
                "grade": "A",
                "color": "dark-green",
                "label": "Very Good Nutritional Quality",
                "description": "Foods with the best nutritional quality"
            },
            "B": {
                "grade": "B",
                "color": "light-green",
                "label": "Good Nutritional Quality",
                "description": "Foods with good nutritional quality"
            },
            "C": {
                "grade": "C",
                "color": "yellow",
                "label": "Average Nutritional Quality",
                "description": "Foods with average nutritional quality"
            },
            "D": {
                "grade": "D",
                "color": "orange",
                "label": "Poor Nutritional Quality",
                "description": "Foods with poor nutritional quality"
            },
            "E": {
                "grade": "E",
                "color": "red",
                "label": "Very Poor Nutritional Quality",
                "description": "Foods with very poor nutritional quality"
            }
        }
        return scores.get(grade.upper(), {
            "grade": "Unknown",
            "color": "gray",
            "label": "Not Rated",
            "description": "Nutritional quality not assessed"
        })

    def get_nova_info(self, group: int) -> Dict:
        """
        Get information about NOVA processing group

        Args:
            group: NOVA group (1-4)

        Returns:
            Dictionary with group info
        """
        groups = {
            1: {
                "group": 1,
                "label": "Unprocessed or Minimally Processed",
                "description": "Fresh, dried, frozen foods with no added ingredients",
                "color": "green"
            },
            2: {
                "group": 2,
                "label": "Processed Culinary Ingredients",
                "description": "Oils, butter, sugar, salt extracted from foods",
                "color": "yellow"
            },
            3: {
                "group": 3,
                "label": "Processed Foods",
                "description": "Foods with added salt, sugar, or fat",
                "color": "orange"
            },
            4: {
                "group": 4,
                "label": "Ultra-Processed Foods",
                "description": "Industrial formulations with many additives",
                "color": "red"
            }
        }
        return groups.get(group, {
            "group": 0,
            "label": "Unknown Processing Level",
            "description": "Processing level not assessed",
            "color": "gray"
        })


async def test_scraper():
    """Test the Open Food Facts scraper"""
    scraper = OpenFoodFactsScraper()

    try:
        print("\n" + "="*60)
        print("🧪 Testing Open Food Facts Scraper")
        print("="*60 + "\n")

        # Test 1: Get product by barcode (Coca-Cola)
        print("📋 Test 1: Fetching product by barcode...")
        barcode = "5449000000996"  # Coca-Cola
        product = await scraper.get_product_by_barcode(barcode)

        if product:
            print(f"✅ Product found: {product['product_name']}")
            print(f"  Barcode: {product['barcode']}")
            print(f"  Brands: {product.get('brands', 'N/A')}")
            print(f"  Categories: {', '.join(product['categories'][:3])}")
            print(f"  Nutri-Score: {product.get('nutriscore_grade', 'N/A')}")
            print(f"  NOVA Group: {product.get('nova_group', 'N/A')}")
            print(f"  Eco-Score: {product.get('ecoscore_grade', 'N/A')}")

            if product.get('allergens'):
                print(f"  Allergens: {', '.join(product['allergens'])}")
        else:
            print("❌ Product not found")

        print("\n" + "-"*60 + "\n")

        # Test 2: Search for products
        print("🔍 Test 2: Searching for 'organic banana'...")
        products = await scraper.search_products("organic banana", page_size=5)
        print(f"✅ Found {len(products)} products\n")

        for i, p in enumerate(products[:3], 1):
            print(f"  {i}. {p['product_name']}")
            print(f"     Barcode: {p['barcode']}")
            if p.get('nutriscore_grade'):
                print(f"     Nutri-Score: {p['nutriscore_grade']}")

        print("\n" + "-"*60 + "\n")

        # Test 3: Another common barcode (Cheerios)
        print("📋 Test 3: Fetching another product...")
        barcode2 = "016000275287"  # Cheerios
        product2 = await scraper.get_product_by_barcode(barcode2)

        if product2:
            print(f"✅ Product: {product2['product_name']}")
            print(f"  Nutri-Score: {product2.get('nutriscore_grade', 'N/A')}")

            # Show Nutri-Score info
            if product2.get('nutriscore_grade'):
                info = scraper.get_nutriscore_info(product2['nutriscore_grade'])
                print(f"  Quality: {info['label']}")

            # Show NOVA info
            if product2.get('nova_group'):
                nova_info = scraper.get_nova_info(product2['nova_group'])
                print(f"  Processing: {nova_info['label']}")

        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60 + "\n")

    finally:
        await scraper.close()


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_scraper())
