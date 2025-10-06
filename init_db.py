#!/usr/bin/env python3
"""
Database initialization script for Stock King
"""

import sys
import os
import time

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def init_database():
    """Initialize the database with S&P 500 data"""
    try:
        print("🚀 Initializing Stock King database...")
        
        from backend.database.database_manager import DatabaseManager
        from backend.scrapers.data_collector import DataCollector
        
        # Initialize database
        print("📊 Setting up database...")
        db_manager = DatabaseManager()
        
        # Collect S&P 500 data
        print("📈 Collecting S&P 500 data...")
        collector = DataCollector()
        result = collector.collect_all_data()
        
        print(f"✅ Database initialized successfully!")
        print(f"   - Tickers added: {result.get('tickers_added', 0)}")
        print(f"   - Stocks processed: {result.get('stocks_processed', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Wait a bit for the server to start
    time.sleep(5)
    init_database()
