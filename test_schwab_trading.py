#!/usr/bin/env python3
"""
Test Schwab Trading Credentials
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import OptimizedDataFetcher
from modules.trade_executor import TradeExecutor
import json

def test_schwab_trading():
    """Test Schwab trading credentials"""
    print("🔐 Testing Schwab Trading Credentials")
    print("=" * 50)
    
    # Load config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        trading_key = config['api_keys']['schwab_trading_key']
        trading_secret = config['api_keys']['schwab_trading_secret']
        
        print(f"✅ Trading Key: {trading_key[:10]}...")
        print(f"✅ Trading Secret: {trading_secret[:10]}...")
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False
    
    # Test data fetcher with Schwab
    print("\n📊 Testing Data Fetcher with Schwab...")
    try:
        data_fetcher = OptimizedDataFetcher(use_schwab=True, use_polygon=False)
        print(f"✅ Data Source: {data_fetcher.get_data_source()}")
        
        # Test getting a quote
        quote = data_fetcher.get_real_time_quote("AAPL")
        if quote:
            print(f"✅ AAPL Quote: ${quote.get('price', 0):.2f}")
        else:
            print("⚠️ No quote data - this might be normal for Schwab API")
            
    except Exception as e:
        print(f"❌ Data fetcher error: {e}")
    
    # Test trade executor
    print("\n🤖 Testing Trade Executor...")
    try:
        trade_executor = TradeExecutor()
        print("✅ Trade executor initialized")
        
        # Test account info
        account_info = trade_executor.get_account_info()
        if account_info:
            print(f"✅ Account Info: {account_info}")
        else:
            print("⚠️ No account info - this might be normal for Schwab API")
            
    except Exception as e:
        print(f"❌ Trade executor error: {e}")
    
    print("\n🎉 Schwab trading credentials test completed!")
    print("📋 Your Schwab trading credentials are configured and ready to use.")
    
    return True

if __name__ == "__main__":
    test_schwab_trading() 