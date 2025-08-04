#!/usr/bin/env python3
"""
Check current market prices from multiple sources
"""

import yfinance as yf
import requests
from datetime import datetime

def check_yahoo_prices():
    """Check current prices from Yahoo Finance"""
    print("📊 Checking Yahoo Finance Prices")
    print("=" * 40)
    
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get('regularMarketPrice', 0)
            previous_close = info.get('regularMarketPreviousClose', 0)
            change = current_price - previous_close if previous_close else 0
            
            print(f"{symbol}: ${current_price:.2f} ({change:+.2f})")
        except Exception as e:
            print(f"{symbol}: Error - {e}")

def check_schwab_prices():
    """Check current prices from Schwab API"""
    print("\n📊 Checking Schwab API Prices")
    print("=" * 40)
    
    try:
        from data.data_fetcher import DataFetcher
        
        data_fetcher = DataFetcher(use_schwab=True, use_alpaca=False, use_tos=False)
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
        
        for symbol in symbols:
            quote = data_fetcher.get_real_time_quote(symbol)
            if quote:
                price = quote.get('price', 0)
                print(f"{symbol}: ${price:.2f}")
            else:
                print(f"{symbol}: No data")
                
    except Exception as e:
        print(f"Error checking Schwab: {e}")

def check_market_status():
    """Check if market is open"""
    print("\n📈 Market Status")
    print("=" * 40)
    
    now = datetime.now()
    print(f"Current Time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Simple market hours check (9:30 AM - 4:00 PM ET, weekdays)
    if now.weekday() >= 5:  # Weekend
        print("🔴 Market: Closed (Weekend)")
    else:
        # This is a simplified check - in reality you'd need proper timezone handling
        current_time = now.time()
        market_open = datetime.strptime("09:30", "%H:%M").time()
        market_close = datetime.strptime("16:00", "%H:%M").time()
        
        if market_open <= current_time <= market_close:
            print("🟢 Market: Open")
        else:
            print("🔴 Market: Closed")

if __name__ == "__main__":
    print("🚀 Current Market Price Check")
    print("=" * 50)
    
    check_market_status()
    check_yahoo_prices()
    check_schwab_prices()
    
    print("\n" + "=" * 50)
    print("💡 Compare the prices above to see if Schwab API is accurate")
    print("📱 You can also check prices on your phone's stock app") 