#!/usr/bin/env python3
"""
Debug script to test analysis functions
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.database.database_manager import DatabaseManager
from analysis.analysis_orchestrator import AnalysisOrchestrator
import pandas as pd

def test_analysis():
    print("🔍 Testing analysis functions...")
    
    # Initialize components
    db_manager = DatabaseManager()
    analysis_orchestrator = AnalysisOrchestrator()
    
    # Test getting stock data
    print("\n1. Testing stock data retrieval...")
    try:
        stock_data = db_manager.get_stock_data("AAPL")
        print(f"✅ Got stock data: {len(stock_data)} records")
        print(f"   Date range: {stock_data.index.min()} to {stock_data.index.max()}")
        print(f"   Columns: {list(stock_data.columns)}")
        print(f"   Index type: {type(stock_data.index)}")
    except Exception as e:
        print(f"❌ Error getting stock data: {e}")
        return
    
    # Test technical analysis
    print("\n2. Testing technical analysis...")
    try:
        tech_analysis = analysis_orchestrator.get_trend_analysis("AAPL")
        print(f"✅ Technical analysis result: {type(tech_analysis)}")
        if isinstance(tech_analysis, dict):
            print(f"   Keys: {list(tech_analysis.keys())}")
            if 'error' in tech_analysis:
                print(f"   Error: {tech_analysis['error']}")
    except Exception as e:
        print(f"❌ Error in technical analysis: {e}")
        import traceback
        traceback.print_exc()
    
    # Test comprehensive analysis
    print("\n3. Testing comprehensive analysis...")
    try:
        comp_analysis = analysis_orchestrator.get_comprehensive_analysis("AAPL")
        print(f"✅ Comprehensive analysis result: {type(comp_analysis)}")
        if isinstance(comp_analysis, dict):
            print(f"   Keys: {list(comp_analysis.keys())}")
            if 'error' in comp_analysis:
                print(f"   Error: {comp_analysis['error']}")
    except Exception as e:
        print(f"❌ Error in comprehensive analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analysis()
