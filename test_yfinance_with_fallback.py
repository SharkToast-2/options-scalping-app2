#!/usr/bin/env python3
"""
Test script for Yahoo Finance with fallback to mock data
"""

import sys
import os
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import DataFetcher
from signals.technical_indicators import TechnicalIndicators
from config.settings import TARGET_SYMBOLS

def create_mock_data(symbol, days=100):
    """Create realistic mock stock data"""
    np.random.seed(42)  # For reproducible results
    
    # Generate realistic stock data
    start_price = 150.0
    dates = pd.date_range(end=datetime.now(), periods=days, freq='1min')
    
    # Generate price movements
    returns = np.random.normal(0.0001, 0.01, days)  # 1-minute returns
    prices = [start_price]
    
    for i in range(1, days):
        new_price = prices[-1] * (1 + returns[i])
        prices.append(new_price)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Open': [p * (1 + np.random.normal(0, 0.002)) for p in prices],
        'High': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
        'Close': prices,
        'Volume': np.random.randint(100000, 5000000, days)
    }, index=dates)
    
    return data

def test_yfinance_with_fallback():
    """Test Yahoo Finance with fallback to mock data"""
    print("🚀 Testing Yahoo Finance with Fallback")
    print("=" * 50)
    
    # Initialize data fetcher
    print("📊 Initializing Data Fetcher...")
    data_fetcher = DataFetcher(use_schwab=False, use_alpaca=False)
    
    # Check data source
    data_source_info = data_fetcher.get_data_source_info()
    print(f"✅ Data Source: {data_source_info['name']}")
    print(f"📋 Description: {data_source_info['description']}")
    print(f"🔧 Status: {data_source_info['status']}")
    print(f"⚠️  Limitations: {data_source_info['limitations']}")
    print()
    
    # Test with a single symbol first
    test_symbol = "AAPL"
    print(f"🔍 Testing {test_symbol}...")
    
    # Try to get real data
    print("  📈 Attempting to fetch real data...")
    data = data_fetcher.get_stock_data(test_symbol, "1d", "5d")
    
    if data is not None and not data.empty:
        print(f"  ✅ Real data retrieved: {len(data)} bars")
        print(f"  📊 Latest price: ${data['Close'].iloc[-1]:.2f}")
        print(f"  📈 Volume: {data['Volume'].iloc[-1]:,}")
        print(f"  🕒 Latest timestamp: {data.index[-1]}")
        use_real_data = True
    else:
        print("  ⚠️  Real data unavailable, using mock data")
        data = create_mock_data(test_symbol, 100)
        print(f"  ✅ Mock data created: {len(data)} bars")
        print(f"  📊 Latest price: ${data['Close'].iloc[-1]:.2f}")
        use_real_data = False
    
    # Test technical indicators
    print(f"\n📊 Testing Technical Indicators...")
    
    try:
        indicators = TechnicalIndicators()
        
        # Calculate all indicators
        all_indicators = indicators.calculate_all_indicators(data)
        
        if all_indicators:
            print(f"  ✅ Indicators calculated successfully")
            
            # Show some key indicators
            if 'rsi' in all_indicators and not all_indicators['rsi'].empty:
                rsi_value = all_indicators['rsi'].iloc[-1]
                print(f"  📈 RSI: {rsi_value:.2f}")
            
            if 'macd' in all_indicators and not all_indicators['macd'].empty:
                macd_value = all_indicators['macd'].iloc[-1]
                print(f"  📊 MACD: {macd_value:.4f}")
            
            if 'vwap' in all_indicators and not all_indicators['vwap'].empty:
                vwap_value = all_indicators['vwap'].iloc[-1]
                print(f"  📉 VWAP: {vwap_value:.2f}")
            
            # Get signal summary
            signal_summary = indicators.get_signal_summary(all_indicators)
            print(f"  🎯 Signal Summary: {signal_summary}")
            
        else:
            print(f"  ❌ No indicators calculated")
            
    except Exception as e:
        print(f"  ❌ Error calculating indicators: {e}")
    
    # Test stock ranking with multiple symbols
    print(f"\n🏆 Testing Stock Ranking...")
    
    try:
        stock_data = {}
        indicators_data = {}
        current_prices = {}
        
        # Use a subset of symbols for testing
        test_symbols = TARGET_SYMBOLS[:3]
        
        for symbol in test_symbols:
            print(f"  🔍 Processing {symbol}...")
            
            if use_real_data:
                # Try real data first
                symbol_data = data_fetcher.get_stock_data(symbol, "1d", "5d")
                if symbol_data is None or symbol_data.empty:
                    print(f"    ⚠️  Using mock data for {symbol}")
                    symbol_data = create_mock_data(symbol, 100)
                else:
                    print(f"    ✅ Using real data for {symbol}")
            else:
                # Use mock data
                symbol_data = create_mock_data(symbol, 100)
                print(f"    📊 Using mock data for {symbol}")
            
            if symbol_data is not None and not symbol_data.empty:
                stock_data[symbol] = symbol_data
                current_prices[symbol] = symbol_data['Close'].iloc[-1]
                
                # Calculate indicators
                indicators_calc = indicators.calculate_all_indicators(symbol_data)
                indicators_data[symbol] = indicators_calc
        
        if stock_data and indicators_data and current_prices:
            # Rank stocks
            rankings = indicators.rank_stocks_for_scalping(stock_data, indicators_data, current_prices)
            
            if rankings:
                print(f"  ✅ Successfully ranked {len(rankings)} stocks")
                print("  📋 Rankings:")
                for i, ranking in enumerate(rankings):
                    print(f"    #{i+1} {ranking['symbol']}: {ranking['overall_score']:.1f}/100 - {ranking['recommendation']}")
                    print(f"        Direction: {ranking['signal_direction'].upper()} | Price: ${ranking['current_price']:.2f}")
                
                # Get best opportunities
                opportunities = indicators.get_best_scalping_opportunities(rankings, min_score=50.0, max_stocks=2)
                
                if opportunities:
                    print(f"\n  🎯 Best Scalping Opportunities:")
                    for opp in opportunities:
                        print(f"    • {opp['symbol']}: {opp['recommendation']}")
                        print(f"      Score: {opp['overall_score']:.1f}/100 | Direction: {opp['signal_direction'].upper()}")
            else:
                print(f"  ❌ No rankings generated")
        else:
            print(f"  ❌ Insufficient data for ranking")
            
    except Exception as e:
        print(f"  ❌ Error in stock ranking: {e}")
    
    print(f"\n🎉 Yahoo Finance with Fallback Test Completed!")
    print(f"📊 Data Source: {data_source_info['name']}")
    print(f"🔧 Data Type: {'Real' if use_real_data else 'Mock'}")

if __name__ == "__main__":
    test_yfinance_with_fallback() 