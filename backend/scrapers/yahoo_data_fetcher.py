"""
Yahoo Finance data fetcher for historical stock prices
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Optional, Tuple
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YahooDataFetcher:
    """Fetches historical stock data from Yahoo Finance"""
    
    def __init__(self):
        self.start_date = "2018-01-01"
        self.today = datetime.now().date()
    
    def fetch_stock_data(self, ticker: str, start_date: str = None, end_date: str = None) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data for a given ticker
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            # Use default start date if not provided
            if start_date is None:
                start_date = self.start_date
            
            if end_date is None:
                end_date = self.today.strftime("%Y-%m-%d")
            
            logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
            
            # Create yfinance ticker object
            stock = yf.Ticker(ticker)
            
            # Fetch historical data
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                logger.warning(f"No data found for {ticker}")
                return None
            
            # Ensure we have the required columns (Adj Close is optional)
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in data.columns]
            
            if missing_columns:
                logger.error(f"Missing columns for {ticker}: {missing_columns}")
                return None
            
            # Add Adj Close if missing (use Close as fallback)
            if 'Adj Close' not in data.columns:
                data['Adj Close'] = data['Close']
            
            # Clean the data
            data = data.dropna()
            
            if data.empty:
                logger.warning(f"No valid data after cleaning for {ticker}")
                return None
            
            logger.info(f"Successfully fetched {len(data)} records for {ticker}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return None
    
    def fetch_latest_data(self, ticker: str, days_back: int = 7) -> Optional[pd.DataFrame]:
        """
        Fetch the latest stock data for a ticker
        
        Args:
            ticker: Stock ticker symbol
            days_back: Number of days to look back for latest data
            
        Returns:
            DataFrame with latest OHLCV data or None if failed
        """
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days_back)
            
            return self.fetch_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            
        except Exception as e:
            logger.error(f"Error fetching latest data for {ticker}: {e}")
            return None
    
    def fetch_multiple_tickers(self, tickers: list, start_date: str = None, end_date: str = None, 
                              delay: float = 0.1) -> dict:
        """
        Fetch data for multiple tickers with rate limiting
        
        Args:
            tickers: List of ticker symbols
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            delay: Delay between requests in seconds
            
        Returns:
            Dictionary with ticker as key and DataFrame as value
        """
        results = {}
        
        for i, ticker in enumerate(tickers):
            logger.info(f"Fetching data for {ticker} ({i+1}/{len(tickers)})")
            
            data = self.fetch_stock_data(ticker, start_date, end_date)
            if data is not None:
                results[ticker] = data
            else:
                logger.warning(f"Failed to fetch data for {ticker}")
            
            # Rate limiting to avoid being blocked
            if delay > 0 and i < len(tickers) - 1:
                time.sleep(delay)
        
        logger.info(f"Successfully fetched data for {len(results)} out of {len(tickers)} tickers")
        return results
    
    def validate_ticker(self, ticker: str) -> bool:
        """
        Validate if a ticker exists and has data
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            True if ticker is valid, False otherwise
        """
        try:
            stock = yf.Ticker(ticker)
            # Try to fetch just one day of recent data
            data = stock.history(period="1d")
            return not data.empty
        except Exception as e:
            logger.error(f"Error validating ticker {ticker}: {e}")
            return False
    
    def get_ticker_info(self, ticker: str) -> Optional[dict]:
        """
        Get basic information about a ticker
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with ticker info or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'ticker': ticker,
                'name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD')
            }
        except Exception as e:
            logger.error(f"Error getting info for {ticker}: {e}")
            return None

def main():
    """Main function to test the data fetcher"""
    fetcher = YahooDataFetcher()
    
    # Test with a few popular stocks
    test_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    print("Testing Yahoo Finance data fetcher...")
    
    for ticker in test_tickers:
        print(f"\nTesting {ticker}:")
        
        # Validate ticker
        if fetcher.validate_ticker(ticker):
            print(f"✓ {ticker} is valid")
            
            # Get basic info
            info = fetcher.get_ticker_info(ticker)
            if info:
                print(f"  Name: {info['name']}")
                print(f"  Sector: {info['sector']}")
            
            # Fetch recent data
            data = fetcher.fetch_latest_data(ticker, days_back=5)
            if data is not None:
                print(f"  Latest data: {len(data)} records")
                print(f"  Latest close: ${data['Close'].iloc[-1]:.2f}")
            else:
                print(f"  ✗ Failed to fetch data for {ticker}")
        else:
            print(f"✗ {ticker} is not valid")

if __name__ == "__main__":
    main()
