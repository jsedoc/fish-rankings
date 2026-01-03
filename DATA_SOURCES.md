# Food Safety Platform - Data Sources

This document catalogs all data sources used and planned for the Food Safety Platform, including implementation status, credibility ratings, and integration details.

## 📊 Overview

| Status | Count |
|--------|-------|
| ✅ Implemented | 4 |
| 🔄 In Progress | 0 |
| 📋 Planned | 11 |
| **Total** | **15** |

---

## ✅ IMPLEMENTED SOURCES

### 1. FDA (Food and Drug Administration) - ⭐⭐⭐⭐⭐ (10/10)

**Status**: ✅ Implemented
**Type**: Government
**Implementation**: Web scraper (manual data + API fallback)

**Data Collected**:
- Fish mercury levels for 60+ species
- Consumption advisories (Best Choice, Good Choice, Avoid)
- Risk categorization
- Serving recommendations

**URLs**:
- Main: https://www.fda.gov/food/consumers/advice-about-eating-fish
- API: https://open.fda.gov/apis/

**Update Frequency**: Annually (fish advice), Daily (recalls)
**Coverage**: 60+ fish species
**Implementation File**: `scripts/scrapers/fda_fish_scraper.py`

**Data Structure**:
```python
{
    "name": "Salmon",
    "mercury_ppm": 0.02,
    "risk_score": 20,
    "risk_category": "low",
    "consumption_advice": "Best Choice - 2-3 servings per week",
    "source": "FDA Fish Advice 2024"
}
```

**Integration Notes**:
- Real FDA data used
- Includes detailed mercury measurements
- Categorized by consumption frequency
- Updated annually by FDA

---

### 2. EWG (Environmental Working Group) - ⭐⭐⭐⭐ (8/10)

**Status**: ✅ Implemented
**Type**: Non-Governmental Organization (NGO)
**Implementation**: Web scraper

**Data Collected**:
- Dirty Dozen (12 produce items with highest pesticides)
- Clean Fifteen (15 produce items with lowest pesticides)
- Pesticide risk ratings
- Organic vs. conventional recommendations

**URLs**:
- Main: https://www.ewg.org/foodnews/
- Dirty Dozen: https://www.ewg.org/foodnews/dirty-dozen.php
- Clean Fifteen: https://www.ewg.org/foodnews/clean-fifteen.php

**Update Frequency**: Annually
**Coverage**: 37 produce items (12 Dirty Dozen + 15 Clean Fifteen + 10 middle-tier)
**Implementation File**: `scripts/scrapers/ewg_produce_scraper.py`

**Data Structure**:
```python
{
    "name": "Strawberries",
    "pesticide_level": "high",
    "risk_score": 97,
    "risk_category": "high",
    "ewg_rank": 1,
    "list_type": "Dirty Dozen",
    "advice": "Choose organic when possible to reduce pesticide exposure"
}
```

**Integration Notes**:
- 2024 data included
- Ranked by pesticide load
- Clear organic recommendations
- Backed by independent testing

---

### 3. PubMed / NCBI - ⭐⭐⭐⭐⭐ (9/10)

**Status**: ✅ Implemented
**Type**: Academic / Government
**Implementation**: API (E-utilities)

**Data Collected**:
- Peer-reviewed research papers on food safety
- Studies on mercury, microplastics, pesticides, heavy metals
- Academic journals and publications
- DOIs, PMIDs, abstracts

**URLs**:
- Main: https://pubmed.ncbi.nlm.nih.gov/
- API: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/

**Update Frequency**: Continuous (real-time)
**Coverage**: 150+ papers collected
**Implementation File**: `scripts/scrapers/pubmed_scraper.py`

**Search Topics**:
- Mercury contamination in fish
- Microplastics in food
- Pesticide residues in produce
- Food safety contaminants
- Heavy metals in seafood
- Foodborne pathogens
- PCBs in fish consumption

**Data Structure**:
```python
{
    "pmid": "12345678",
    "title": "Mercury levels in Atlantic salmon...",
    "authors": ["Smith J", "Doe A"],
    "abstract": "This study examines...",
    "journal": "Food Safety Journal",
    "publication_date": "2024-05-01",
    "doi": "10.1234/example",
    "keywords": ["mercury", "fish", "contamination"],
    "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/"
}
```

**Integration Notes**:
- Free API access
- No authentication required
- Rate limits: 3 requests/second
- Last 2 years of publications collected
- Automatic keyword extraction

---

### 4. USDA FoodData Central - ⭐⭐⭐⭐⭐ (10/10)

**Status**: ✅ Implemented
**Type**: Government
**Implementation**: REST API Client

**Data Collected**:
- Nutritional information (macros, vitamins, minerals)
- Serving sizes
- Food categories
- Foundation foods, SR Legacy, Survey foods

**URLs**:
- Main: https://fdc.nal.usda.gov/
- API: https://api.nal.usda.gov/fdc/v1/

**Update Frequency**: Monthly
**API Key**: Optional (free signup at https://fdc.nal.usda.gov/api-key-signup.html)
**Coverage**: Common foods nutrition data
**Implementation File**: `scripts/scrapers/usda_api_client.py`

**Data Structure**:
```python
{
    "name": "Chicken breast",
    "fdc_id": 171477,
    "nutrients": {
        "Protein": {"value": 31, "unit": "g"},
        "Total lipid (fat)": {"value": 3.6, "unit": "g"},
        "Energy": {"value": 165, "unit": "kcal"}
    }
}
```

**Integration Notes**:
- Works without API key (lower rate limits)
- Comprehensive nutrition database
- Multiple food databases available
- High quality government data

---

## 📋 PLANNED SOURCES

### 5. EPA (Environmental Protection Agency) - ⭐⭐⭐⭐⭐ (10/10)

**Status**: 📋 Planned for Milestone 2
**Type**: Government
**Planned Implementation**: API + Web Scraper

**Data to Collect**:
- State-by-state fish advisories
- Water quality affecting fish safety
- Pesticide residue limits
- Regional contamination data

**URLs**:
- Fish Advisories: https://fishadvisoryonline.epa.gov/
- Water Quality: https://www.epa.gov/waterdata

**Update Frequency**: Quarterly
**Priority**: HIGH
**Estimated Integration Time**: 2-3 days

**Why Important**:
- Localized fish safety data
- State-specific recommendations
- Water body contamination levels

---

### 6. NOAA FishWatch - ⭐⭐⭐⭐⭐ (10/10)

**Status**: 📋 Planned for Milestone 2
**Type**: Government
**Planned Implementation**: Web Scraper

**Data to Collect**:
- Overfishing status
- Sustainability ratings
- Fishing method impacts
- Wild vs. farmed comparisons

**URLs**:
- Main: https://www.fishwatch.gov/

**Update Frequency**: Quarterly
**Priority**: MEDIUM
**Estimated Integration Time**: 1-2 days

---

### 7. Monterey Bay Aquarium - Seafood Watch - ⭐⭐⭐⭐ (9/10)

**Status**: 📋 Planned for Milestone 2
**Type**: Non-Profit
**Planned Implementation**: API (partnership required)

**Data to Collect**:
- Seafood sustainability ratings (Best/Good/Avoid)
- Regional recommendations
- Aquaculture certifications
- Fishing practice assessments

**URLs**:
- Main: https://www.seafoodwatch.org/
- API: Contact for partnership

**Update Frequency**: Quarterly
**Priority**: HIGH
**Estimated Integration Time**: 3-5 days (partnership negotiation)

**Why Important**:
- Most trusted seafood sustainability ratings
- Widely used by consumers and restaurants
- Complements FDA safety data with sustainability

---

### 8. Consumer Reports - ⭐⭐⭐⭐ (8/10)

**Status**: 📋 Planned for Milestone 3
**Type**: Non-Profit
**Planned Implementation**: Web Scraper (with subscription)

**Data to Collect**:
- Heavy metals in foods (arsenic, lead, cadmium)
- Pesticide residue testing
- Product safety testing
- Brand-specific contamination data

**URLs**:
- Main: https://www.consumerreports.org/food/

**Update Frequency**: Per study release (irregular)
**Priority**: MEDIUM
**Estimated Cost**: $40/year subscription
**Estimated Integration Time**: 2-3 days

---

### 9. Open Food Facts - ⭐⭐⭐ (7/10)

**Status**: 📋 Planned for Milestone 2 (Barcode Scanning)
**Type**: Crowdsourced
**Planned Implementation**: REST API

**Data to Collect**:
- Barcode (UPC/EAN) lookups
- Product ingredients
- Nutrition facts
- Photos and packaging info

**URLs**:
- Main: https://world.openfoodfacts.org/
- API: https://world.openfoodfacts.org/data

**Update Frequency**: Real-time (crowdsourced)
**API**: Free, no key required
**Priority**: HIGH (for barcode feature)
**Estimated Integration Time**: 1 day

**Why Important**:
- Enables barcode scanning feature
- Large global product database
- Free and open source

---

### 10. WHO (World Health Organization) - ⭐⭐⭐⭐⭐ (10/10)

**Status**: 📋 Planned for Milestone 3
**Type**: International Government
**Planned Implementation**: Web Scraper

**Data to Collect**:
- Codex Alimentarius (international food standards)
- Maximum residue levels (MRLs)
- Food safety guidelines
- International contamination limits

**URLs**:
- Main: https://www.who.int/health-topics/food-safety
- Codex: https://www.fao.org/fao-who-codexalimentarius/en/

**Update Frequency**: Annually
**Priority**: LOW
**Estimated Integration Time**: 3-4 days

---

### 11. FDA Recalls API - ⭐⭐⭐⭐⭐ (10/10)

**Status**: 📋 Planned for Milestone 2 (Real-time Alerts)
**Type**: Government
**Planned Implementation**: REST API

**Data to Collect**:
- Real-time food recalls
- Product details
- Reason for recall
- Distribution areas

**URLs**:
- API: https://api.fda.gov/food/enforcement.json

**Update Frequency**: Real-time
**Priority**: HIGH
**Estimated Integration Time**: 1 day

**Why Important**:
- Critical for user safety
- Enable push notifications
- Match against saved foods

---

### 12. EFSA (European Food Safety Authority) - ⭐⭐⭐⭐⭐ (10/10)

**Status**: 📋 Planned for International Expansion
**Type**: International Government
**Planned Implementation**: Web Scraper

**Data to Collect**:
- European food safety standards
- Pesticide approvals
- Risk assessments
- Scientific opinions

**URLs**:
- Main: https://www.efsa.europa.eu/

**Update Frequency**: Ongoing
**Priority**: LOW (US-focused MVP)
**Estimated Integration Time**: 5-7 days

---

### 13. Health Canada - ⭐⭐⭐⭐⭐ (10/10)

**Status**: 📋 Planned for International Expansion
**Type**: Government
**Planned Implementation**: Web Scraper

**Data to Collect**:
- Canadian food safety data
- Recalls
- Mercury in fish
- Pesticide MRLs

**URLs**:
- Main: https://www.canada.ca/en/health-canada/services/food-nutrition.html

**Update Frequency**: Regular
**Priority**: LOW (US-focused MVP)

---

### 14. Nutritionix - ⭐⭐⭐ (6/10)

**Status**: 📋 Planned for Milestone 3
**Type**: Commercial
**Planned Implementation**: REST API

**Data to Collect**:
- Restaurant menu nutrition
- Branded food products
- Detailed nutrition facts

**URLs**:
- Main: https://www.nutritionix.com/
- API: https://developer.nutritionix.com/

**Update Frequency**: Real-time
**API**: Free tier available
**Priority**: LOW

---

### 15. Edamam - ⭐⭐⭐ (6/10)

**Status**: 📋 Planned for Milestone 3
**Type**: Commercial
**Planned Implementation**: REST API

**Data to Collect**:
- Recipe nutrition analysis
- Ingredient parsing
- Dietary labels

**URLs**:
- Main: https://www.edamam.com/
- API: https://developer.edamam.com/

**Update Frequency**: Real-time
**API**: Free tier available
**Priority**: LOW

---

## 📈 Integration Roadmap

### Milestone 1 (✅ COMPLETE)
- [x] FDA Fish Advisory
- [x] EWG Produce Data
- [x] PubMed Research
- [x] USDA Nutrition

### Milestone 2 (Next 2-3 Weeks)
- [ ] EPA Fish Advisories
- [ ] NOAA FishWatch
- [ ] Seafood Watch API
- [ ] FDA Recalls (real-time)
- [ ] Open Food Facts (barcode)

### Milestone 3 (1-2 Months)
- [ ] Consumer Reports
- [ ] WHO Codex
- [ ] Additional nutrition APIs

### Future Expansion
- [ ] International sources (EFSA, Health Canada)
- [ ] Restaurant menu data
- [ ] More research databases

---

## 🔍 Data Quality Standards

### Credibility Tiers

**Tier 1 (9-10/10)**: Government agencies, international orgs, peer-reviewed research
- Direct integration without additional verification
- Highest trust score shown to users

**Tier 2 (7-8/10)**: Reputable NGOs, established non-profits
- Cross-check with Tier 1 sources when possible
- Clearly attribute source

**Tier 3 (5-6/10)**: Commercial databases, crowdsourced data
- Use for supplementary information only
- Verify critical claims with higher-tier sources
- Clear disclaimer to users

**Tier 4 (1-4/10)**: Unverified sources, news media
- Generally avoided
- Only for non-critical data (e.g., food images)

### Update Requirements

- **Critical Safety Data**: Update within 24 hours of source change
- **Recalls**: Real-time (< 1 hour)
- **Research Papers**: Weekly scans
- **Nutritional Data**: Monthly
- **Sustainability Ratings**: Quarterly

---

## 📝 Implementation Guidelines

### Adding a New Data Source

1. **Research**
   - Verify credibility
   - Check update frequency
   - Review terms of use
   - Test API/website

2. **Create Scraper/Client**
   - Add to `scripts/scrapers/`
   - Follow existing patterns
   - Include error handling
   - Add rate limiting

3. **Register Source**
   - Add to `sources` table in database
   - Set credibility score
   - Document update frequency

4. **Test & Validate**
   - Run scraper
   - Validate data quality
   - Check for duplicates
   - Test error scenarios

5. **Document**
   - Update this file
   - Add to API docs
   - Update README

6. **Monitor**
   - Set up alerts for failures
   - Track data freshness
   - Log API errors

---

## 🎯 Data Coverage Goals

### By Food Category

| Category | Current | Milestone 2 | Milestone 3 | Final Goal |
|----------|---------|-------------|-------------|------------|
| **Seafood** | 60 | 100 | 200 | 500+ |
| **Produce** | 37 | 100 | 200 | 500+ |
| **Meat** | 0 | 50 | 100 | 200+ |
| **Dairy** | 0 | 30 | 75 | 150+ |
| **Grains** | 0 | 25 | 50 | 100+ |
| **Processed** | 0 | 100 | 500 | 2000+ |
| **Total** | **97** | **405** | **1,125** | **3,450+** |

### By Contaminant Type

- [x] Mercury
- [x] Pesticides
- [ ] Lead
- [ ] Arsenic
- [ ] Cadmium
- [ ] Microplastics
- [ ] PCBs
- [ ] Dioxins
- [ ] PFAS
- [ ] Listeria
- [ ] Salmonella
- [ ] E. coli

---

## 🔐 Legal & Ethical Considerations

### Data Usage Rights
- All sources used within their terms of service
- Proper attribution provided
- No commercial data sold or redistributed
- Fair use of academic research (citations only)

### Privacy
- No user data shared with data providers
- Aggregate usage statistics only
- GDPR and CCPA compliant

### Accuracy Disclaimer
- Data is educational, not medical advice
- Sources cited for verification
- Update dates clearly shown
- Encourage consulting healthcare professionals

---

**Last Updated**: 2026-01-03
**Total Sources**: 15 (4 implemented, 11 planned)
**Next Review**: Milestone 2 planning
