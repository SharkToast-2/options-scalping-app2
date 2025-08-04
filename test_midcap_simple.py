#!/usr/bin/env python3
"""
Simple Mid-Cap Stock Screener Test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import OptimizedDataFetcher
from data.midcap_screener import get_midcap_stock_analysis
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_simple_midcap():
    """Test the mid-cap stock screener with a few stocks"""
    print("🧪 Simple Mid-Cap Stock Screener Test")
    print("=" * 50)
    
    # Initialize data fetcher
    print("🔧 Initializing data fetcher...")
    data_fetcher = OptimizedDataFetcher(use_polygon=True)
    print(f"✅ Data source: {data_fetcher.get_data_source()}")
    
    # Test a few specific stocks
    test_symbols = ['AMD', 'NVDA', 'INTC', 'QCOM', 'AVGO']
    
    print(f"\n📈 Testing {len(test_symbols)} mid-cap stocks...")
    print("-" * 60)
    
    results = []
    for symbol in test_symbols:
        try:
            print(f"🔍 Analyzing {symbol}...")
            analysis = get_midcap_stock_analysis(symbol, data_fetcher)
            if analysis:
                results.append(analysis)
                print(f"✅ {symbol}: ${analysis['price']:.2f} (Score: {analysis['growth_score']:.3f})")
                print(f"   RSI: {analysis['rsi']:.1f}, MACD: {analysis['macd']:.4f}")
                print(f"   Volume: {analysis['volume_ratio']:.2f}x, Momentum: {analysis['momentum_pct']:+.1f}%")
            else:
                print(f"❌ {symbol}: No data available")
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")
    
    # Sort by growth score
    results.sort(key=lambda x: x['growth_score'], reverse=True)
    
    if results:
        print(f"\n🏆 Top Growth Stocks Found:")
        print("-" * 60)
        for i, stock in enumerate(results, 1):
            print(f"{i}. {stock['symbol']}: {stock['growth_score']:.3f} score "
                  f"(${stock['price']:.2f}, {stock['momentum_pct']:+.1f}% momentum)")
        
        # Show best opportunity
        best = results[0]
        print(f"\n🎯 Best Opportunity: {best['symbol']}")
        print(f"   Growth Score: {best['growth_score']:.3f}")
        print(f"   Current Price: ${best['price']:.2f}")
        print(f"   Momentum: {best['momentum_pct']:+.1f}%")
        print(f"   RSI: {best['rsi']:.1f}")
        print(f"   Volume Ratio: {best['volume_ratio']:.2f}x")
    else:
        print("\n❌ No stocks found with growth potential")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_simple_midcap() 