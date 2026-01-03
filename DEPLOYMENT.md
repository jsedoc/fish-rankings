# Deployment Guide

This guide covers deploying the Food Safety Platform to production using Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account
- Railway account (free tier available)
- Vercel account (free tier available)
- Your code pushed to a GitHub repository

## Option 1: Deploy to Railway + Vercel (Recommended)

### Step 1: Deploy Backend to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your food-safety-platform repository
   - Railway will detect the Dockerfile in `apps/api/`

3. **Add PostgreSQL Database**
   - In your project dashboard, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway will create a database and set `DATABASE_URL` automatically

4. **Configure Environment Variables**
   - Go to your API service → Variables
   - Add the following:
     ```
     ENVIRONMENT=production
     SECRET_KEY=<generate with: openssl rand -hex 32>
     ALLOWED_ORIGINS=["https://your-app.vercel.app"]
     ```
   - Note: `DATABASE_URL` is set automatically by Railway

5. **Deploy**
   - Railway will automatically deploy
   - Copy your backend URL (e.g., `https://your-api.up.railway.app`)

6. **Run Database Migrations**
   - In Railway dashboard, open your API service
   - Go to "Settings" → "Deploy"
   - Add a custom start command or run migrations manually via Railway CLI

### Step 2: Deploy Frontend to Vercel

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Select the repository

3. **Configure Build Settings**
   - Framework Preset: Next.js
   - Root Directory: `apps/web`
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

4. **Set Environment Variables**
   - Add the following:
     ```
     NEXT_PUBLIC_API_URL=https://your-railway-backend.up.railway.app
     NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
     ```

5. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your app
   - Your app will be live at `https://your-app.vercel.app`

6. **Update Backend CORS**
   - Go back to Railway
   - Update `ALLOWED_ORIGINS` to include your Vercel URL
   - Redeploy the backend

### Step 3: Seed Production Database

You have two options:

**Option A: Run seed script from local machine**
```bash
# Set DATABASE_URL to your Railway PostgreSQL URL
export DATABASE_URL="postgresql+asyncpg://user:pass@host:port/db"
cd scripts
python init_db.py
```

**Option B: Run seed script on Railway**
- Connect to your Railway project
- Run the seeding script via Railway CLI or create a one-off task

## Option 2: Deploy to Google Cloud Platform (GCP)

### Backend: Cloud Run

1. **Set Up GCP Project**
   ```bash
   gcloud init
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Create Cloud SQL PostgreSQL Instance**
   ```bash
   gcloud sql instances create foodsafety-db \
     --database-version=POSTGRES_15 \
     --tier=db-f1-micro \
     --region=us-central1

   gcloud sql databases create foodsafety \
     --instance=foodsafety-db
   ```

3. **Build and Deploy to Cloud Run**
   ```bash
   cd apps/api

   # Build container
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/foodsafety-api

   # Deploy to Cloud Run
   gcloud run deploy foodsafety-api \
     --image gcr.io/YOUR_PROJECT_ID/foodsafety-api \
     --platform managed \
     --region us-central1 \
     --add-cloudsql-instances YOUR_PROJECT_ID:us-central1:foodsafety-db \
     --set-env-vars DATABASE_URL="postgresql+asyncpg://..." \
     --allow-unauthenticated
   ```

4. **Set Environment Variables**
   ```bash
   gcloud run services update foodsafety-api \
     --set-env-vars ENVIRONMENT=production \
     --set-env-vars SECRET_KEY=your-secret-key
   ```

### Frontend: Vercel (same as above)

Or use Firebase Hosting / Cloud Storage + CDN if you prefer staying in GCP ecosystem.

## Post-Deployment Checklist

- [ ] Backend health check works: `https://your-api.url/health`
- [ ] Frontend loads successfully
- [ ] Search functionality works
- [ ] Food detail pages load
- [ ] API docs accessible: `https://your-api.url/api/docs`
- [ ] Database contains foods (check a few searches)
- [ ] CORS configured correctly (no console errors)
- [ ] HTTPS enabled on both frontend and backend
- [ ] Environment variables set correctly
- [ ] Monitoring set up (Railway/Vercel have built-in monitoring)

## Monitoring

### Railway
- Built-in metrics dashboard
- View logs in real-time
- Set up alerts for downtime

### Vercel
- Analytics dashboard
- Performance metrics
- Error tracking

### Optional: Add Sentry
```bash
# Install Sentry
pip install sentry-sdk
npm install @sentry/nextjs

# Configure in your apps
# See: https://docs.sentry.io/
```

## Updating Your Deployment

### Auto-Deploy (Recommended)
Both Railway and Vercel support automatic deployments from GitHub:
- Push to `main` branch → automatic deployment
- Preview deployments for pull requests

### Manual Deploy
```bash
# Railway
cd apps/api
railway up

# Vercel
cd apps/web
vercel --prod
```

## Troubleshooting

### Backend won't start
- Check Railway logs for errors
- Verify `DATABASE_URL` is set correctly
- Ensure PostgreSQL database exists

### Frontend shows API errors
- Verify `NEXT_PUBLIC_API_URL` points to correct backend
- Check CORS configuration in backend
- Verify backend is running and healthy

### Database connection issues
- Check DATABASE_URL format
- For Railway: ensure PostgreSQL service is running
- For GCP: verify Cloud SQL connection settings

### Slow performance
- Check database indexes (we create them in migrations)
- Monitor API response times in Railway/Vercel dashboards
- Consider upgrading to paid tiers for better performance

## Costs

### Free Tier Limits
- **Railway**: $5/month credit (enough for small projects)
- **Vercel**: 100GB bandwidth, unlimited deploys
- **GCP**: $300 credit for 90 days, then pay-as-you-go

### Estimated Monthly Costs (Low Traffic)
- Railway (Hobby): $5-10/month
- Vercel: Free
- **Total**: ~$5-10/month

### Scaling Up
As your traffic grows, expect:
- **1K daily users**: $20-30/month
- **10K daily users**: $100-200/month
- **100K daily users**: $500-1000/month (time to optimize!)

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong `SECRET_KEY` (32+ random characters)
- [ ] Enable HTTPS (done automatically by Railway/Vercel)
- [ ] Set up rate limiting (future enhancement)
- [ ] Regular backups enabled (Railway does this automatically)
- [ ] Database credentials stored in environment variables (not in code)
- [ ] CORS properly configured (only allow your frontend domain)

## Need Help?

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- GCP Docs: https://cloud.google.com/docs
- File an issue in this repository

Happy deploying! 🚀
