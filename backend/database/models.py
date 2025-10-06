"""
Database models for the S&P 500 Stock Analysis Tool
"""

from sqlalchemy import create_engine, Column, String, Float, Date, Integer, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database configuration
DATABASE_URL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "database", "sp500_stocks.db")
DATABASE_URL = f"sqlite:///{DATABASE_URL}"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SP500Ticker(Base):
    """Model for S&P 500 ticker symbols and company names"""
    __tablename__ = "sp500_tickers"
    
    ticker = Column(String(10), primary_key=True)
    name = Column(String(200), nullable=False)
    
    def __repr__(self):
        return f"<SP500Ticker(ticker='{self.ticker}', name='{self.name}')>"

class StockData(Base):
    """Model for historical stock price data"""
    __tablename__ = "stock_data"
    
    date = Column(Date, nullable=False)
    ticker = Column(String(10), nullable=False)
    open_price = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    adj_close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    
    # Composite primary key to avoid duplicates
    __table_args__ = (
        PrimaryKeyConstraint('date', 'ticker'),
    )
    
    def __repr__(self):
        return f"<StockData(date='{self.date}', ticker='{self.ticker}', close={self.close})>"

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session():
    """Get a database session for direct use"""
    return SessionLocal()
