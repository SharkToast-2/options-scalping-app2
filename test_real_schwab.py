#!/usr/bin/env python3
"""
Test if Schwab API is actually connecting to real endpoints
"""

import requests
import json
from datetime import datetime

def test_schwab_api_endpoints():
    """Test if Schwab API endpoints are accessible"""
    
    print("🔍 Testing Schwab API Endpoints")
    print("=" * 50)
    
    # Load API key
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            api_key = config.get('api_keys', {}).get('schwab', '')
    except Exception as e:
        print(f"Error loading config: {e}")
        return
    
    print(f"API Key: {api_key[:10]}..." if len(api_key) > 10 else "No API key")
    
    # Test Schwab API endpoints
    base_url = "https://api.schwab.com"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Quotes endpoint
    print("\n📊 Testing Quotes Endpoint...")
    try:
        url = f"{base_url}/v1/quotes/AAPL"
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Historical data endpoint
    print("\n📈 Testing Historical Data Endpoint...")
    try:
        url = f"{base_url}/v1/history/AAPL"
        params = {
            'startDate': '2025-07-01',
            'endDate': '2025-07-31',
            'interval': '1d'
        }
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")

def test_alternative_data_sources():
    """Test alternative data sources for comparison"""
    
    print("\n🔄 Testing Alternative Data Sources")
    print("=" * 50)
    
    # Test Yahoo Finance
    print("\n📊 Testing Yahoo Finance...")
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        current_price = info.get('regularMarketPrice', 0)
        print(f"AAPL Current Price (Yahoo): ${current_price:.2f}")
    except Exception as e:
        print(f"Yahoo Finance Error: {e}")
    
    # Test Alpha Vantage (if you have a key)
    print("\n📊 Testing Alpha Vantage...")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            alpha_key = config.get('api_keys', {}).get('alpha_vantage', '')
        
        if alpha_key and alpha_key != "your_alpha_vantage_api_key_here":
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={alpha_key}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                price = quote.get('05. price', 0)
                print(f"AAPL Current Price (Alpha Vantage): ${price}")
            else:
                print("No data from Alpha Vantage")
        else:
            print("Alpha Vantage API key not configured")
    except Exception as e:
        print(f"Alpha Vantage Error: {e}")

def check_market_status():
    """Check if market is currently open"""
    print("\n📈 Market Status")
    print("=" * 30)
    
    now = datetime.now()
    print(f"Current Time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Check if it's a weekday
    if now.weekday() >= 5:
        print("🔴 Market: Closed (Weekend)")
        print("💡 This might explain why Schwab API isn't returning real-time data")
    else:
        print("🟢 Market: Should be open (weekday)")
        print("💡 If market is closed, Schwab API might return delayed data")

if __name__ == "__main__":
    print("🚀 Schwab API Real Endpoint Test")
    print("=" * 50)
    
    check_market_status()
    test_schwab_api_endpoints()
    test_alternative_data_sources()
    
    print("\n" + "=" * 50)
    print("💡 If Schwab API endpoints return errors, the API might be:")
    print("   1. Not publicly available yet")
    print("   2. Requiring special registration")
    print("   3. Using different endpoints")
    print("   4. Requiring different authentication")
    
    print("\n🔄 Recommendation:")
    print("   Use Yahoo Finance or Alpha Vantage for real-time data")
    print("   Update the data fetcher to prioritize these sources") 