# Issues Found and Fixes Implemented

## 1. Setup & Infrastructure
*   **Issue**: `setup.sh` used system Python, leading to `PEP 668` "externally managed environment" errors.
*   **Fix**: Modified script to create and activate a Python virtual environment (`.venv`).
*   **Issue**: `pg_trgm` extension was missing from PostgreSQL, causing index creation failures for search.
*   **Fix**: Added `CREATE EXTENSION IF NOT EXISTS pg_trgm;` to the setup script.

## 2. Database Initialization (`init_db.py`)
*   **Issue**: Script imports matched an old file structure (`src.models`) rather than the actual one (`app.db.models`).
*   **Issue**: Created obsolete models (`FishSpecies`) instead of current ones (`Food`).
*   **Issue**: Attempted to create `Food` records without first creating their dependencies (`Contaminant`, `FoodCategory`).
*   **Issue**: `NameError: name 'func' is not defined`.
*   **Fix**: Rewrote the entire script to correctly import models, follow the schema dependency order, and use SQLAlchemy's `func` correctly.

## 3. Backend API (FastAPI/SQLAlchemy)
*   **Issue**: `MissingGreenlet` error during response serialization. This occurs because Pydantic tries to access lazy-loaded attributes (`category`, `contaminants`, `nutrients`) outside the async session context.
*   **Fix**: Updated `apps/api/app/api/v1/endpoints/foods.py` and `search.py` to use `joinedload` (eager loading) for all relationships required in the response schemas.
    *   *Note*: `selectinload` was initially tried but sometimes still caused issues in specific nested contexts or loops; `joinedload` proved stable for these 1-to-1 and 1-to-many depths.
*   **Issue**: Search endpoint returned a 500 status due to the same serialization issue.
*   **Fix**: Applied eager loading options to the search queries as well.

## 4. Frontend (Next.js)
*   **Issue**: Food Detail page (`/food/[slug]`) was fetching from `/api/food/{slug}`, which returned 404.
*   **Fix**: Updated fetch URL to the correct endpoint: `/api/v1/foods/slug/{slug}` in `apps/web/app/food/[slug]/page.tsx`.
*   **Issue**: CORS errors were observed when backend redirected URLs (e.g. strict slashes).
*   **Fix**: Ensured exact path matching in requests and backend router configurations.

## Remaining / Potential Improvements
*   **Git Ignore**: `apps/web/.next`, `apps/web/node_modules`, `apps/api/__pycache__` and `.venv` are currently visible in `git status` (as untracked). Ensure `.gitignore` is properly configured at the root and in subdirectories to keep the repo clean.
*   **Error Handling**: Frontend error handling is basic. Improved UI feedback for API failures (like the 500 error we saw) would be better than a blank or broken page.
*   **Testing**: Add automated integration tests to catch the `MissingGreenlet` serialization issues in the CI pipeline.
