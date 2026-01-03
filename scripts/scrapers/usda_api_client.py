"""
USDA FoodData Central API Client
Free nutritional data for foods
No API key required for basic usage
"""
import httpx
from typing import List, Dict, Optional
import asyncio
import json

USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
USDA_FOOD_URL = "https://api.nal.usda.gov/fdc/v1/food"

# Note: USDA API doesn't strictly require a key for basic searches,
# but it's recommended to get one (free) for higher rate limits
# Get one at: https://fdc.nal.usda.gov/api-key-signup.html

async def search_usda_food(query: str, page_size: int = 50) -> List[Dict]:
    """
    Search USDA FoodData Central for foods
    """
    print(f"🌽 Searching USDA for: {query}")

    params = {
        "query": query,
        "pageSize": page_size,
        "dataType": ["Survey (FNDDS)", "Foundation", "SR Legacy"],  # Most comprehensive
    }

    # Add API key if available (optional)
    # params["api_key"] = "YOUR_API_KEY"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(USDA_SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                print("⚠️  USDA API requires an API key. Get one at: https://fdc.nal.usda.gov/api-key-signup.html")
                return []
            raise

    foods = data.get("foods", [])
    print(f"  Found {len(foods)} foods")

    return foods


async def get_usda_food_details(fdc_id: int) -> Optional[Dict]:
    """
    Get detailed nutritional information for a specific food
    """
    url = f"{USDA_FOOD_URL}/{fdc_id}"

    # params = {"api_key": "YOUR_API_KEY"}  # Add if you have one

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except:
            return None


async def get_nutrition_for_common_foods() -> List[Dict]:
    """
    Get nutritional data for common foods
    Returns simplified nutrition data
    """
    print("🍎 Fetching nutrition data for common foods...")

    common_foods = [
        "chicken breast", "salmon", "spinach", "broccoli", "apple",
        "banana", "rice", "potato", "milk", "eggs", "beef", "pork",
        "carrots", "tomatoes", "onions", "garlic", "olive oil"
    ]

    all_nutrition = []

    for food_name in common_foods:
        results = await search_usda_food(food_name, page_size=1)

        if results:
            food = results[0]
            nutrients = {}

            # Extract key nutrients
            for nutrient in food.get("foodNutrients", []):
                name = nutrient.get("nutrientName", "")
                value = nutrient.get("value", 0)
                unit = nutrient.get("unitName", "")

                # Only keep important nutrients
                important = [
                    "Protein", "Total lipid (fat)", "Carbohydrate",
                    "Energy", "Fiber", "Sugars",
                    "Calcium", "Iron", "Magnesium", "Phosphorus", "Potassium",
                    "Sodium", "Zinc", "Vitamin C", "Vitamin A", "Vitamin D"
                ]

                if any(imp in name for imp in important):
                    nutrients[name] = {"value": value, "unit": unit}

            all_nutrition.append({
                "name": food.get("description", food_name),
                "fdc_id": food.get("fdcId"),
                "category": food.get("foodCategory", ""),
                "nutrients": nutrients
            })

        await asyncio.sleep(0.3)  # Be polite to API

    print(f"✅ Collected nutrition data for {len(all_nutrition)} foods")
    return all_nutrition


if __name__ == "__main__":
    # Test the client
    data = asyncio.run(get_nutrition_for_common_foods())
    print(f"\nCollected {len(data)} foods with nutrition data")
    if data:
        print(f"\nSample: {data[0]['name']}")
        print(f"Nutrients: {list(data[0]['nutrients'].keys())[:5]}")
