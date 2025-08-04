#!/usr/bin/env python3
"""
Debug script to test Schwab API integration in Streamlit context
"""

import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_schwab_in_streamlit_context():
    """Test Schwab API in the same context as Streamlit app"""
    
    print("🔍 Testing Schwab API in Streamlit Context")
    print("=" * 50)
    
    try:
        # Import the same modules used in Streamlit app
        from data.data_fetcher import DataFetcher
        from signals.technical_indicators import TechnicalIndicators
        
        print("📊 Initializing Data Fetcher (same as Streamlit)...")
        data_fetcher = DataFetcher(use_schwab=True, use_alpaca=False, use_tos=False)
        
        print(f"✅ Data Source: {data_fetcher.get_data_source()}")
        
        # Test with symbols used in the app
        test_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
        
        for symbol in test_symbols:
            print(f"\n🔍 Testing {symbol}...")
            
            # Test real-time quote
            quote = data_fetcher.get_real_time_quote(symbol)
            if quote:
                print(f"✅ Quote: ${quote.get('price', 'N/A')}")
            else:
                print(f"❌ No quote data")
            
            # Test stock data
            data = data_fetcher.get_stock_data(symbol, "1m", "1d")
            if data is not None and not data.empty:
                print(f"✅ Stock Data: ${data['Close'].iloc[-1]:.2f} ({len(data)} points)")
            else:
                print(f"❌ No stock data")
        
        # Test batch data
        print(f"\n🔄 Testing batch data...")
        batch_data = data_fetcher.get_market_data_batch(test_symbols)
        if batch_data:
            print(f"✅ Batch Data Retrieved:")
            for symbol, quote in batch_data.items():
                if quote:
                    print(f"   {symbol}: ${quote.get('price', 'N/A')}")
                else:
                    print(f"   {symbol}: ❌ No data")
        else:
            print("❌ No batch data retrieved")
        
        # Test technical indicators
        print(f"\n📈 Testing technical indicators...")
        indicators = TechnicalIndicators()
        
        # Get data for one symbol
        data = data_fetcher.get_stock_data("AAPL", "1m", "1d")
        if data is not None and not data.empty:
            all_indicators = indicators.calculate_all_indicators(data)
            print(f"✅ Indicators calculated: {list(all_indicators.keys())}")
            
            # Test stock ranking
            stock_data = {"AAPL": data}
            indicators_data = {"AAPL": all_indicators}
            current_prices = {"AAPL": data['Close'].iloc[-1]}
            
            rankings = indicators.rank_stocks_for_scalping(stock_data, indicators_data, current_prices)
            if rankings:
                print(f"✅ Stock rankings calculated: {len(rankings)} stocks")
                for rank in rankings[:3]:  # Show top 3
                    print(f"   {rank['symbol']}: Score {rank['overall_score']:.1f}")
            else:
                print("❌ No rankings calculated")
        else:
            print("❌ No data for indicator testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in Streamlit context test: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_config():
    """Check the current configuration"""
    print("\n📋 Configuration Check")
    print("=" * 30)
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            schwab_key = config.get('api_keys', {}).get('schwab', '')
            print(f"Schwab API Key: {schwab_key[:10]}..." if len(schwab_key) > 10 else "Not set")
    except Exception as e:
        print(f"Error reading config: {e}")

if __name__ == "__main__":
    print("🚀 Schwab API Streamlit Context Debug")
    print("=" * 50)
    
    check_config()
    success = test_schwab_in_streamlit_context()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Schwab API should work in Streamlit")
        print("💡 If prices still don't update, try refreshing the browser")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    print("\n📋 Next Steps:")
    print("1. Open http://localhost:8501 in your browser")
    print("2. Check the 'Data Source' section in the sidebar")
    print("3. Look for '✅ Using Schwab API as data source'")
    print("4. Try refreshing the page if data doesn't update") 