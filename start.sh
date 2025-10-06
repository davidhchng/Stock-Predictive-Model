222222222222#!/bin/bash

# S&P 500 Stock Analysis Tool - Quick Start Script
# This script helps you quickly start the application

echo "🚀 S&P 500 Stock Analysis Tool - Quick Start"
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Function to start backend
start_backend() {
    echo "🔧 Starting backend server..."
    cd backend
    python3 api/run_server.py &
    BACKEND_PID=$!
    echo "📊 Backend started with PID: $BACKEND_PID"
    cd ..
    return $BACKEND_PID
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting frontend server..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    echo "🌐 Frontend started with PID: $FRONTEND_PID"
    cd ..
    return $FRONTEND_PID
}

# Function to check if ports are available
check_ports() {
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️ Port 8000 is already in use. Backend might already be running."
    fi
    
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️ Port 3000 is already in use. Frontend might already be running."
    fi
}

# Function to install dependencies
install_dependencies() {
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
    
    echo "📦 Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
}

# Function to setup database
setup_database() {
    echo "🗄️ Setting up database..."
    python3 scripts/setup_database.py
}

# Main menu
show_menu() {
    echo ""
    echo "Choose an option:"
    echo "1) Full setup (install dependencies + setup database + start servers)"
    echo "2) Start servers only (if already set up)"
    echo "3) Install dependencies only"
    echo "4) Setup database only"
    echo "5) Run demo"
    echo "6) Exit"
    echo ""
    read -p "Enter your choice (1-6): " choice
}

# Handle user choice
handle_choice() {
    case $choice in
        1)
            echo "🔄 Running full setup..."
            check_ports
            install_dependencies
            setup_database
            start_backend
            sleep 5
            start_frontend
            echo ""
            echo "✅ Setup complete! Applications are starting..."
            echo "🌐 Frontend: http://localhost:3000"
            echo "📊 Backend API: http://localhost:8000"
            echo "📚 API Docs: http://localhost:8000/docs"
            echo ""
            echo "Press Ctrl+C to stop all servers"
            wait
            ;;
        2)
            echo "🚀 Starting servers..."
            check_ports
            start_backend
            sleep 5
            start_frontend
            echo ""
            echo "✅ Servers started!"
            echo "🌐 Frontend: http://localhost:3000"
            echo "📊 Backend API: http://localhost:8000"
            echo ""
            echo "Press Ctrl+C to stop all servers"
            wait
            ;;
        3)
            echo "📦 Installing dependencies..."
            install_dependencies
            echo "✅ Dependencies installed!"
            ;;
        4)
            echo "🗄️ Setting up database..."
            setup_database
            echo "✅ Database setup complete!"
            ;;
        5)
            echo "🎬 Running demo..."
            python3 scripts/run_demo.py
            ;;
        6)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            ;;
    esac
}

# Main execution
echo "🔍 Checking system..."
check_ports

# Show menu and handle choice
while true; do
    show_menu
    handle_choice
    
    if [ $choice -eq 1 ] || [ $choice -eq 2 ]; then
        break
    fi
    
    echo ""
    read -p "Press Enter to continue..."
done
