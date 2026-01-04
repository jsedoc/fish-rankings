# Development Guide

## Setup

1.  **Prerequisites**: Python 3.11+, PostgreSQL, Node.js.
2.  **Environment**:
    - Backend: `apps/api/.env` (copy from `.env.example`).
    - Database: Create `foodsafety` DB locally.
    - Python: Create `.venv` and install requirements.

## Database Initialization & Data Ingestion

We use a combination of robust JSON data loading and dynamic scrapers.
To seed the database with all data (Sources, Categories, Fish, Produce, Papers):
```bash
cd apps/api
../../.venv/bin/python3 ../../scripts/init_db.py
```
This script:
- Creates tables.
- Loads Fish data from `data/fda_mercury_1990_2012.json` and `data/ewg_seafood.json`.
- Scrapes/Seeds Produce data (EWG).
- Scrapes/Seeds Research Papers (PubMed).

## Running the Application

### Using the Helper Script
```bash
./start-dev.sh
```
This starts PostgreSQL (if needed), Backend (port 8000), and Frontend (port 3000).

### Manual Start
**Backend**:
```bash
cd apps/api
../../.venv/bin/uvicorn main:app --reload --port 8000
```

**Frontend**:
```bash
cd apps/web
npm run dev
```

## Testing

Backend unit tests are located in `apps/api/tests`.
Run them with:
```bash
cd apps/api
pytest
```

## Repository Structure
- `apps/api`: FastAPI backend.
- `apps/web`: Next.js frontend.
- `scripts`: Data ingestion and DB initialization.
- `data`: Persisted JSON datasets for reproducible seeding.
