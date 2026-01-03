#!/bin/bash
#
# Food Safety Platform - Stop Development Servers
#

echo "🛑 Stopping Food Safety Platform services..."
echo ""

# Stop API
if [ -f /tmp/foodsafety-api.pid ]; then
    API_PID=$(cat /tmp/foodsafety-api.pid)
    if kill -0 $API_PID 2>/dev/null; then
        echo "Stopping API (PID: $API_PID)..."
        kill $API_PID
        rm /tmp/foodsafety-api.pid
    fi
fi

# Stop Web
if [ -f /tmp/foodsafety-web.pid ]; then
    WEB_PID=$(cat /tmp/foodsafety-web.pid)
    if kill -0 $WEB_PID 2>/dev/null; then
        echo "Stopping Frontend (PID: $WEB_PID)..."
        kill $WEB_PID
        rm /tmp/foodsafety-web.pid
    fi
fi

# Kill any remaining processes
pkill -f "uvicorn main:app"
pkill -f "next dev"

echo ""
echo "✅ All services stopped"
