"""
Food Safety Platform - Data Scrapers Package

This package contains all scrapers for fetching food safety data from various sources.
Scrapers are shared between the API application and standalone scripts.
"""

from .fda_fish_scraper import scrape_fda_fish_data, scrape_fda_detailed_mercury
from .ewg_produce_scraper import scrape_ewg_produce
from .pubmed_scraper import collect_food_safety_papers
from .usda_api_client import get_nutrition_for_common_foods
from .openfoodfacts_scraper import OpenFoodFactsScraper
from .fda_recalls_scraper import FDARecallsScraper
from .epa_advisories_scraper import EPAAdvisoriesScraper
from .noaa_fishwatch_scraper import NOAAFishWatchScraper

__all__ = [
    'scrape_fda_fish_data',
    'scrape_fda_detailed_mercury',
    'scrape_ewg_produce',
    'collect_food_safety_papers',
    'get_nutrition_for_common_foods',
    'OpenFoodFactsScraper',
    'FDARecallsScraper',
    'EPAAdvisoriesScraper',
    'NOAAFishWatchScraper',
]
