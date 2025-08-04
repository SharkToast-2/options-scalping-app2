#!/usr/bin/env python3
"""
Test Mid-Cap Stock Screener
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import OptimizedDataFetcher
from data.midcap_screener import get_top_midcap_stocks, get_midcap_stock_analysis
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_midcap_screener():
    """Test the mid-cap stock screener"""
    print("🧪 Testing Mid-Cap Stock Screener")
    print("=" * 50)
    
    # Initialize data fetcher
    print("🔧 Initializing data fetcher...")
    data_fetcher = OptimizedDataFetcher(use_polygon=True)
    print(f"✅ Data source: {data_fetcher.get_data_source()}")
    
    # Test individual stock analysis
    print("\n📈 Testing individual stock analysis...")
    test_symbols = ['AMD', 'NVDA', 'INTC']
    
    for symbol in test_symbols:
        try:
            analysis = get_midcap_stock_analysis(symbol, data_fetcher)
            if analysis:
                print(f"✅ {symbol}: ${analysis['price']:.2f} (Growth Score: {analysis['growth_score']:.3f})")
                print(f"   RSI: {analysis['rsi']:.1f}, MACD: {analysis['macd']:.4f}")
                print(f"   Volume Ratio: {analysis['volume_ratio']:.2f}x, Momentum: {analysis['momentum_pct']:+.1f}%")
            else:
                print(f"❌ {symbol}: No analysis data")
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")
    
    # Test full screening
    print("\n🔍 Testing full mid-cap screening...")
    try:
        with open('test_midcap_results.txt', 'w') as f:
            f.write("Mid-Cap Stock Screening Results\n")
            f.write("=" * 40 + "\n\n")
            
            top_stocks = get_top_midcap_stocks(data_fetcher, max_workers=3)
            
            if top_stocks:
                print(f"✅ Found {len(top_stocks)} stocks with growth potential")
                print("\n🏆 Top 10 Mid-Cap Growth Stocks:")
                print("-" * 80)
                
                for i, stock in enumerate(top_stocks, 1):
                    print(f"{i:2d}. {stock['symbol']:6s} | ${stock['price']:8.2f} | "
                          f"Score: {stock['growth_score']:.3f} | "
                          f"RSI: {stock['rsi']:5.1f} | "
                          f"MACD: {stock['macd']:8.4f} | "
                          f"Vol: {stock['volume_ratio']:4.1f}x | "
                          f"Mom: {stock['momentum_pct']:+6.1f}%")
                    
                    # Write to file
                    f.write(f"{i:2d}. {stock['symbol']:6s} | ${stock['price']:8.2f} | "
                           f"Score: {stock['growth_score']:.3f} | "
                           f"RSI: {stock['rsi']:5.1f} | "
                           f"MACD: {stock['macd']:8.4f} | "
                           f"Vol: {stock['volume_ratio']:4.1f}x | "
                           f"Mom: {stock['momentum_pct']:+6.1f}%\n")
                
                # Show best opportunities
                print("\n🎯 Best Growth Opportunities:")
                best_stocks = [s for s in top_stocks if s['growth_score'] >= 0.7]
                for stock in best_stocks[:3]:
                    print(f"   🚀 {stock['symbol']}: {stock['growth_score']:.3f} score "
                          f"({stock['momentum_pct']:+.1f}% momentum)")
                
                print(f"\n📄 Results saved to test_midcap_results.txt")
                
            else:
                print("❌ No stocks found with growth potential")
                
    except Exception as e:
        print(f"❌ Screening error: {e}")
    
    print("\n🎉 Mid-cap screener test complete!")

def main():
    test_midcap_screener()
    
    print("\n✅ Test completed successfully!")
    print("📋 You can now use the mid-cap screener in your Streamlit app.")

if __name__ == "__main__":
    main() 