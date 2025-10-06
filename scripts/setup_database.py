#!/usr/bin/env python3
"""
Database setup script for initial data collection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.scrapers.data_collector import DataCollector
from backend.database.database_manager import DatabaseManager
import logging
import argparse
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_database():
    """Set up the database with initial data"""
    logger.info("Setting up database...")
    
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        db_manager.create_tables()
        logger.info("Database tables created successfully")
        
        # Initialize data collector
        collector = DataCollector()
        
        # Perform full data collection
        logger.info("Starting full data collection...")
        results = collector.full_data_collection(delay=0.1)  # 0.1 second delay between requests
        
        logger.info("Database setup completed!")
        logger.info(f"Results: {results}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        raise

def update_tickers_only():
    """Update only the S&P 500 ticker list"""
    logger.info("Updating S&P 500 tickers...")
    
    try:
        collector = DataCollector()
        tickers = collector.collect_sp500_tickers()
        
        if tickers:
            logger.info(f"Successfully updated {len(tickers)} S&P 500 tickers")
        else:
            logger.error("Failed to collect S&P 500 tickers")
            
        return tickers
        
    except Exception as e:
        logger.error(f"Error updating tickers: {e}")
        raise

def main():
    """Main function for database setup"""
    parser = argparse.ArgumentParser(description='Setup S&P 500 Stock Database')
    parser.add_argument('--mode', choices=['full', 'tickers-only'], default='full',
                       help='Setup mode: full (default) or tickers-only')
    parser.add_argument('--delay', type=float, default=0.1, 
                       help='Delay between requests in seconds (default: 0.1)')
    
    args = parser.parse_args()
    
    logger.info(f"Starting database setup at {datetime.now()}")
    logger.info(f"Mode: {args.mode}")
    logger.info(f"Request delay: {args.delay} seconds")
    
    try:
        if args.mode == 'full':
            setup_database()
        elif args.mode == 'tickers-only':
            update_tickers_only()
            
        logger.info("Database setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
