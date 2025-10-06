"""
S&P 500 ticker scraper from Wikipedia
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Tuple
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SP500Scraper:
    """Scrapes current S&P 500 ticker symbols and company names from Wikipedia"""
    
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_sp500_tickers(self) -> List[Tuple[str, str]]:
        """
        Scrape S&P 500 ticker symbols and company names from Wikipedia
        
        Returns:
            List of tuples (ticker, company_name)
        """
        try:
            logger.info("Scraping S&P 500 tickers from Wikipedia...")
            
            # Make request to Wikipedia page
            response = requests.get(self.base_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main table with S&P 500 companies
            table = soup.find('table', {'id': 'constituents'})
            if not table:
                logger.error("Could not find S&P 500 table on Wikipedia page")
                return []
            
            tickers_data = []
            
            # Extract data from table rows
            for row in table.find('tbody').find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    # Extract ticker symbol (first column)
                    ticker_cell = cells[0]
                    ticker = ticker_cell.get_text(strip=True)
                    
                    # Extract company name (second column)
                    name_cell = cells[1]
                    company_name = name_cell.get_text(strip=True)
                    
                    # Clean ticker symbol (remove any extra characters)
                    ticker = ticker.replace('.', '-')  # Yahoo Finance uses - instead of .
                    
                    if ticker and company_name:
                        tickers_data.append((ticker, company_name))
            
            logger.info(f"Successfully scraped {len(tickers_data)} S&P 500 tickers")
            return tickers_data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching Wikipedia page: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing Wikipedia page: {e}")
            return []
    
    def save_tickers_to_csv(self, tickers_data: List[Tuple[str, str]], filename: str = "sp500_tickers.csv"):
        """Save tickers data to CSV file"""
        try:
            df = pd.DataFrame(tickers_data, columns=['Ticker', 'Company_Name'])
            df.to_csv(filename, index=False)
            logger.info(f"Saved {len(tickers_data)} tickers to {filename}")
        except Exception as e:
            logger.error(f"Error saving tickers to CSV: {e}")
    
    def get_tickers_with_retry(self, max_retries: int = 3) -> List[Tuple[str, str]]:
        """
        Get tickers with retry logic in case of network issues
        
        Args:
            max_retries: Maximum number of retry attempts
            
        Returns:
            List of tuples (ticker, company_name)
        """
        for attempt in range(max_retries):
            try:
                tickers_data = self.scrape_sp500_tickers()
                if tickers_data:
                    return tickers_data
                else:
                    logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(2)  # Wait 2 seconds before retry
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        
        logger.error("All attempts failed to scrape S&P 500 tickers")
        return []

def main():
    """Main function to test the scraper"""
    scraper = SP500Scraper()
    tickers_data = scraper.get_tickers_with_retry()
    
    if tickers_data:
        print(f"Successfully scraped {len(tickers_data)} S&P 500 tickers")
        print("\nFirst 10 tickers:")
        for i, (ticker, name) in enumerate(tickers_data[:10]):
            print(f"{i+1}. {ticker}: {name}")
        
        # Save to CSV
        scraper.save_tickers_to_csv(tickers_data)
    else:
        print("Failed to scrape S&P 500 tickers")

if __name__ == "__main__":
    main()
