# Milestone 2 Implementation Plan

**Goal**: Expand data sources and add real-time features
**Timeline**: Today (aggressive build)
**Status**: 🚧 IN PROGRESS

---

## 🎯 Milestone 2 Features

### Core Features
1. **FDA Recalls API** - Real-time food recall alerts ⚡
2. **Open Food Facts API** - Barcode scanning feature 📱
3. **EPA Fish Advisories** - State-specific fish safety data 🗺️
4. **NOAA FishWatch** - Sustainability ratings 🌊
5. **Seafood Watch** - Sustainability ratings (if time permits) 🦐

### Supporting Features
- Real-time alert system
- Barcode scanning frontend
- Enhanced food detail pages
- State-based filtering
- Sustainability scores

---

## 📋 Implementation Order

### Phase 1: Real-Time Alerts (High Impact, Easy) - 1-2 hours
**Feature**: FDA Recalls API Integration

**Tasks**:
- [ ] Create FDA Recalls API client (`scripts/scrapers/fda_recalls_scraper.py`)
- [ ] Add `food_recalls` table to database schema
- [ ] Create API endpoint `/api/v1/recalls`
- [ ] Create scraper to fetch recent recalls
- [ ] Add recall alerts to food detail pages
- [ ] Create recalls page in frontend

**Impact**: Critical safety feature - users see recent recalls immediately

---

### Phase 2: Barcode Scanning (High Impact, Easy) - 1-2 hours
**Feature**: Open Food Facts API Integration

**Tasks**:
- [ ] Create Open Food Facts API client (`scripts/scrapers/openfoodfacts_scraper.py`)
- [ ] Add barcode support to food model
- [ ] Create API endpoint `/api/v1/foods/barcode/{code}`
- [ ] Create barcode lookup function
- [ ] Add barcode search to frontend
- [ ] Create product import from Open Food Facts

**Impact**: Major UX feature - scan products in store

---

### Phase 3: EPA Fish Advisories (High Impact, Medium) - 2-3 hours
**Feature**: State-Specific Fish Safety Data

**Tasks**:
- [ ] Create EPA scraper (`scripts/scrapers/epa_scraper.py`)
- [ ] Add `state_advisories` table
- [ ] Scrape EPA fish advisory data
- [ ] Create API endpoint `/api/v1/advisories`
- [ ] Add state filter to frontend
- [ ] Show state-specific warnings on fish pages

**Impact**: Localized safety information for users

---

### Phase 4: NOAA FishWatch (Medium Impact, Medium) - 2-3 hours
**Feature**: Sustainability Ratings

**Tasks**:
- [ ] Create NOAA scraper (`scripts/scrapers/noaa_scraper.py`)
- [ ] Add `sustainability_ratings` table
- [ ] Scrape NOAA FishWatch data
- [ ] Add sustainability score to food model
- [ ] Create sustainability badge component
- [ ] Show sustainability info on fish pages

**Impact**: Environmental consciousness feature

---

## 🗃️ Database Schema Updates

### New Tables

#### `food_recalls` table
```sql
CREATE TABLE food_recalls (
    id SERIAL PRIMARY KEY,
    recall_number VARCHAR(50) UNIQUE,
    product_description TEXT,
    reason_for_recall TEXT,
    recall_date DATE,
    company_name VARCHAR(255),
    distribution_pattern TEXT,
    food_id INTEGER REFERENCES foods(id),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### `state_advisories` table
```sql
CREATE TABLE state_advisories (
    id SERIAL PRIMARY KEY,
    state_code VARCHAR(2),
    state_name VARCHAR(100),
    waterbody_name VARCHAR(255),
    fish_species VARCHAR(255),
    contaminant_type VARCHAR(100),
    advisory_text TEXT,
    consumption_limit VARCHAR(255),
    effective_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### `sustainability_ratings` table
```sql
CREATE TABLE sustainability_ratings (
    id SERIAL PRIMARY KEY,
    food_id INTEGER REFERENCES foods(id),
    rating VARCHAR(50), -- 'Best Choice', 'Good Alternative', 'Avoid'
    source VARCHAR(100), -- 'NOAA', 'Seafood Watch'
    fishing_method VARCHAR(255),
    location VARCHAR(255),
    overfished BOOLEAN,
    last_updated DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔧 Backend Changes

### New Scrapers
1. `scripts/scrapers/fda_recalls_scraper.py`
2. `scripts/scrapers/openfoodfacts_scraper.py`
3. `scripts/scrapers/epa_scraper.py`
4. `scripts/scrapers/noaa_scraper.py`

### New API Endpoints
1. `GET /api/v1/recalls` - List recent recalls
2. `GET /api/v1/recalls/{recall_id}` - Recall details
3. `GET /api/v1/foods/barcode/{code}` - Barcode lookup
4. `GET /api/v1/advisories` - State advisories (filter by state/species)
5. `GET /api/v1/sustainability/{food_id}` - Sustainability ratings

### Updated Endpoints
- `GET /api/v1/foods/{id}` - Add recalls, sustainability data

---

## 🎨 Frontend Changes

### New Pages
1. `/recalls` - List of recent food recalls
2. `/barcode` - Barcode scanner interface
3. `/advisories` - Interactive state advisory map

### New Components
1. `RecallAlert.tsx` - Warning banner for recalled items
2. `BarcodeScanner.tsx` - Camera barcode scanner
3. `SustainabilityBadge.tsx` - Color-coded rating badge
4. `StateAdvisoryMap.tsx` - Interactive US map
5. `RecallsList.tsx` - Recall cards with filters

### Updated Components
- `FoodDetailPage.tsx` - Add recalls section, sustainability badge
- `SearchBar.tsx` - Add barcode scan button
- `Navigation.tsx` - Add recalls link

---

## 📊 Success Criteria

### Functionality
- [ ] FDA Recalls API fetches data successfully
- [ ] Open Food Facts API returns product info
- [ ] EPA scraper collects state advisories
- [ ] NOAA scraper collects sustainability data
- [ ] All new endpoints return valid data

### Data Quality
- [ ] At least 100 recent recalls imported
- [ ] Barcode lookup works for common products
- [ ] State advisories cover all 50 states
- [ ] Sustainability ratings for 50+ fish species

### User Experience
- [ ] Recalls page shows clear warnings
- [ ] Barcode scanner UI is intuitive
- [ ] State filter works on seafood pages
- [ ] Sustainability badges are color-coded

---

## 🚀 Deployment

### Database Migration
```bash
# Run migrations for new tables
python scripts/migrate_milestone2.py
```

### Data Seeding
```bash
# Fetch all Milestone 2 data
python scripts/seed_milestone2.py
```

### Frontend Build
```bash
cd apps/web
npm run build
```

---

## 📈 Expected Impact

### Data Growth
| Metric | Before (M1) | After (M2) | Growth |
|--------|-------------|------------|--------|
| Food Items | 97 | 300+ | 209% |
| Data Sources | 4 | 8 | 100% |
| Seafood Species | 60 | 100+ | 67% |
| Features | 5 | 10 | 100% |

### New Capabilities
- ✅ Real-time safety alerts
- ✅ In-store barcode scanning
- ✅ State-specific recommendations
- ✅ Environmental sustainability ratings
- ✅ Comprehensive fish advisory data

---

## 🔍 Testing Checklist

### API Testing
- [ ] Test FDA Recalls API with various filters
- [ ] Test barcode lookup with 10+ products
- [ ] Test state advisory filtering
- [ ] Test sustainability endpoint
- [ ] Verify CORS for all new endpoints

### Frontend Testing
- [ ] Recalls page loads and displays data
- [ ] Barcode scanner opens camera
- [ ] State filter updates results
- [ ] Sustainability badges render correctly
- [ ] Mobile responsive design works

### Integration Testing
- [ ] End-to-end recall alert flow
- [ ] Barcode scan to food detail flow
- [ ] State selection to advisory flow
- [ ] Search to sustainability info flow

---

## 📝 Documentation Updates

- [ ] Update README with new features
- [ ] Update API documentation
- [ ] Create barcode scanning guide
- [ ] Document state advisory system
- [ ] Update DATA_SOURCES.md

---

## ⏱️ Time Estimates

| Phase | Feature | Estimated Time |
|-------|---------|----------------|
| Phase 1 | FDA Recalls | 1-2 hours |
| Phase 2 | Barcode Scanning | 1-2 hours |
| Phase 3 | EPA Advisories | 2-3 hours |
| Phase 4 | NOAA Sustainability | 2-3 hours |
| **Total** | | **6-10 hours** |

---

## 🎯 MVP Features (Must Have)

1. ✅ FDA Recalls API (safety critical)
2. ✅ Open Food Facts API (UX game-changer)
3. ⚠️ EPA Advisories (high value, can be simplified)
4. ⚠️ NOAA FishWatch (nice to have, can be basic)

---

**Status**: Ready to implement
**Start Date**: 2026-01-04
**Target Completion**: Today (6-10 hours)
**Priority**: FDA Recalls → Barcode → EPA → NOAA
