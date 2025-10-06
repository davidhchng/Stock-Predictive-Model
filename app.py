#!/usr/bin/env python3
"""
Main FastAPI application entrypoint for Stock King
"""

import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.api.main import app

# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (for the HTML frontend)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the main HTML file"""
    return FileResponse("simple_webpage.html")

def init_database_on_startup():
    """Initialize database on startup"""
    try:
        print("🚀 Initializing Stock King database...")
        from backend.database.database_manager import DatabaseManager
        from backend.scrapers.data_collector import DataCollector
        
        # Initialize database
        db_manager = DatabaseManager()
        
        # Check if we have data
        tickers = db_manager.get_all_tickers()
        if len(tickers) == 0:
            print("📊 No data found, collecting S&P 500 data...")
            collector = DataCollector()
            result = collector.full_data_collection()
            print(f"✅ Database initialized! Processed {result.get('stocks_processed', 0)} stocks")
        else:
            print(f"✅ Database already has {len(tickers)} tickers")
            
    except Exception as e:
        print(f"⚠️ Database initialization warning: {str(e)}")

if __name__ == "__main__":
    # Initialize database on startup
    init_database_on_startup()
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
