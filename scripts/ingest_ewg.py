import requests
from bs4 import BeautifulSoup
import json
import os
import ssl

# Fix for SSL certificate verify failed
ssl._create_default_https_context = ssl._create_unverified_context

OUTPUT_FILE = "data/ewg_seafood.json"
URL = "https://www.ewg.org/consumer-guides/ewgs-consumer-guide-seafood"

def ingest_ewg_data():
    print(f"Fetching data from {URL}...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = []
        
        # Helper to process sections
        def process_section(header_text, category_name, mercury, omega3, sustainable):
            # Find the header
            header = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4'] and header_text in tag.get_text())
            if not header:
                print(f"Warning: Header '{header_text}' not found")
                return

            # Find the next UL
            # The structure in the chunks showed Header -> Text -> UL or something similar
            # Let's look for the next sibling that is a UL or contains a UL
            
            # Simple traversal: find next UL
            ul = header.find_next('ul')
            if ul:
                for li in ul.find_all('li'):
                    text = li.get_text().strip()
                    # Remove asterisks
                    name = text.replace('*', '').strip()
                    if not name:
                        continue
                        
                    record = {
                        "name": name,
                        "category": category_name,
                        "mercury_level": mercury,
                        "omega_3_level": omega3,
                        "sustainable": sustainable,
                        "source": "EWG"
                    }
                    data.append(record)
            else:
                print(f"Warning: No list found for '{header_text}'")

        # 1. Best Bets
        process_section("Best Bets", "Best Choice", "Low", "Very High", True)
        
        # 2. Good Choices
        process_section("Good Choices", "Good Choice", "Low", "High", False)
        
        # 3. Low Mercury (but low omega-3)
        process_section("Low Mercury", "Low Mercury", "Low", "Low", None)
        
        # 4. Avoid
        process_section("Avoid", "Avoid", "High", None, None)
        
        # Save to JSON
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Successfully saved {len(data)} records to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error ingesting EWG data: {e}")

if __name__ == "__main__":
    ingest_ewg_data()
