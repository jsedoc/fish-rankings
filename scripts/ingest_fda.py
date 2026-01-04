import pandas as pd
import json
import os
import ssl

# Fix for SSL certificate verify failed
ssl._create_default_https_context = ssl._create_unverified_context

OUTPUT_FILE = "data/fda_mercury_1990_2012.json"
URL = "https://www.fda.gov/food/environmental-contaminants-food/mercury-levels-commercial-fish-and-shellfish-1990-2012"

def ingest_fda_data():
    print(f"Fetching data from {URL}...")
    try:
        tables = pd.read_html(URL)
        if not tables:
            print("No tables found!")
            return

        df = tables[0]
        
        # The table has a MultiIndex header. We need to flatten it.
        # Level 0: Species, Mercury Concentration (PPM), ...
        # Level 1: Species, Mean, Median, Min, Max, ...
        
        # Let's clean up columns
        # Expected structure might vary, so let's inspect and flatten safely
        if isinstance(df.columns, pd.MultiIndex):
            # Flatten columns: join levels with '_' if not empty
            df.columns = ['_'.join(col).strip() for col in df.columns.values]
        
        # Now identify relevant columns. 
        # Typically: 'Species_Species', 'Mercury Concentration (PPM)_Mean', 'Mercury Concentration (PPM)_Median', ...
        
        print("Columns found:", df.columns.tolist())
        
        # Rename for consistency
        # finding the column that contains 'Species' (case insensitive)
        species_col = next((c for c in df.columns if 'SPECIES' in c.upper()), None)
        mean_col = next((c for c in df.columns if 'MEAN' in c.upper()), None)
        
        if not species_col or not mean_col:
            print(f"Could not identify required columns. Found: {df.columns.tolist()}")
            return

        # Select and rename
        df_clean = df[[species_col, mean_col]].copy()
        df_clean.columns = ['name', 'mercury_mean_ppm']
        
        # Clean data
        # Remove "ND" (Non-Detect) and convert to float
        def clean_ppm(val):
            if str(val).upper() == 'ND':
                return 0.0
            try:
                return float(val)
            except ValueError:
                return None

        df_clean['mercury_mean_ppm'] = df_clean['mercury_mean_ppm'].apply(clean_ppm)
        
        # Clean species names
        df_clean['name'] = df_clean['name'].str.title().str.strip()
        
        # Add source metadata
        df_clean['source'] = "FDA"
        df_clean['year_range'] = "1990-2012"
        
        # Drop invalid rows
        df_clean = df_clean.dropna(subset=['mercury_mean_ppm'])
        
        # Convert to list of dicts
        records = df_clean.to_dict(orient='records')
        
        # Save to JSON
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(records, f, indent=2)
            
        print(f"Successfully saved {len(records)} records to {OUTPUT_FILE}")
        
        # Print sample
        print("Sample data:")
        print(df_clean.head())

    except Exception as e:
        print(f"Error ingesting FDA data: {e}")

if __name__ == "__main__":
    ingest_fda_data()
