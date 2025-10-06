#!/bin/bash

echo "🚀 Starting S&P 500 Stock Analysis Tool..."

# Kill any existing processes
echo "🔄 Cleaning up existing processes..."
pkill -f "python.*run_server" 2>/dev/null || true
pkill -f "react-scripts" 2>/dev/null || true
sleep 2

# Start backend
echo "🔧 Starting backend server..."
cd backend
source ../venv/bin/activate
python api/run_server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

# Open browser
echo "🌐 Opening web browser..."
open http://localhost:3000

echo "✅ Application started!"
echo "📊 Backend API: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user to stop
wait