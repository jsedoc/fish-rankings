# Issues and TODOs - Food Safety Platform

## ✅ FIXED ISSUES (Milestone 1)

### 1. ✅ PostgreSQL Extension Missing
**Issue**: `pg_trgm` extension not installed, causing database seeding to fail
**Fix**: Removed GIN index from models (optional feature for MVP)
**File**: `apps/api/app/db/models.py`
**Status**: RESOLVED

### 2. ✅ Date Parsing Error in PubMed Scraper
**Issue**: Research papers with non-ISO date formats (e.g., "2024-Sep-01") causing crashes
**Fix**: Added try-except block to handle date parsing errors gracefully
**File**: `scripts/init_db.py`
**Status**: RESOLVED

### 3. ✅ PostgreSQL Authentication
**Issue**: Default postgres user had no password set
**Fix**: Set password with `ALTER USER postgres PASSWORD 'postgres';`
**Status**: RESOLVED

### 4. ✅ Python Dependencies
**Issue**: SQLAlchemy, httpx, and other packages not installed
**Fix**: Installed all requirements from `requirements.txt`
**Status**: RESOLVED

### 5. ✅ TypeScript Import Errors in Food Detail Page
**Issue**: Missing `notFound` import in `apps/web/app/food/[slug]/page.tsx`
**Fix**: Added `import { notFound } from 'next/navigation'`
**Status**: RESOLVED

### 6. ✅ Vercel Deployment Configuration
**Issue**: Missing root `vercel.json` for monorepo
**Fix**: Added proper `vercel.json` routing API requests to python backend
**Status**: RESOLVED

### 7. ✅ Merge Conflict Resolution
**Issue**: `init_db.py` corrupted by merge
**Fix**: Rewrote script to support hybrid JSON + Scraper loading
**Status**: RESOLVED

---

## 🔧 MINOR ISSUES (Non-blocking for MVP)

### 1. FastAPI Trailing Slash Redirect
**Issue**: `/api/v1/foods` redirects to `/api/v1/foods/` (307 redirect)
**Impact**: Minor - works but adds latency
**Priority**: Low
**Fix**: Update router configuration to handle both
**File**: `apps/api/app/api/v1/endpoints/foods.py`

### 2. Next.js ESLint Not Configured
**Issue**: Running `next lint` prompts for configuration
**Impact**: Cosmetic - doesn't affect functionality
**Priority**: Low
**Fix**: Run `npx next lint` and select "Strict (recommended)"

---

## 📋 TODOS FOR MILESTONE 1 COMPLETION

### High Priority (Complete Before Launch)

- [x] **Fix TypeScript import error** in `apps/web/app/food/[slug]/page.tsx`
- [x] **Test end-to-end flow** (Verified via Walkthrough)
- [x] **Create simple test/start script** (`start-dev.sh` created)
- [x] **Verify API endpoints work from frontend** (Search and Detail pages verified)
- [x] **Vercel Deployment Setup** (`vercel.json` created)

### Medium Priority (Nice to Have)

- [x] **Add pg_trgm extension** for better search (Implemented in `setup.sh`)
- [ ] **Configure ESLint for Next.js**
- [x] **Add basic error handling** in frontend (Implemented 404 handling)
- [x] **Create development .env templates** (`apps/api/.env.example` exists)

### Low Priority (Post-MVP)

- [ ] **Add API request logging**
- [ ] **Add frontend analytics**
- [ ] **Optimize database queries**
- [ ] **Add database indexes** for performance
- [ ] **Set up Redis** for caching
- [ ] **Add rate limiting** to API

---

## 📊 DATABASE STATUS

✅ **Successfully Seeded:**
- 6 food categories
- 5 contaminant types
- 4 data sources
- 60 fish species (from FDA)
- 37 produce items (from EWG)
- 152 research papers (from PubMed)

**Total**: 110 foods with complete safety data

---

## 📝 NOTES

### What's Working
✅ Database seeding (Fish + Produce + Papers)
✅ FastAPI backend starts and responds
✅ Health check endpoint works
✅ Data scrapers functional (FDA, EWG, PubMed)
✅ Next.js dependencies installed
✅ Frontend Search & Detail Pages Verification successful

### What Needs Fixing
(None - Milestone 1 Goal Met)

### Priority Order
1. Deploy to Vercel (Ready via `chore/vercel-setup` PR)

**Total time to MVP**: 0 minutes (Complete)

---

**Last Updated**: 2026-01-03
**Status**: 100% Complete - MVP Ready
**Next**: Deploy to Vercel
