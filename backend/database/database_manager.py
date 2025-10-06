"""
Database management functions for the S&P 500 Stock Analysis Tool
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from .models import Base, SP500Ticker, StockData, get_session
import pandas as pd
from datetime import datetime, date
import os

class DatabaseManager:
    """Handles all database operations for the stock analysis tool"""
    
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "database", "sp500_stocks.db")
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        # Create tables if they don't exist
        self.create_tables()
    
    def create_tables(self):
        """Create all database tables if they don't exist"""
        Base.metadata.create_all(bind=self.engine)
        print("Database tables created successfully!")
    
    def add_ticker(self, ticker: str, name: str):
        """Add a single ticker to the database"""
        session = self.SessionLocal()
        try:
            # Check if ticker already exists
            existing = session.query(SP500Ticker).filter(SP500Ticker.ticker == ticker).first()
            if existing:
                existing.name = name  # Update name if different
            else:
                new_ticker = SP500Ticker(ticker=ticker, name=name)
                session.add(new_ticker)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error adding ticker {ticker}: {e}")
        finally:
            session.close()
    
    def add_tickers_batch(self, tickers_data: list):
        """Add multiple tickers to the database in batch"""
        session = self.SessionLocal()
        try:
            for ticker, name in tickers_data:
                existing = session.query(SP500Ticker).filter(SP500Ticker.ticker == ticker).first()
                if existing:
                    existing.name = name
                else:
                    new_ticker = SP500Ticker(ticker=ticker, name=name)
                    session.add(new_ticker)
            session.commit()
            print(f"Added/updated {len(tickers_data)} tickers to database")
        except Exception as e:
            session.rollback()
            print(f"Error adding tickers batch: {e}")
        finally:
            session.close()
    
    def get_all_tickers(self):
        """Get all tickers from the database"""
        session = self.SessionLocal()
        try:
            tickers = session.query(SP500Ticker).all()
            return [(t.ticker, t.name) for t in tickers]
        except Exception as e:
            print(f"Error getting tickers: {e}")
            return []
        finally:
            session.close()
    
    def add_stock_data(self, ticker: str, data: pd.DataFrame):
        """Add stock data for a ticker to the database"""
        session = self.SessionLocal()
        try:
            # Convert DataFrame to list of StockData objects
            stock_records = []
            for _, row in data.iterrows():
                stock_record = StockData(
                    date=row.name.date() if hasattr(row.name, 'date') else row.name,
                    ticker=ticker,
                    open_price=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    adj_close=float(row['Adj Close']),
                    volume=int(row['Volume'])
                )
                stock_records.append(stock_record)
            
            # Use bulk operations for better performance
            session.bulk_insert_mappings(StockData, 
                                       [{'date': r.date, 'ticker': r.ticker, 
                                         'open_price': r.open_price, 'high': r.high, 
                                         'low': r.low, 'close': r.close, 
                                         'adj_close': r.adj_close, 'volume': r.volume} 
                                        for r in stock_records],
                                       render_nulls=True)
            session.commit()
            print(f"Added {len(stock_records)} records for {ticker}")
        except Exception as e:
            session.rollback()
            print(f"Error adding stock data for {ticker}: {e}")
        finally:
            session.close()
    
    def get_stock_data(self, ticker: str, start_date: date = None, end_date: date = None):
        """Get stock data for a ticker within a date range"""
        session = self.SessionLocal()
        try:
            query = session.query(StockData).filter(StockData.ticker == ticker)
            
            if start_date:
                query = query.filter(StockData.date >= start_date)
            if end_date:
                query = query.filter(StockData.date <= end_date)
            
            query = query.order_by(StockData.date)
            records = query.all()
            
            # Convert to DataFrame
            data = []
            for record in records:
                data.append({
                    'Date': record.date,
                    'Open': record.open_price,
                    'High': record.high,
                    'Low': record.low,
                    'Close': record.close,
                    'Adj Close': record.adj_close,
                    'Volume': record.volume
                })
            
            df = pd.DataFrame(data)
            if not df.empty:
                df.set_index('Date', inplace=True)
            return df
        except Exception as e:
            print(f"Error getting stock data for {ticker}: {e}")
            return pd.DataFrame()
        finally:
            session.close()
    
    def get_latest_date(self, ticker: str):
        """Get the latest date for a ticker in the database"""
        session = self.SessionLocal()
        try:
            latest = session.query(StockData.date).filter(
                StockData.ticker == ticker
            ).order_by(StockData.date.desc()).first()
            return latest[0] if latest else None
        except Exception as e:
            print(f"Error getting latest date for {ticker}: {e}")
            return None
        finally:
            session.close()
    
    def get_tickers_with_data(self):
        """Get list of tickers that have stock data in the database"""
        session = self.SessionLocal()
        try:
            tickers = session.query(StockData.ticker).distinct().all()
            return [t[0] for t in tickers]
        except Exception as e:
            print(f"Error getting tickers with data: {e}")
            return []
        finally:
            session.close()
    
    def update_stock_data(self, ticker: str, new_data: pd.DataFrame):
        """Update stock data for a ticker, adding only new records"""
        session = self.SessionLocal()
        try:
            # Get the latest date for this ticker
            latest_date = self.get_latest_date(ticker)
            
            if latest_date:
                # Filter new data to only include dates after the latest date
                new_data = new_data[new_data.index > pd.Timestamp(latest_date)]
            
            if not new_data.empty:
                # Add new data
                stock_records = []
                for _, row in new_data.iterrows():
                    stock_record = StockData(
                        date=row.name.date() if hasattr(row.name, 'date') else row.name,
                        ticker=ticker,
                        open_price=float(row['Open']),
                        high=float(row['High']),
                        low=float(row['Low']),
                        close=float(row['Close']),
                        adj_close=float(row['Adj Close']),
                        volume=int(row['Volume'])
                    )
                    stock_records.append(stock_record)
                
                session.bulk_insert_mappings(StockData, 
                                           [{'date': r.date, 'ticker': r.ticker, 
                                             'open_price': r.open_price, 'high': r.high, 
                                             'low': r.low, 'close': r.close, 
                                             'adj_close': r.adj_close, 'volume': r.volume} 
                                            for r in stock_records])
                session.commit()
                print(f"Updated {len(stock_records)} new records for {ticker}")
                return len(stock_records)
            else:
                print(f"No new data to update for {ticker}")
                return 0
        except Exception as e:
            session.rollback()
            print(f"Error updating stock data for {ticker}: {e}")
            return 0
        finally:
            session.close()

# Global database manager instance
db_manager = DatabaseManager()
