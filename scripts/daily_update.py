#!/usr/bin/env python3
"""
Daily update script for S&P 500 stock data
This script can be scheduled to run daily to update stock data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.scrapers.data_collector import DataCollector
from backend.database.database_manager import DatabaseManager
import logging
from datetime import datetime, date
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DailyUpdater:
    """Handles daily updates of stock data"""
    
    def __init__(self):
        self.data_collector = DataCollector()
        self.db_manager = DatabaseManager()
    
    def update_all_data(self, delay: float = 0.1) -> dict:
        """
        Update all stock data with latest information
        
        Args:
            delay: Delay between requests to avoid rate limiting
            
        Returns:
            Dictionary with update results
        """
        logger.info("Starting daily data update...")
        
        try:
            # Update all existing data
            results = self.data_collector.update_all_data(delay=delay)
            
            # Log summary
            successful = len(results['successful'])
            failed = len(results['failed'])
            total_records = results['total_records']
            
            logger.info(f"Daily update completed:")
            logger.info(f"  Successful updates: {successful}")
            logger.info(f"  Failed updates: {failed}")
            logger.info(f"  Total new records: {total_records}")
            
            # Log failed tickers for debugging
            if failed > 0:
                logger.warning(f"Failed tickers: {', '.join(results['failed'][:10])}")  # Log first 10
            
            return results
            
        except Exception as e:
            logger.error(f"Error in daily update: {e}")
            return {'error': str(e)}
    
    def update_specific_tickers(self, tickers: list, delay: float = 0.1) -> dict:
        """
        Update data for specific tickers
        
        Args:
            tickers: List of ticker symbols to update
            delay: Delay between requests
            
        Returns:
            Dictionary with update results
        """
        logger.info(f"Updating specific tickers: {', '.join(tickers)}")
        
        try:
            results = self.data_collector.collect_historical_data(tickers, delay=delay)
            return results
            
        except Exception as e:
            logger.error(f"Error updating specific tickers: {e}")
            return {'error': str(e)}
    
    def check_data_freshness(self) -> dict:
        """
        Check how fresh the data is
        
        Returns:
            Dictionary with data freshness information
        """
        try:
            tickers_with_data = self.db_manager.get_tickers_with_data()
            today = date.today()
            
            freshness_info = {
                'total_tickers': len(tickers_with_data),
                'up_to_date': 0,
                'outdated': 0,
                'missing_data': 0
            }
            
            for ticker in tickers_with_data[:20]:  # Check first 20 tickers as sample
                latest_date = self.db_manager.get_latest_date(ticker)
                
                if not latest_date:
                    freshness_info['missing_data'] += 1
                elif latest_date < today:
                    freshness_info['outdated'] += 1
                else:
                    freshness_info['up_to_date'] += 1
            
            logger.info(f"Data freshness check: {freshness_info}")
            return freshness_info
            
        except Exception as e:
            logger.error(f"Error checking data freshness: {e}")
            return {'error': str(e)}

def main():
    """Main function for daily update script"""
    parser = argparse.ArgumentParser(description='Daily S&P 500 Stock Data Update')
    parser.add_argument('--mode', choices=['all', 'specific', 'check'], default='all',
                       help='Update mode: all (default), specific tickers, or check freshness')
    parser.add_argument('--tickers', nargs='+', help='Specific tickers to update (for specific mode)')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between requests (default: 0.1)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    updater = DailyUpdater()
    
    logger.info(f"Starting daily update script at {datetime.now()}")
    logger.info(f"Mode: {args.mode}")
    
    try:
        if args.mode == 'all':
            results = updater.update_all_data(delay=args.delay)
            logger.info(f"Update results: {results}")
            
        elif args.mode == 'specific':
            if not args.tickers:
                logger.error("Specific tickers must be provided for specific mode")
                sys.exit(1)
            results = updater.update_specific_tickers(args.tickers, delay=args.delay)
            logger.info(f"Update results: {results}")
            
        elif args.mode == 'check':
            freshness = updater.check_data_freshness()
            logger.info(f"Data freshness: {freshness}")
            
        logger.info("Daily update script completed successfully")
        
    except Exception as e:
        logger.error(f"Daily update script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
