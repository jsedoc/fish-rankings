# Food Safety Platform

A comprehensive, data-driven web platform that empowers consumers to make informed, healthier food choices by aggregating and presenting food safety information from authoritative sources (FDA, EPA, academic research, NGOs).

## 🚨 Production Deployment Status

**Current Issue**: Category pages return 404 on https://fish-rankings.vercel.app/category/seafood

**Cause**: Backend API not deployed yet (frontend is deployed to Vercel)

**Fix**: 👉 **[PRODUCTION_404_FIX.md](./PRODUCTION_404_FIX.md)** ← Follow this guide to deploy the backend and fix the 404 error

**Quick Summary**:
1. Deploy backend to Railway (`railway init && railway up`)
2. Seed production database (`./seed-production.sh`)
3. Set `NEXT_PUBLIC_API_URL` in Vercel environment variables
4. Redeploy frontend

**See also**: [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md) for current deployment status

---

## 🎯 Features (Milestone 1)

- ✅ **100+ Foods**: Comprehensive database of seafood and produce with safety data
- 🔍 **Smart Search**: Find any food instantly with intelligent search
- 📊 **Evidence-Based**: All data from FDA, EPA, EWG, and PubMed research
- 🎨 **Beautiful UI**: Clean, accessible design built with Next.js and Tailwind
- 🔬 **Research Papers**: Curated collection of food safety research from PubMed
- 🐟 **Mercury Data**: Complete FDA fish advisory data with consumption guidance
- 🥬 **Pesticide Data**: EWG Dirty Dozen and Clean Fifteen produce ratings

## 🏗️ Architecture

This is a modern monorepo with:

- **Frontend**: Next.js 14 (App Router, React 18, TypeScript, Tailwind CSS)
- **Backend**: FastAPI (Python 3.11, SQLAlchemy, PostgreSQL)
- **Data**: Web scrapers for FDA, EWG, USDA, and PubMed
- **Database**: PostgreSQL 15+ with asyncpg
- **Deployment**: Vercel (frontend) + Railway (backend)

```
food-safety-platform/
├── apps/
│   ├── web/           # Next.js frontend
│   └── api/           # FastAPI backend
├── scripts/
│   └── scrapers/      # Data collection scripts
└── docs/              # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- npm or yarn

### 1. Clone and Install

```bash
# Install frontend dependencies
cd apps/web
npm install

# Install backend dependencies
cd ../api
pip install -r requirements.txt
```

### 2. Set Up Database

```bash
# Create PostgreSQL database
createdb foodsafety

# Or using psql
psql -U postgres
CREATE DATABASE foodsafety;
\q
```

### 3. Configure Environment

```bash
# Backend (.env in apps/api/)
cd apps/api
cp .env.example .env

# Edit .env and set your DATABASE_URL:
# DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/foodsafety
```

### 4. Seed Database

```bash
# From project root
cd scripts
python init_db.py
```

This will:
- Create all database tables
- Scrape FDA fish data (60+ species)
- Scrape EWG produce data (40+ items)
- Collect PubMed research papers
- Populate database with 100+ foods

### 5. Start Development Servers

```bash
# Terminal 1: Start backend
cd apps/api
uvicorn main:app --reload --port 8000

# Terminal 2: Start frontend
cd apps/web
npm run dev
```

Visit **http://localhost:3000** 🎉

## 📊 API Endpoints

The FastAPI backend provides:

```
GET  /api/v1/foods              # List all foods
GET  /api/v1/foods/{id}         # Get food details
GET  /api/v1/foods/slug/{slug}  # Get food by slug
GET  /api/v1/search?q={query}   # Search foods
GET  /api/v1/categories         # List categories
```

API docs available at: **http://localhost:8000/api/docs**

## 🌐 Deployment

### Deploy Backend to Railway

1. Create account at [railway.app](https://railway.app)
2. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   railway login
   ```
3. Deploy:
   ```bash
   cd apps/api
   railway init
   railway up
   ```
4. Add PostgreSQL service in Railway dashboard
5. Set environment variables in Railway

### Deploy Frontend to Vercel

1. Create account at [vercel.com](https://vercel.com)
2. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```
3. Deploy:
   ```bash
   cd apps/web
   vercel
   ```
4. Set environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-backend.up.railway.app
   ```

## 📚 Data Sources

All data comes from trusted, authoritative sources:

- **FDA** (10/10 credibility): Fish mercury levels, consumption advice
- **EWG** (8/10 credibility): Pesticide residues in produce
- **USDA** (10/10 credibility): Nutritional information
- **PubMed** (9/10 credibility): Peer-reviewed research papers

## 🗺️ Roadmap

### ✅ Milestone 1 (Completed Today!)
- [x] Monorepo structure
- [x] PostgreSQL database schema
- [x] FastAPI backend with REST endpoints
- [x] Next.js frontend with search and detail pages
- [x] FDA fish scraper (60+ species)
- [x] EWG produce scraper (40+ items)
- [x] PubMed research paper collector
- [x] Database seeding script

### 🎯 Milestone 2 (Next 2-3 Weeks)
- [ ] LLM-powered natural language queries
- [ ] User authentication (email/password)
- [ ] Saved foods feature
- [ ] Meal planning interface
- [ ] Mobile PWA capabilities
- [ ] Barcode scanning

### 🚀 Milestone 3 (1-2 Months)
- [ ] Personalized risk scoring
- [ ] User health profiles
- [ ] Email alerts for recalls
- [ ] Community contributions
- [ ] 1,000+ foods in database
- [ ] Additional data sources (NOAA, Consumer Reports)

## 🤝 Contributing

This is currently a solo project, but contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This platform provides educational information only and does not constitute medical advice. Always consult healthcare professionals for personalized dietary guidance.

## 🙏 Acknowledgments

- FDA for fish mercury data
- EWG for pesticide residue data
- USDA for nutritional information
- PubMed/NCBI for research access
- All the open-source libraries that make this possible

---

**Built with ❤️ and Claude Code**
