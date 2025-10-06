"""
Main data collection orchestrator that combines S&P 500 scraping and Yahoo Finance data fetching
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.database_manager import DatabaseManager
from scrapers.sp500_scraper import SP500Scraper
from scrapers.yahoo_data_fetcher import YahooDataFetcher
import logging
from datetime import datetime, date
from typing import List, Tuple
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataCollector:
    """Orchestrates the complete data collection process"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.sp500_scraper = SP500Scraper()
        self.yahoo_fetcher = YahooDataFetcher()
    
    def initialize_database(self):
        """Initialize database tables"""
        logger.info("Initializing database...")
        self.db_manager.create_tables()
        logger.info("Database initialized successfully!")
    
    def collect_sp500_tickers(self) -> List[Tuple[str, str]]:
        """
        Collect current S&P 500 tickers and store in database
        
        Returns:
            List of (ticker, name) tuples
        """
        logger.info("Collecting S&P 500 tickers...")
        
        # Scrape tickers from Wikipedia
        tickers_data = self.sp500_scraper.get_tickers_with_retry()
        
        if not tickers_data:
            logger.error("Failed to collect S&P 500 tickers")
            return []
        
        # Store tickers in database
        self.db_manager.add_tickers_batch(tickers_data)
        
        logger.info(f"Successfully collected and stored {len(tickers_data)} S&P 500 tickers")
        return tickers_data
    
    def collect_historical_data(self, tickers: List[str] = None, start_date: str = "2018-01-01", 
                               delay: float = 0.1) -> dict:
        """
        Collect historical stock data for all or specified tickers
        
        Args:
            tickers: List of tickers to collect data for (None for all S&P 500)
            start_date: Start date for historical data
            delay: Delay between requests to avoid rate limiting
            
        Returns:
            Dictionary with collection results
        """
        if tickers is None:
            # Get all tickers from database
            tickers_data = self.db_manager.get_all_tickers()
            tickers = [ticker for ticker, _ in tickers_data]
        
        logger.info(f"Collecting historical data for {len(tickers)} tickers...")
        
        results = {
            'successful': [],
            'failed': [],
            'total_records': 0
        }
        
        for i, ticker in enumerate(tickers):
            logger.info(f"Processing {ticker} ({i+1}/{len(tickers)})")
            
            try:
                # Check if we already have data for this ticker
                latest_date = self.db_manager.get_latest_date(ticker)
                if latest_date:
                    logger.info(f"  {ticker} already has data up to {latest_date}")
                    # Only fetch new data if the latest date is not today
                    if latest_date < date.today():
                        logger.info(f"  Fetching new data for {ticker} from {latest_date}")
                        data = self.yahoo_fetcher.fetch_stock_data(
                            ticker, 
                            (latest_date + time.timedelta(days=1)).strftime("%Y-%m-%d")
                        )
                        if data is not None:
                            records_added = self.db_manager.update_stock_data(ticker, data)
                            results['total_records'] += records_added
                            if records_added > 0:
                                results['successful'].append(ticker)
                            else:
                                logger.info(f"  No new data for {ticker}")
                        else:
                            results['failed'].append(ticker)
                    else:
                        logger.info(f"  {ticker} is up to date")
                        results['successful'].append(ticker)
                else:
                    # No existing data, fetch from start date
                    logger.info(f"  Fetching initial data for {ticker} from {start_date}")
                    data = self.yahoo_fetcher.fetch_stock_data(ticker, start_date)
                    if data is not None:
                        self.db_manager.add_stock_data(ticker, data)
                        results['successful'].append(ticker)
                        results['total_records'] += len(data)
                    else:
                        results['failed'].append(ticker)
                
                # Rate limiting
                if delay > 0 and i < len(tickers) - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")
                results['failed'].append(ticker)
        
        logger.info(f"Data collection completed:")
        logger.info(f"  Successful: {len(results['successful'])}")
        logger.info(f"  Failed: {len(results['failed'])}")
        logger.info(f"  Total records added: {results['total_records']}")
        
        return results
    
    def update_all_data(self, delay: float = 0.1) -> dict:
        """
        Update all stock data with the latest information
        
        Args:
            delay: Delay between requests to avoid rate limiting
            
        Returns:
            Dictionary with update results
        """
        logger.info("Updating all stock data...")
        
        # Get all tickers that have data
        tickers = self.db_manager.get_tickers_with_data()
        
        if not tickers:
            logger.warning("No tickers found in database")
            return {'successful': [], 'failed': [], 'total_records': 0}
        
        return self.collect_historical_data(tickers, delay=delay)
    
    def full_data_collection(self, delay: float = 0.1) -> dict:
        """
        Perform complete data collection from scratch
        
        Args:
            delay: Delay between requests to avoid rate limiting
            
        Returns:
            Dictionary with collection results
        """
        logger.info("Starting full data collection...")
        
        # Initialize database
        self.initialize_database()
        
        # Collect S&P 500 tickers
        tickers_data = self.collect_sp500_tickers()
        if not tickers_data:
            logger.error("Failed to collect S&P 500 tickers")
            return {'successful': [], 'failed': [], 'total_records': 0}
        
        # Extract ticker symbols
        tickers = [ticker for ticker, _ in tickers_data]
        
        # Collect historical data
        results = self.collect_historical_data(tickers, delay=delay)
        
        logger.info("Full data collection completed!")
        return results

def main():
    """Main function for data collection"""
    collector = DataCollector()
    
    print("S&P 500 Stock Data Collection Tool")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Full data collection (S&P 500 tickers + historical data)")
        print("2. Update existing data")
        print("3. Collect S&P 500 tickers only")
        print("4. Collect historical data for specific tickers")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\nStarting full data collection...")
            results = collector.full_data_collection(delay=0.1)
            print(f"\nResults: {results}")
            
        elif choice == '2':
            print("\nUpdating existing data...")
            results = collector.update_all_data(delay=0.1)
            print(f"\nResults: {results}")
            
        elif choice == '3':
            print("\nCollecting S&P 500 tickers...")
            tickers = collector.collect_sp500_tickers()
            print(f"Collected {len(tickers)} tickers")
            
        elif choice == '4':
            tickers_input = input("\nEnter tickers (comma-separated): ").strip()
            if tickers_input:
                tickers = [t.strip().upper() for t in tickers_input.split(',')]
                print(f"\nCollecting data for {tickers}...")
                results = collector.collect_historical_data(tickers, delay=0.1)
                print(f"\nResults: {results}")
            else:
                print("No tickers provided")
                
        elif choice == '5':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
