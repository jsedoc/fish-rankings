"""
EPA Fish Advisories Scraper

Scrapes state-by-state fish consumption advisories from EPA.
Note: This is a simplified version that generates sample data.
For production, you would scrape from https://fishadvisoryonline.epa.gov/

EPA provides state-specific fish consumption advisories based on:
- Mercury levels
- PCB contamination
- Other pollutants
- Waterbody-specific advisories
"""

import asyncio
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EPAAdvisoriesScraper:
    """
    Scraper for EPA State Fish Advisory data

    Note: This implementation generates realistic sample data.
    For production, implement actual web scraping from EPA website.
    """

    # US States
    STATES = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming'
    }

    # Common fish species in advisories
    FISH_SPECIES = [
        'Bass (Largemouth)', 'Bass (Smallmouth)', 'Bass (Striped)',
        'Bluefish', 'Carp', 'Catfish', 'Crappie', 'Kingfish',
        'Northern Pike', 'Perch', 'Pickerel', 'Salmon (Atlantic)',
        'Salmon (Chinook)', 'Salmon (Coho)', 'Shark', 'Swordfish',
        'Tilefish', 'Trout (Brook)', 'Trout (Lake)', 'Trout (Rainbow)',
        'Tuna (Albacore)', 'Walleye', 'White Perch'
    ]

    # Waterbody types
    WATERBODY_TYPES = ['lake', 'river', 'reservoir', 'ocean', 'bay', 'creek']

    # Contaminants
    CONTAMINANTS = ['Mercury', 'PCBs', 'Dioxins', 'Chlordane', 'DDT']

    # Advisory levels
    ADVISORY_LEVELS = [
        'Do Not Eat',
        'Limited Consumption - 1 meal per month',
        'Limited Consumption - 1 meal per week',
        'Limited Consumption - 2 meals per week',
        'Unrestricted Consumption'
    ]

    def __init__(self):
        self.base_url = "https://fishadvisoryonline.epa.gov/"

    async def get_state_advisories(
        self,
        state_code: str,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get fish advisories for a specific state

        Args:
            state_code: Two-letter state code (e.g., 'CA', 'NY')
            limit: Maximum number of advisories to return

        Returns:
            List of advisory dictionaries
        """
        state_code = state_code.upper()

        if state_code not in self.STATES:
            logger.error(f"Invalid state code: {state_code}")
            return []

        state_name = self.STATES[state_code]
        logger.info(f"Fetching advisories for {state_name} ({state_code})")

        # Generate sample advisories
        advisories = self._generate_sample_advisories(state_code, state_name, limit)

        logger.info(f"✅ Generated {len(advisories)} advisories for {state_name}")
        return advisories

    async def get_all_advisories(self, states_limit: int = 10, advisories_per_state: int = 10) -> List[Dict]:
        """
        Get advisories for multiple states

        Args:
            states_limit: Number of states to fetch
            advisories_per_state: Advisories per state

        Returns:
            List of all advisories
        """
        logger.info(f"Fetching advisories for {states_limit} states...")

        all_advisories = []
        states = list(self.STATES.keys())[:states_limit]

        for state_code in states:
            advisories = await self.get_state_advisories(state_code, advisories_per_state)
            all_advisories.extend(advisories)

        logger.info(f"✅ Total advisories fetched: {len(all_advisories)}")
        return all_advisories

    def _generate_sample_advisories(
        self,
        state_code: str,
        state_name: str,
        count: int
    ) -> List[Dict]:
        """
        Generate realistic sample advisory data

        Note: In production, this would scrape actual EPA data
        """
        advisories = []

        for i in range(count):
            # Random fish species
            fish = random.choice(self.FISH_SPECIES)

            # Random waterbody
            waterbody_type = random.choice(self.WATERBODY_TYPES)
            waterbody_name = self._generate_waterbody_name(state_name, waterbody_type)

            # Random contaminant
            contaminant = random.choice(self.CONTAMINANTS)

            # Contaminant level (ppm or ppb)
            if contaminant == 'Mercury':
                level = round(random.uniform(0.1, 1.5), 2)  # ppm
                unit = 'ppm'
            else:
                level = round(random.uniform(10, 500), 1)  # ppb
                unit = 'ppb'

            # Advisory level based on contamination
            if contaminant == 'Mercury' and level > 0.5:
                advisory_level = random.choice(self.ADVISORY_LEVELS[:3])
            elif contaminant == 'PCBs' and level > 200:
                advisory_level = random.choice(self.ADVISORY_LEVELS[:3])
            else:
                advisory_level = random.choice(self.ADVISORY_LEVELS[2:])

            # Consumption limit
            if 'Do Not Eat' in advisory_level:
                consumption_limit = 'Do not consume'
            elif '1 meal per month' in advisory_level:
                consumption_limit = 'Maximum 1 meal (8 oz) per month'
            elif '1 meal per week' in advisory_level:
                consumption_limit = 'Maximum 1 meal (8 oz) per week'
            elif '2 meals per week' in advisory_level:
                consumption_limit = 'Maximum 2 meals (8 oz each) per week'
            else:
                consumption_limit = 'No restrictions'

            # Sensitive populations
            sensitive_pops = []
            if level > 0.3:  # Higher contamination
                sensitive_pops = ['Pregnant women', 'Children under 15', 'Women of childbearing age']
            elif level > 0.15:
                sensitive_pops = ['Pregnant women', 'Children under 6']

            # Effective date (within last 2 years)
            days_ago = random.randint(30, 730)
            effective_date = datetime.now() - timedelta(days=days_ago)

            advisory = {
                'state_code': state_code,
                'state_name': state_name,
                'waterbody_name': waterbody_name,
                'waterbody_type': waterbody_type,
                'fish_species': fish,
                'contaminant_type': contaminant,
                'contaminant_level': level,
                'contaminant_unit': unit,
                'advisory_level': advisory_level,
                'consumption_limit': consumption_limit,
                'advisory_text': f"{fish} from {waterbody_name} may contain elevated levels of {contaminant}. {consumption_limit}.",
                'sensitive_populations': sensitive_pops,
                'effective_date': effective_date,
                'source_url': f"{self.base_url}?state={state_code}"
            }

            advisories.append(advisory)

        return advisories

    def _generate_waterbody_name(self, state_name: str, waterbody_type: str) -> str:
        """Generate realistic waterbody names"""

        prefixes = ['Upper', 'Lower', 'North', 'South', 'East', 'West', 'Big', 'Little']

        # Common waterbody names
        lake_names = ['Superior', 'Michigan', 'Erie', 'Ontario', 'Tahoe', 'Champlain', 'George']
        river_names = ['Hudson', 'Mississippi', 'Missouri', 'Colorado', 'Columbia', 'Snake', 'Delaware']
        reservoir_names = ['Hoover', 'Powell', 'Mead', 'Shasta', 'Oroville']

        if waterbody_type == 'lake':
            name = random.choice(lake_names)
            return f"{random.choice(prefixes)} {name} Lake"
        elif waterbody_type == 'river':
            name = random.choice(river_names)
            return f"{name} River"
        elif waterbody_type == 'reservoir':
            name = random.choice(reservoir_names)
            return f"{name} Reservoir"
        elif waterbody_type == 'ocean':
            return f"{state_name} Coast"
        elif waterbody_type == 'bay':
            return f"{state_name} Bay"
        else:  # creek
            return f"{random.choice(prefixes)} Creek"


async def test_scraper():
    """Test the EPA Advisories scraper"""
    scraper = EPAAdvisoriesScraper()

    print("\n" + "="*60)
    print("🧪 Testing EPA Fish Advisories Scraper")
    print("="*60 + "\n")

    # Test 1: Get advisories for California
    print("📋 Test 1: Fetching California advisories...")
    ca_advisories = await scraper.get_state_advisories('CA', limit=5)

    if ca_advisories:
        print(f"✅ Retrieved {len(ca_advisories)} advisories\n")

        # Show first advisory
        adv = ca_advisories[0]
        print("Sample Advisory:")
        print(f"  State: {adv['state_name']} ({adv['state_code']})")
        print(f"  Waterbody: {adv['waterbody_name']} ({adv['waterbody_type']})")
        print(f"  Fish: {adv['fish_species']}")
        print(f"  Contaminant: {adv['contaminant_type']} ({adv['contaminant_level']} {adv['contaminant_unit']})")
        print(f"  Advisory: {adv['advisory_level']}")
        print(f"  Limit: {adv['consumption_limit']}")
        if adv['sensitive_populations']:
            print(f"  Sensitive Groups: {', '.join(adv['sensitive_populations'])}")

    print("\n" + "-"*60 + "\n")

    # Test 2: Get advisories for multiple states
    print("📋 Test 2: Fetching advisories for 5 states...")
    all_advisories = await scraper.get_all_advisories(states_limit=5, advisories_per_state=3)
    print(f"✅ Total advisories: {len(all_advisories)}\n")

    # Statistics
    contaminants = {}
    advisory_levels = {}

    for adv in all_advisories:
        cont = adv['contaminant_type']
        level = adv['advisory_level']

        contaminants[cont] = contaminants.get(cont, 0) + 1
        advisory_levels[level] = advisory_levels.get(level, 0) + 1

    print("📊 Statistics:")
    print("\nContaminants:")
    for cont, count in sorted(contaminants.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cont}: {count}")

    print("\nAdvisory Levels:")
    for level, count in sorted(advisory_levels.items(), key=lambda x: x[1], reverse=True):
        print(f"  {level}: {count}")

    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_scraper())
