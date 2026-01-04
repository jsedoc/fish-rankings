#!/bin/bash
#
# Seed Production Database (Supabase)
# Run this from your local machine with internet access
#

set -e

echo "🌱 Seeding Production Database on Supabase"
echo "=========================================="
echo ""

# Production DATABASE_URL
export DATABASE_URL="postgresql+asyncpg://postgres.jheenyygpvfacyetreuu:pakqyn-4Rifvo-qoqqin@aws-0-us-west-2.pooler.supabase.com:5432/postgres"

echo "📍 Database: Supabase (aws-0-us-west-2)"
echo "🗄️  Target: postgres database"
echo ""
echo "This will:"
echo "  - Create all database tables"
echo "  - Seed 6 food categories"
echo "  - Seed 5 contaminant types"
echo "  - Seed 4 data sources"
echo "  - Scrape 60 fish species from FDA"
echo "  - Scrape 37 produce items from EWG"
echo "  - Fetch 152 research papers from PubMed"
echo ""
echo "⏱️  Estimated time: 60-90 seconds"
echo ""

read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted"
    exit 1
fi

echo ""
echo "🚀 Starting database seeding..."
echo ""

# Navigate to scripts directory
cd "$(dirname "$0")/scripts"

# Run the seeding script
python3 init_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Production database seeded successfully!"
    echo "=========================================="
    echo ""
    echo "📊 Data Summary:"
    echo "  - Categories: 6"
    echo "  - Contaminants: 5"
    echo "  - Data Sources: 4"
    echo "  - Foods: 97 (60 seafood + 37 produce)"
    echo "  - Research Papers: 152"
    echo ""
    echo "🌐 Your API can now serve data!"
    echo ""
    echo "Next steps:"
    echo "  1. Deploy backend to Railway"
    echo "  2. Set NEXT_PUBLIC_API_URL in Vercel"
    echo "  3. Test: https://fish-rankings.vercel.app/category/seafood"
    echo ""
else
    echo ""
    echo "❌ Seeding failed. Check error messages above."
    echo ""
    echo "Common issues:"
    echo "  - Internet connection required"
    echo "  - Python 3.11+ required"
    echo "  - Dependencies must be installed: pip install -r requirements.txt"
    echo "  - Database must be accessible"
    echo ""
    exit 1
fi
