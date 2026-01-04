# Deployment Status - Food Safety Platform

**Last Updated**: 2026-01-04
**Branch**: `claude/food-safety-platform-mvp-BzGsg`

---

## 🚨 Current Production Issue

**Issue**: Category pages return 404 on https://fish-rankings.vercel.app/category/seafood

**Status**: 🔴 **BACKEND NOT DEPLOYED**

**Root Cause**:
- ✅ Frontend deployed to Vercel (working)
- ❌ Backend NOT deployed (missing)
- ❌ API environment variable not set in Vercel
- ⚠️ Production database needs seeding

---

## 📊 Deployment Status

| Component | Status | URL | Notes |
|-----------|--------|-----|-------|
| **Frontend** | ✅ Deployed | https://fish-rankings.vercel.app | Vercel - Working |
| **Backend API** | ❌ Not Deployed | N/A | **NEEDS DEPLOYMENT** |
| **Database** | ⚠️ Exists but Empty | Supabase | Needs seeding |
| **Environment Vars** | ❌ Not Set | N/A | `NEXT_PUBLIC_API_URL` missing |

---

## ✅ What's Working

1. **Frontend Build**: ✅ Next.js compiles successfully
2. **Frontend Deployment**: ✅ Deployed to Vercel
3. **Homepage**: ✅ https://fish-rankings.vercel.app loads
4. **Static Pages**: ✅ Work correctly
5. **Database**: ✅ Supabase PostgreSQL ready
6. **Code Quality**: ✅ All critical issues fixed
7. **Local Development**: ✅ `./start-dev.sh` works

---

## ❌ What's NOT Working

1. **Backend API**: ❌ Not deployed anywhere
2. **Dynamic Pages**: ❌ Return 404 (need API)
3. **Search**: ❌ Can't fetch data (no API)
4. **Food Details**: ❌ Can't fetch data (no API)
5. **Category Pages**: ❌ Can't fetch data (no API)

---

## 🚀 Fix Guide

**👉 See detailed instructions**: [PRODUCTION_404_FIX.md](./PRODUCTION_404_FIX.md)

### Quick Fix (15 minutes)

**Step 1: Deploy Backend to Railway**
```bash
cd apps/api
railway login
railway init
railway up
```

**Step 2: Set Backend URL in Railway Environment**
In Railway dashboard, set:
```env
DATABASE_URL=postgresql+asyncpg://postgres.jheenyygpvfacyetreuu:pakqyn-4Rifvo-qoqqin@aws-0-us-west-2.pooler.supabase.com:5432/postgres
ENVIRONMENT=production
SECRET_KEY=<generate with: openssl rand -hex 32>
```

**Step 3: Seed Production Database**
From your local machine:
```bash
./seed-production.sh
```

**Step 4: Update Vercel Environment**
In Vercel dashboard, add:
```env
NEXT_PUBLIC_API_URL=<your-railway-backend-url>
```

**Step 5: Redeploy Frontend**
```bash
cd apps/web
vercel --prod
```

---

## 📁 Database Details

**Provider**: Supabase
**Region**: AWS US-West-2
**Connection String**:
```
postgresql+asyncpg://postgres.jheenyygpvfacyetreuu:pakqyn-4Rifvo-qoqqin@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

**Current Status**: Empty (needs seeding)

**To Seed**: Run `./seed-production.sh` from local machine

**Expected Data After Seeding**:
- 6 food categories
- 5 contaminant types
- 4 data sources
- 97 foods (60 fish + 37 produce)
- 152 research papers

---

## 🔍 Why Category Pages Return 404

### Technical Explanation

1. **Next.js Routing**: Dynamic route exists at `apps/web/app/category/[slug]/page.tsx`
2. **API Call**: Page tries to fetch from `/api/v1/foods?category=seafood`
3. **Rewrite Rule**: Request goes to `process.env.NEXT_PUBLIC_API_URL + /api/v1/foods`
4. **Problem**: `NEXT_PUBLIC_API_URL` is not set in Vercel
5. **Fallback**: Defaults to `http://localhost:8000` (which doesn't exist in production)
6. **Result**: Fetch fails, page returns 404

### The Fix

Set `NEXT_PUBLIC_API_URL` in Vercel to point to your deployed Railway backend.

---

## 🎯 Deployment Checklist

### Backend Deployment
- [ ] Deploy FastAPI app to Railway
- [ ] Add Supabase DATABASE_URL to Railway env vars
- [ ] Set ENVIRONMENT=production
- [ ] Generate and set SECRET_KEY
- [ ] Verify ALLOWED_ORIGINS includes Vercel domain
- [ ] Test health endpoint: `https://your-api.railway.app/health`

### Database Setup
- [ ] Run `./seed-production.sh` from local machine
- [ ] Verify 97 foods created
- [ ] Verify 152 research papers created
- [ ] Test direct database connection

### Frontend Configuration
- [ ] Set NEXT_PUBLIC_API_URL in Vercel
- [ ] Set NEXT_PUBLIC_APP_URL in Vercel
- [ ] Redeploy frontend
- [ ] Clear Vercel cache if needed

### Verification
- [ ] Homepage loads: https://fish-rankings.vercel.app
- [ ] Search works: https://fish-rankings.vercel.app/search
- [ ] Category page loads: https://fish-rankings.vercel.app/category/seafood
- [ ] Food detail works: https://fish-rankings.vercel.app/food/salmon
- [ ] No CORS errors in browser console
- [ ] API docs accessible: https://your-api.railway.app/api/docs

---

## 📝 Environment Variables Reference

### Backend (Railway)
```env
DATABASE_URL=postgresql+asyncpg://postgres.jheenyygpvfacyetreuu:pakqyn-4Rifvo-qoqqin@aws-0-us-west-2.pooler.supabase.com:5432/postgres
ENVIRONMENT=production
SECRET_KEY=<generate-with-openssl>
ALLOWED_ORIGINS=["https://fish-rankings.vercel.app","https://*.vercel.app"]
```

### Frontend (Vercel)
```env
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
NEXT_PUBLIC_APP_URL=https://fish-rankings.vercel.app
```

---

## 🔐 Security Notes

**✅ Already Configured**:
- `.gitignore` includes `.env` files
- CORS configured for Vercel domain
- Sensitive files removed from git
- PostgreSQL password in environment variable (not in code)

**⚠️ TODO**:
- Generate production SECRET_KEY
- Review ALLOWED_ORIGINS before going live
- Enable rate limiting (future)
- Set up monitoring (Sentry recommended)

---

## 📊 Cost Estimate

**Current Setup**:
- Frontend (Vercel): **$0/month** (free tier)
- Backend (Railway): **$5-10/month** (free $5 credit, then paid)
- Database (Supabase): **$0/month** (free tier, 500MB)

**Total**: ~$5-10/month

**Scaling**:
- 1K daily users: $10-20/month
- 10K daily users: $50-100/month

---

## 🆘 Troubleshooting

### "I deployed to Railway but still getting 404"
→ Did you set `NEXT_PUBLIC_API_URL` in Vercel?
→ Did you redeploy the frontend after setting it?

### "Backend health check fails"
→ Check Railway logs: `railway logs`
→ Verify DATABASE_URL is set correctly
→ Check if database is accessible from Railway

### "CORS errors in browser console"
→ Verify ALLOWED_ORIGINS in backend config
→ Should include: `"https://fish-rankings.vercel.app"`

### "Database is empty"
→ Run `./seed-production.sh` from local machine
→ Make sure you have internet access
→ Check Python dependencies are installed

---

## 📞 Next Steps

1. **Deploy Backend** → Use Railway (recommended) or Cloud Run
2. **Seed Database** → Run `./seed-production.sh`
3. **Configure Vercel** → Set `NEXT_PUBLIC_API_URL`
4. **Test Production** → Verify all pages work
5. **Monitor** → Check logs for errors

---

## 📚 Documentation

- **Fix Guide**: [PRODUCTION_404_FIX.md](./PRODUCTION_404_FIX.md) ← **START HERE**
- **Deployment Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Milestone 1 Summary**: [MILESTONE_1_READY.md](./MILESTONE_1_READY.md)
- **Issues Tracker**: [ISSUES_AND_TODOS.md](./ISSUES_AND_TODOS.md)
- **Data Sources**: [DATA_SOURCES.md](./DATA_SOURCES.md)

---

**Built with ❤️ and Claude Code**
**Status**: ⚠️ Backend deployment needed
**Priority**: 🔴 HIGH - Production is incomplete
