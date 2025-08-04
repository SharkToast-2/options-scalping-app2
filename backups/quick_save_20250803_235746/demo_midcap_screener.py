#!/usr/bin/env python3
"""
Demo: Mid-Cap Stock Screener
Shows the top 10 mid-cap stocks with growth potential
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import OptimizedDataFetcher
from data.midcap_screener import get_top_midcap_stocks
import pandas as pd

def demo_midcap_screener():
    """Demo the mid-cap stock screener"""
    print("🚀 Mid-Cap Growth Stock Screener Demo")
    print("=" * 60)
    print("Analyzing 185+ mid-cap stocks for growth potential...")
    print("Using Polygon.io real-time market data")
    print()
    
    # Initialize data fetcher
    data_fetcher = OptimizedDataFetcher(use_polygon=True)
    print(f"✅ Data Source: {data_fetcher.get_data_source()}")
    print()
    
    # Get top mid-cap stocks
    print("🔍 Screening stocks...")
    top_stocks = get_top_midcap_stocks(data_fetcher, max_workers=3)
    
    if not top_stocks:
        print("❌ No stocks found. This might be due to API rate limits.")
        return
    
    print(f"✅ Found {len(top_stocks)} stocks with growth potential")
    print()
    
    # Create a nice table
    print("🏆 TOP 10 MID-CAP GROWTH STOCKS")
    print("=" * 80)
    print(f"{'Rank':<4} {'Symbol':<6} {'Price':<8} {'Score':<6} {'RSI':<5} {'MACD':<8} {'Volume':<7} {'Momentum':<9}")
    print("-" * 80)
    
    for i, stock in enumerate(top_stocks, 1):
        print(f"{i:<4} {stock['symbol']:<6} ${stock['price']:<7.2f} {stock['growth_score']:<6.3f} "
              f"{stock['rsi']:<5.1f} {stock['macd']:<8.4f} {stock['volume_ratio']:<7.2f}x "
              f"{stock['momentum_pct']:<+9.1f}%")
    
    print()
    print("📊 GROWTH POTENTIAL BREAKDOWN")
    print("=" * 40)
    
    # Categorize stocks by growth potential
    excellent = [s for s in top_stocks if s['growth_score'] >= 0.7]
    good = [s for s in top_stocks if 0.5 <= s['growth_score'] < 0.7]
    moderate = [s for s in top_stocks if 0.3 <= s['growth_score'] < 0.5]
    
    if excellent:
        print("🎯 EXCELLENT GROWTH POTENTIAL (Score ≥ 0.7):")
        for stock in excellent:
            print(f"   • {stock['symbol']}: {stock['growth_score']:.3f} score "
                  f"(${stock['price']:.2f}, {stock['momentum_pct']:+.1f}% momentum)")
        print()
    
    if good:
        print("📈 GOOD GROWTH POTENTIAL (Score 0.5-0.7):")
        for stock in good:
            print(f"   • {stock['symbol']}: {stock['growth_score']:.3f} score "
                  f"(${stock['price']:.2f}, {stock['momentum_pct']:+.1f}% momentum)")
        print()
    
    if moderate:
        print("⚠️ MODERATE GROWTH POTENTIAL (Score 0.3-0.5):")
        for stock in moderate:
            print(f"   • {stock['symbol']}: {stock['growth_score']:.3f} score "
                  f"(${stock['price']:.2f}, {stock['momentum_pct']:+.1f}% momentum)")
        print()
    
    # Show best opportunity
    if top_stocks:
        best = top_stocks[0]
        print("🎯 BEST OPPORTUNITY:")
        print(f"   Symbol: {best['symbol']}")
        print(f"   Growth Score: {best['growth_score']:.3f}")
        print(f"   Current Price: ${best['price']:.2f}")
        print(f"   Momentum: {best['momentum_pct']:+.1f}%")
        print(f"   RSI: {best['rsi']:.1f}")
        print(f"   Volume Ratio: {best['volume_ratio']:.2f}x")
        print(f"   MACD: {best['macd']:.4f}")
    
    print()
    print("💡 NEXT STEPS:")
    print("   1. Open your Streamlit app to see this data in real-time")
    print("   2. Click on any stock for detailed technical analysis")
    print("   3. Monitor these stocks for potential entry points")
    print("   4. Use the growth score to prioritize your investments")
    print()
    print("🎉 Demo completed! Your mid-cap screener is working perfectly!")

if __name__ == "__main__":
    demo_midcap_screener() 