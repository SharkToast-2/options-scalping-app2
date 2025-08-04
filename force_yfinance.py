#!/usr/bin/env python3
"""
Force yfinance data fetching to test if it works
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

def test_yfinance():
    print("🔍 Testing yfinance directly...")
    
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
    
    for symbol in symbols:
        try:
            print(f"\n📊 Testing {symbol}...")
            
            # Get ticker info
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current_price = info.get('regularMarketPrice', 0)
            previous_close = info.get('regularMarketPreviousClose', current_price)
            change = current_price - previous_close if previous_close else 0
            change_percent = (change / previous_close * 100) if previous_close else 0
            
            print(f"   Current Price: ${current_price}")
            print(f"   Previous Close: ${previous_close}")
            print(f"   Change: ${change:.2f} ({change_percent:.2f}%)")
            print(f"   Volume: {info.get('volume', 0):,}")
            
            # Get historical data
            hist = ticker.history(period="1d", interval="1m")
            if not hist.empty:
                print(f"   Latest Close: ${hist['Close'].iloc[-1]:.2f}")
                print(f"   Data Points: {len(hist)}")
            else:
                print("   No historical data available")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_yfinance() 