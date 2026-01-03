#!/bin/bash
#
# Food Safety Platform - Development Server Startup Script
# Starts PostgreSQL, FastAPI backend, and Next.js frontend
#

set -e

echo "🚀 Food Safety Platform - Starting Development Servers"
echo "======================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if PostgreSQL is running
echo "📦 Checking PostgreSQL..."
if ! sudo service postgresql status | grep -q "online"; then
    echo "   Starting PostgreSQL..."
    sudo service postgresql start
    sleep 2
fi
echo -e "${GREEN}✓${NC} PostgreSQL is running"
echo ""

# Check if database exists
echo "🗄️  Checking database..."
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw foodsafety; then
    echo -e "${YELLOW}⚠${NC}  Database 'foodsafety' not found"
    echo "   Creating database and seeding data..."
    sudo -u postgres psql -c "CREATE DATABASE foodsafety;"
    cd scripts && python3 init_db.py
    cd ..
else
    echo -e "${GREEN}✓${NC} Database exists"
fi
echo ""

# Start FastAPI backend
echo "🐍 Starting FastAPI backend..."
cd apps/api
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > /tmp/foodsafety-api.log 2>&1 &
API_PID=$!
echo $API_PID > /tmp/foodsafety-api.pid
echo -e "${GREEN}✓${NC} Backend started (PID: $API_PID)"
echo "   Logs: /tmp/foodsafety-api.log"
echo "   URL: http://localhost:8000"
echo "   Docs: http://localhost:8000/api/docs"
cd ../..

# Wait for API to be ready
echo "   Waiting for API to be ready..."
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} API is healthy"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}✗${NC} API failed to start. Check logs: /tmp/foodsafety-api.log"
        kill $API_PID 2>/dev/null
        exit 1
    fi
    sleep 1
done
echo ""

# Start Next.js frontend
echo "⚛️  Starting Next.js frontend..."
cd apps/web
npm run dev > /tmp/foodsafety-web.log 2>&1 &
WEB_PID=$!
echo $WEB_PID > /tmp/foodsafety-web.pid
echo -e "${GREEN}✓${NC} Frontend started (PID: $WEB_PID)"
echo "   Logs: /tmp/foodsafety-web.log"
echo "   URL: http://localhost:3000"
cd ../..
echo ""

echo "======================================================"
echo -e "${GREEN}🎉 All services started successfully!${NC}"
echo "======================================================"
echo ""
echo "Services:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/api/docs"
echo ""
echo "Process IDs:"
echo "  Backend:   $API_PID"
echo "  Frontend:  $WEB_PID"
echo ""
echo "Logs:"
echo "  API:       tail -f /tmp/foodsafety-api.log"
echo "  Frontend:  tail -f /tmp/foodsafety-web.log"
echo ""
echo "To stop all services, run:"
echo "  ./stop-dev.sh"
echo ""
echo "Press Ctrl+C to stop (will leave services running in background)"
echo ""

# Keep script running
wait
