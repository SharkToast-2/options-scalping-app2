#!/usr/bin/env python3
"""
Test script for stock ranking functionality
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import DataFetcher
from signals.technical_indicators import TechnicalIndicators
from config.settings import TARGET_SYMBOLS

def create_mock_data(symbol, days=100):
    """Create mock stock data for testing"""
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

def test_stock_rankings():
    """Test the stock ranking functionality"""
    print("🚀 Testing Stock Ranking System")
    print("=" * 50)
    
    # Initialize components
    data_fetcher = DataFetcher()
    indicators = TechnicalIndicators()
    
    # Test with mock data
    stock_data = {}
    indicators_data = {}
    current_prices = {}
    
    print("📊 Generating mock data for testing...")
    
    for symbol in TARGET_SYMBOLS[:3]:  # Test with first 3 symbols
        # Create mock data
        data = create_mock_data(symbol)
        stock_data[symbol] = data
        current_prices[symbol] = data['Close'].iloc[-1]
        
        # Calculate indicators
        indicators_calc = indicators.calculate_all_indicators(data)
        indicators_data[symbol] = indicators_calc
        
        print(f"✅ {symbol}: ${current_prices[symbol]:.2f}")
    
    print("\n🏆 Ranking stocks for scalping...")
    
    # Rank stocks
    rankings = indicators.rank_stocks_for_scalping(stock_data, indicators_data, current_prices)
    
    if rankings:
        print(f"\n📋 Found {len(rankings)} ranked stocks:")
        print("-" * 80)
        
        for i, ranking in enumerate(rankings):
            print(f"#{i+1} {ranking['symbol']}")
            print(f"   Overall Score: {ranking['overall_score']:.1f}/100")
            print(f"   Signal Direction: {ranking['signal_direction'].upper()}")
            print(f"   Current Price: ${ranking['current_price']:.2f}")
            print(f"   Signal Strength: {ranking['signal_strength']:.1f}%")
            print(f"   Volatility: {ranking['volatility']:.1f}%")
            print(f"   Volume: {ranking['volume']:.1f}%")
            print(f"   Recommendation: {ranking['recommendation']}")
            print()
        
        # Get best opportunities
        opportunities = indicators.get_best_scalping_opportunities(rankings, min_score=60.0, max_stocks=2)
        
        if opportunities:
            print("🎯 Best Scalping Opportunities:")
            print("-" * 40)
            for opp in opportunities:
                print(f"• {opp['symbol']}: {opp['recommendation']}")
                print(f"  Score: {opp['overall_score']:.1f}/100 | Direction: {opp['signal_direction'].upper()}")
        else:
            print("⚠️ No stocks meet the minimum score criteria")
    
    else:
        print("❌ No rankings generated")
    
    print("\n✅ Stock ranking test completed!")

if __name__ == "__main__":
    test_stock_rankings() 