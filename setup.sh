#!/bin/bash
set -e

echo "🚀 Food Safety Platform - Setup Script"
echo "======================================"
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed. Please install PostgreSQL 15+ first."
    echo "   macOS: brew install postgresql@15"
    echo "   Ubuntu: sudo apt-get install postgresql-15"
    exit 1
fi

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Prerequisites check passed!"
echo ""

# Create and activate virtual environment
echo "🐍 Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
echo "✅ Virtual environment active!"
echo ""

# Create database
echo "📦 Creating PostgreSQL database..."
psql -U postgres -c "CREATE DATABASE foodsafety;" 2>/dev/null || echo "  Database may already exist, continuing..."
psql -d foodsafety -U postgres -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
echo "✅ Database ready!"
echo ""

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd apps/api
python3 -m pip install -q -r requirements.txt
cd ../..
echo "✅ Python dependencies installed!"
echo ""

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
cd apps/web
npm install --silent
cd ../..
echo "✅ Node.js dependencies installed!"
echo ""

# Seed database
echo "🌱 Seeding database with food data..."
echo "   This will scrape FDA, EWG, and PubMed data..."
cd scripts
python3 init_db.py
cd ..
echo "✅ Database seeded successfully!"
echo ""

echo "======================================"
echo "🎉 Setup complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Start the backend:"
echo "     cd apps/api && uvicorn main:app --reload"
echo ""
echo "  2. In another terminal, start the frontend:"
echo "     cd apps/web && npm run dev"
echo ""
echo "  3. Visit http://localhost:3000"
echo ""
echo "Happy coding! 🚀"
