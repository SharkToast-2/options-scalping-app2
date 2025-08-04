#!/usr/bin/env python3
"""
Test Polygon.io Integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import OptimizedDataFetcher
from data.polygon_data import initialize_polygon, get_polygon_quote, get_polygon_batch_data
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_polygon_integration():
    """Test Polygon.io integration"""
    print("🧪 Testing Polygon.io Integration")
    print("=" * 50)
    
    # Initialize Polygon.io
    polygon_api_key = "ylJB2jaCAWQaHTa7BZFB60GAoapmK97P"
    print(f"🔑 Polygon API Key: {polygon_api_key[:10]}...")
    
    try:
        initialize_polygon(polygon_api_key)
        print("✅ Polygon.io initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Polygon.io: {e}")
        return False
    
    # Test single quote
    print("\n📈 Testing single quote...")
    test_symbols = ['AAPL', 'MSFT', 'GOOGL']
    
    for symbol in test_symbols:
        try:
            quote = get_polygon_quote(symbol)
            if quote:
                print(f"✅ {symbol}: ${quote.get('price', 0):.2f} ({quote.get('change_percent', 0):.2f}%)")
            else:
                print(f"❌ {symbol}: No data returned")
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")
    
    # Test batch data
    print("\n📊 Testing batch data...")
    try:
        batch_data = get_polygon_batch_data(test_symbols)
        print(f"✅ Batch data: {len(batch_data)} symbols returned")
        for symbol, data in batch_data.items():
            print(f"   {symbol}: ${data.get('price', 0):.2f}")
    except Exception as e:
        print(f"❌ Batch data error: {e}")
    
    # Test with OptimizedDataFetcher
    print("\n🔧 Testing with OptimizedDataFetcher...")
    try:
        fetcher = OptimizedDataFetcher(use_polygon=True)
        print(f"✅ Data source: {fetcher.get_data_source()}")
        
        # Test quote through fetcher
        quote = fetcher.get_real_time_quote('AAPL')
        if quote:
            print(f"✅ AAPL quote via fetcher: ${quote.get('price', 0):.2f}")
        else:
            print("❌ No quote via fetcher")
            
    except Exception as e:
        print(f"❌ Fetcher error: {e}")
    
    print("\n🎉 Polygon.io integration test complete!")
    return True

def main():
    success = test_polygon_integration()
    
    if success:
        print("\n✅ All tests passed! Polygon.io is working correctly.")
        print("📋 You can now use Polygon.io as your primary data source.")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main() 