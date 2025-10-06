#!/usr/bin/env python3
"""
Demo script to showcase the S&P 500 Stock Analysis Tool
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.database.database_manager import DatabaseManager
from analysis.analysis_orchestrator import AnalysisOrchestrator
import pandas as pd
from datetime import datetime, date, timedelta
import json

def print_separator(title):
    """Print a formatted separator with title"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_subsection(title):
    """Print a formatted subsection title"""
    print(f"\n--- {title} ---")

def demo_data_overview():
    """Demonstrate data overview"""
    print_separator("DATABASE OVERVIEW")
    
    db_manager = DatabaseManager()
    
    # Get tickers
    tickers = db_manager.get_all_tickers()
    print(f"📊 Total S&P 500 Tickers: {len(tickers)}")
    
    # Get tickers with data
    tickers_with_data = db_manager.get_tickers_with_data()
    print(f"📈 Tickers with Historical Data: {len(tickers_with_data)}")
    
    # Show sample tickers
    print(f"\n🔍 Sample Tickers:")
    for i, (ticker, name) in enumerate(tickers[:5]):
        print(f"  {i+1}. {ticker}: {name}")
    
    # Check data freshness
    sample_ticker = tickers_with_data[0] if tickers_with_data else None
    if sample_ticker:
        latest_date = db_manager.get_latest_date(sample_ticker)
        print(f"\n📅 Latest Data Date for {sample_ticker}: {latest_date}")

def demo_stock_analysis(ticker="AAPL"):
    """Demonstrate comprehensive stock analysis"""
    print_separator(f"COMPREHENSIVE ANALYSIS: {ticker}")
    
    analysis_orchestrator = AnalysisOrchestrator()
    
    # Get comprehensive analysis
    analysis = analysis_orchestrator.get_comprehensive_analysis(ticker)
    
    if 'error' in analysis:
        print(f"❌ Error: {analysis['error']}")
        return
    
    # Data period info
    data_period = analysis.get('data_period', {})
    print(f"📊 Data Period: {data_period.get('start_date')} to {data_period.get('end_date')}")
    print(f"📈 Total Days: {data_period.get('total_days')}")
    
    # Technical Analysis
    print_subsection("Technical Analysis")
    tech_analysis = analysis.get('technical_analysis', {})
    current_indicators = tech_analysis.get('current_indicators', {})
    
    if current_indicators:
        print(f"💰 Current Price: ${current_indicators.get('current_price', 'N/A'):.2f}")
        print(f"📊 Daily Return: {current_indicators.get('daily_return', 0)*100:.2f}%")
        print(f"📈 RSI: {current_indicators.get('rsi', 'N/A'):.1f}")
        print(f"📉 MACD: {current_indicators.get('macd', 'N/A'):.3f}")
        print(f"📊 MA 20: ${current_indicators.get('ma_20', 'N/A'):.2f}")
        print(f"📊 MA 50: ${current_indicators.get('ma_50', 'N/A'):.2f}")
    
    # Seasonality Analysis
    print_subsection("Seasonality Analysis")
    seasonality = analysis.get('seasonality_analysis', {})
    summary = seasonality.get('summary', {})
    
    if summary:
        best_month = summary.get('best_month', {})
        worst_month = summary.get('worst_month', {})
        
        if best_month:
            print(f"🎯 Best Month: {best_month.get('month_name')} ({best_month.get('avg_return', 0)*100:.2f}%)")
        if worst_month:
            print(f"⚠️ Worst Month: {worst_month.get('month_name')} ({worst_month.get('avg_return', 0)*100:.2f}%)")
        
        strength = summary.get('seasonality_strength', 'unknown')
        print(f"📊 Seasonality Strength: {strength}")
    
    # Prediction Analysis
    print_subsection("AI Prediction")
    predictive = analysis.get('predictive_analysis', {})
    prediction = predictive.get('next_day_prediction', {})
    
    if prediction:
        pred_value = prediction.get('prediction', 'neutral')
        probability = prediction.get('probability', 0.5)
        confidence = prediction.get('confidence', 'medium')
        model = prediction.get('model_used', 'unknown')
        
        print(f"🤖 Prediction: {pred_value.upper()}")
        print(f"📊 Probability: {probability*100:.1f}%")
        print(f"🎯 Confidence: {confidence.upper()}")
        print(f"🧠 Model: {model}")
        
        # Feature importance
        feature_importance = predictive.get('feature_importance', {})
        if feature_importance:
            print(f"\n🔍 Top 3 Important Features:")
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            for i, (feature, importance) in enumerate(sorted_features[:3]):
                print(f"  {i+1}. {feature}: {importance:.3f}")
    
    # Analysis Summary
    print_subsection("Analysis Summary")
    analysis_summary = analysis.get('summary', {})
    
    if analysis_summary:
        sentiment = analysis_summary.get('overall_sentiment', 'neutral')
        confidence = analysis_summary.get('confidence_level', 'medium')
        
        print(f"🎭 Overall Sentiment: {sentiment.upper()}")
        print(f"🎯 Confidence Level: {confidence.upper()}")
        
        insights = analysis_summary.get('key_insights', [])
        if insights:
            print(f"\n💡 Key Insights:")
            for i, insight in enumerate(insights[:3]):
                print(f"  {i+1}. {insight}")
        
        recommendations = analysis_summary.get('recommendations', [])
        if recommendations:
            print(f"\n📋 Recommendations:")
            for i, rec in enumerate(recommendations[:2]):
                print(f"  {i+1}. {rec}")

def demo_multiple_tickers():
    """Demonstrate analysis for multiple tickers"""
    print_separator("MULTIPLE TICKER COMPARISON")
    
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    analysis_orchestrator = AnalysisOrchestrator()
    
    print(f"🔍 Analyzing {len(tickers)} popular stocks...")
    
    results = []
    
    for ticker in tickers:
        print(f"\n📊 Processing {ticker}...")
        
        # Get prediction only for speed
        prediction = analysis_orchestrator.get_prediction(ticker)
        
        if 'error' not in prediction:
            results.append({
                'ticker': ticker,
                'prediction': prediction.get('prediction', 'neutral'),
                'probability': prediction.get('probability', 0.5),
                'confidence': prediction.get('confidence', 'medium')
            })
        else:
            print(f"  ❌ Error: {prediction['error']}")
    
    # Display results
    if results:
        print_subsection("Comparison Results")
        print(f"{'Ticker':<8} {'Prediction':<10} {'Probability':<12} {'Confidence':<10}")
        print("-" * 45)
        
        for result in results:
            ticker = result['ticker']
            prediction = result['prediction'].upper()
            probability = f"{result['probability']*100:.1f}%"
            confidence = result['confidence'].upper()
            
            print(f"{ticker:<8} {prediction:<10} {probability:<12} {confidence:<10}")
        
        # Summary
        bullish_count = sum(1 for r in results if r['prediction'] == 'bullish')
        bearish_count = sum(1 for r in results if r['bearish'] == 'bearish')
        neutral_count = len(results) - bullish_count - bearish_count
        
        print(f"\n📈 Summary:")
        print(f"  Bullish: {bullish_count}")
        print(f"  Bearish: {bearish_count}")
        print(f"  Neutral: {neutral_count}")

def demo_seasonality_patterns():
    """Demonstrate seasonality patterns"""
    print_separator("SEASONALITY PATTERNS DEMO")
    
    analysis_orchestrator = AnalysisOrchestrator()
    ticker = "AAPL"
    
    print(f"📅 Analyzing seasonality patterns for {ticker}...")
    
    seasonality = analysis_orchestrator.get_seasonality_analysis(ticker)
    
    if 'error' in seasonality:
        print(f"❌ Error: {seasonality['error']}")
        return
    
    # Monthly patterns
    monthly_patterns = seasonality.get('monthly_patterns', {})
    if monthly_patterns:
        print_subsection("Monthly Performance Patterns")
        
        # Sort months by average return
        sorted_months = sorted(monthly_patterns.items(), 
                             key=lambda x: x[1].get('avg_return', 0), 
                             reverse=True)
        
        print(f"{'Month':<12} {'Avg Return':<12} {'Win Rate':<10} {'Total Days':<10}")
        print("-" * 50)
        
        for month_num, data in sorted_months:
            month_name = data.get('month_name', f'Month {month_num}')
            avg_return = data.get('avg_return', 0) * 100
            win_rate = data.get('win_rate', 0) * 100
            total_days = data.get('total_days', 0)
            
            print(f"{month_name:<12} {avg_return:>8.2f}% {win_rate:>8.1f}% {total_days:>8d}")
    
    # Quarterly patterns
    quarterly_patterns = seasonality.get('quarterly_patterns', {})
    if quarterly_patterns:
        print_subsection("Quarterly Performance Patterns")
        
        for quarter, data in quarterly_patterns.items():
            quarter_name = data.get('quarter_name', f'Q{quarter}')
            avg_return = data.get('avg_return', 0) * 100
            win_rate = data.get('win_rate', 0) * 100
            
            print(f"{quarter_name}: {avg_return:>6.2f}% avg return, {win_rate:>5.1f}% win rate")

def main():
    """Main demo function"""
    print_separator("S&P 500 STOCK ANALYSIS TOOL - DEMO")
    print("🚀 Welcome to the S&P 500 Stock Analysis Tool Demo!")
    print("📊 This demo showcases the key features and capabilities.")
    
    try:
        # 1. Database Overview
        demo_data_overview()
        
        # 2. Comprehensive Analysis
        demo_stock_analysis("AAPL")
        
        # 3. Multiple Ticker Comparison
        demo_multiple_tickers()
        
        # 4. Seasonality Patterns
        demo_seasonality_patterns()
        
        print_separator("DEMO COMPLETED")
        print("✅ Demo completed successfully!")
        print("🌐 To use the full interactive interface:")
        print("   1. Start the backend: cd backend && python api/run_server.py")
        print("   2. Start the frontend: cd frontend && npm start")
        print("   3. Open http://localhost:3000 in your browser")
        print("\n📚 For more information, see README.md and API_DOCUMENTATION.md")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("🔧 Please check your installation and try again.")
        print("📖 See SETUP.md for installation instructions.")

if __name__ == "__main__":
    main()
