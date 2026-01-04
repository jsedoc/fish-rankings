"""
FDA Food Recalls Scraper

Fetches real-time food recall data from FDA's openFDA API.
API Docs: https://open.fda.gov/apis/food/enforcement/

No API key required for < 1000 requests/day
"""

import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FDARecallsScraper:
    """Scraper for FDA Food Recalls using openFDA API"""

    BASE_URL = "https://api.fda.gov/food/enforcement.json"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def fetch_recent_recalls(
        self,
        days: int = 90,
        limit: int = 100
    ) -> List[Dict]:
        """
        Fetch recent food recalls from FDA

        Args:
            days: Number of days back to fetch (default 90)
            limit: Maximum number of recalls to fetch (default 100, max 1000)

        Returns:
            List of recall dictionaries
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Format dates as YYYYMMDD
            date_filter = f"[{start_date.strftime('%Y%m%d')}+TO+{end_date.strftime('%Y%m%d')}]"

            # Build query
            # Search for recalls with report_date in range
            params = {
                "search": f"report_date:{date_filter}",
                "limit": min(limit, 1000),  # FDA limit is 1000
                "sort": "report_date:desc"
            }

            logger.info(f"Fetching FDA recalls from last {days} days...")
            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            logger.info(f"✅ Fetched {len(results)} recalls from FDA")

            # Transform to our format
            recalls = [self._transform_recall(r) for r in results]

            return recalls

        except httpx.HTTPError as e:
            logger.error(f"❌ Error fetching FDA recalls: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return []

    async def search_recalls_by_product(self, product_name: str) -> List[Dict]:
        """
        Search for recalls by product name

        Args:
            product_name: Name or keyword to search for

        Returns:
            List of matching recalls
        """
        try:
            params = {
                "search": f'product_description:"{product_name}"',
                "limit": 100,
                "sort": "report_date:desc"
            }

            logger.info(f"Searching recalls for: {product_name}")
            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            logger.info(f"Found {len(results)} recalls for '{product_name}'")

            recalls = [self._transform_recall(r) for r in results]
            return recalls

        except httpx.HTTPError as e:
            logger.error(f"Error searching recalls: {e}")
            return []

    async def get_recall_by_number(self, recall_number: str) -> Optional[Dict]:
        """
        Get specific recall by recall number

        Args:
            recall_number: FDA recall number (e.g., "F-0000-2024")

        Returns:
            Recall dictionary or None if not found
        """
        try:
            params = {
                "search": f'recall_number:"{recall_number}"',
                "limit": 1
            }

            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            if results:
                return self._transform_recall(results[0])
            return None

        except httpx.HTTPError as e:
            logger.error(f"Error fetching recall {recall_number}: {e}")
            return None

    def _transform_recall(self, raw_recall: Dict) -> Dict:
        """
        Transform FDA API response to our schema

        Args:
            raw_recall: Raw recall data from FDA API

        Returns:
            Transformed recall dictionary
        """
        # Parse date (YYYYMMDD format)
        report_date_str = raw_recall.get("report_date")
        report_date = None
        if report_date_str:
            try:
                report_date = datetime.strptime(report_date_str, "%Y%m%d").date()
            except (ValueError, TypeError):
                pass

        # Get recall date
        recall_initiation_date = raw_recall.get("recall_initiation_date")
        recall_date = None
        if recall_initiation_date:
            try:
                recall_date = datetime.strptime(recall_initiation_date, "%Y%m%d").date()
            except (ValueError, TypeError):
                pass

        return {
            "recall_number": raw_recall.get("recall_number"),
            "product_description": raw_recall.get("product_description"),
            "reason_for_recall": raw_recall.get("reason_for_recall"),
            "recall_date": recall_date,
            "report_date": report_date,
            "company_name": raw_recall.get("recalling_firm"),
            "distribution_pattern": raw_recall.get("distribution_pattern"),
            "product_quantity": raw_recall.get("product_quantity"),
            "status": raw_recall.get("status"),
            "classification": raw_recall.get("classification"),  # Class I, II, or III
            "code_info": raw_recall.get("code_info"),
            "voluntary_mandated": raw_recall.get("voluntary_mandated"),
            "city": raw_recall.get("city"),
            "state": raw_recall.get("state"),
            "country": raw_recall.get("country"),
            "event_id": raw_recall.get("event_id"),
        }

    def categorize_recall_severity(self, classification: str) -> Dict:
        """
        Categorize recall severity based on FDA classification

        Args:
            classification: FDA classification (Class I, II, or III)

        Returns:
            Dictionary with severity info
        """
        severity_map = {
            "Class I": {
                "severity": "critical",
                "color": "red",
                "description": "Dangerous or defective products that could cause serious health problems or death",
                "priority": 1
            },
            "Class II": {
                "severity": "high",
                "color": "orange",
                "description": "Products that might cause temporary health problems or pose risk of serious health problems",
                "priority": 2
            },
            "Class III": {
                "severity": "moderate",
                "color": "yellow",
                "description": "Products unlikely to cause adverse health consequences",
                "priority": 3
            }
        }

        return severity_map.get(classification, {
            "severity": "unknown",
            "color": "gray",
            "description": "Classification unknown",
            "priority": 4
        })


async def test_scraper():
    """Test the FDA Recalls scraper"""
    scraper = FDARecallsScraper()

    try:
        print("\n" + "="*60)
        print("🧪 Testing FDA Recalls Scraper")
        print("="*60 + "\n")

        # Test 1: Fetch recent recalls
        print("📋 Test 1: Fetching recent recalls (last 30 days)...")
        recalls = await scraper.fetch_recent_recalls(days=30, limit=10)
        print(f"✅ Retrieved {len(recalls)} recalls\n")

        if recalls:
            print("📄 Sample recall:")
            sample = recalls[0]
            print(f"  Recall #: {sample.get('recall_number')}")
            print(f"  Product: {sample.get('product_description', '')[:80]}...")
            print(f"  Reason: {sample.get('reason_for_recall', '')[:80]}...")
            print(f"  Company: {sample.get('company_name')}")
            print(f"  Date: {sample.get('recall_date')}")
            print(f"  Status: {sample.get('status')}")
            print(f"  Classification: {sample.get('classification')}")

            # Test severity categorization
            severity = scraper.categorize_recall_severity(sample.get('classification', ''))
            print(f"  Severity: {severity.get('severity')} ({severity.get('description')[:50]}...)")

        print("\n" + "-"*60 + "\n")

        # Test 2: Search by product
        print("🔍 Test 2: Searching for 'salad' recalls...")
        salad_recalls = await scraper.search_recalls_by_product("salad")
        print(f"✅ Found {len(salad_recalls)} salad-related recalls\n")

        if salad_recalls:
            print("📄 Sample salad recall:")
            sample = salad_recalls[0]
            print(f"  Product: {sample.get('product_description', '')[:80]}...")
            print(f"  Reason: {sample.get('reason_for_recall', '')[:80]}...")

        print("\n" + "-"*60 + "\n")

        # Test 3: Statistics
        print("📊 Recall Statistics:")
        if recalls:
            class_counts = {}
            for recall in recalls:
                classification = recall.get('classification', 'Unknown')
                class_counts[classification] = class_counts.get(classification, 0) + 1

            for classification, count in sorted(class_counts.items()):
                print(f"  {classification}: {count} recalls")

        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60 + "\n")

    finally:
        await scraper.close()


if __name__ == "__main__":
    # Run test
    asyncio.run(test_scraper())
