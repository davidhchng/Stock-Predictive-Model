#!/bin/bash

echo "🚀 Quick Start - S&P 500 Stock Analysis Tool"

# Kill any existing processes
echo "🔄 Cleaning up..."
pkill -f "python.*run_server" 2>/dev/null || true
pkill -f "react-scripts" 2>/dev/null || true
pkill -f "node.*3000" 2>/dev/null || true
sleep 3

# Start backend in background
echo "🔧 Starting backend..."
cd backend
source ../venv/bin/activate
python api/run_server.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend
echo "⏳ Waiting for backend..."
sleep 8

# Check if backend is working
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running!"
    
    # Start frontend
    echo "🎨 Starting frontend..."
    cd frontend
    PORT=3001 npm start > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for frontend
    echo "⏳ Waiting for frontend..."
    sleep 15
    
    # Open browser
    echo "🌐 Opening browser..."
    open http://localhost:3001
    
    echo ""
    echo "✅ Application is running!"
    echo "📊 Backend API: http://localhost:8000"
    echo "🌐 Frontend: http://localhost:3001"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all servers"
    
    # Keep running
    wait
else
    echo "❌ Backend failed to start. Check backend.log for details."
    exit 1
fi
