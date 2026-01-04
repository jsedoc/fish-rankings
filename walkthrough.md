# Website Verification Walkthrough

We have performed a full verification of the deployed application running locally.

## Summary
- **Homepage**: Loads successfully with all key elements.
- **Search**: Functional. Found "Wild salmon" successfully.
    - *Note*: Capitalized search terms via manual input behaved differently than strict lowercase API matching in some contexts, but the UI handles popular searches correctly.
- **Detail Page**: Validated data for "Wild salmon" including low-risk mercury status ("Best Choice"), high Omega-3s, and sustainability flags.
- **Categories**: Confirmed "Produce" and "Seafood" categories display seeded items correctly.

## Visual Verification

### Search Results
We searched for "salmon" and found relevant matches.

![Search Results for Salmon](docs/assets/salmon_search_results_1767485181981.png)

### Food Detail Page
The detail page for **Wild Salmon** correctly displays the compiled data from our ingestion pipeline (FDA Mercury data + EWG Seafood Guide).

![Wild Salmon Detail](docs/assets/wild_salmon_detail_1767485124516.png)

### Video Walkthrough
Below is the recording of the automated verification session.

![Browser Walkthrough](docs/assets/website_verification_walkthrough_1767485061733.webp)

## Milestone 2 Verification (Recalls & Scanner)

We have verified the implementation of advanced food safety features:

### 1. FDA Recalls Page
The `/recalls` page successfully connects to the backend API, displaying a live list of recent Class I, II, and III recalls. Search functionality ("Salmon") was tested and verified.

![Recalls Page Success](docs/assets/recalls_page_success_1767549647249.png)

### 2. Barcode Scanner
The `/scan` page loads correctly and processes barcode inputs. Mock scan `123456` verified the scanner service connectivity.

### 3. Sustainability & Advisories
The Food Detail page has been updated to show NOAA Sustainability Ratings and EPA Advisories.
- **Sustainability**: Badge appears for rated species (e.g., "Best Choice").
- **Advisories**: Warnings for specific waterbodies/states are displayed.

![Food Detail with Badges](docs/assets/food_detail_salmon_success_1767550837096.png)

