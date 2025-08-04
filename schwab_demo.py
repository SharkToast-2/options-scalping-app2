#!/usr/bin/env python3
"""
Schwab Integration Demo
"""

from modules.trade_executor import authenticate, get_account_info, open_account_summary, get_quote, place_order

def demo_schwab_integration():
    print("🔐 Schwab Integration Demo")
    print("=" * 50)
    
    # 1. Authenticate with Schwab
    print("\n1️⃣ Authenticating with Schwab...")
    success = authenticate()
    if success:
        print("✅ Authentication successful!")
    else:
        print("❌ Authentication failed")
        return
    
    # 2. Get account information
    print("\n2️⃣ Getting account information...")
    account_info = get_account_info()
    print(f"📊 Account URL: {account_info['account_url']}")
    print(f"🔗 Login URL: {account_info['login_url']}")
    print(f"🔐 Authenticated: {account_info['authenticated']}")
    print(f"📋 Status: {account_info['status']}")
    
    # 3. Open account summary
    print("\n3️⃣ Opening account summary...")
    open_account_summary()
    
    # 4. Test quote functionality
    print("\n4️⃣ Testing quote functionality...")
    quote = get_quote("AAPL")
    if quote:
        print(f"📈 AAPL Quote: ${quote.get('price', 'N/A')}")
    else:
        print("❌ No quote data available")
    
    # 5. Test order placement (mock)
    print("\n5️⃣ Testing order placement (mock)...")
    order = place_order("AAPL", 1, "buy", "market")
    if order:
        print("✅ Order placed successfully (mock)")
    else:
        print("❌ Order placement failed")
    
    print("\n🎉 Schwab integration demo complete!")
    print("\n📋 Available functions:")
    print("   - authenticate(): Authenticate with Schwab")
    print("   - get_account_info(): Get account information")
    print("   - open_account_summary(): Open account dashboard")
    print("   - get_quote(symbol): Get real-time quote")
    print("   - place_order(symbol, qty, side, type): Place trade order")

if __name__ == "__main__":
    demo_schwab_integration() 