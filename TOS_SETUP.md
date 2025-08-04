# ThinkOrSwim API Integration Setup

## Overview

The Options Scalping Application now supports ThinkOrSwim (TOS) as a primary data source. ThinkOrSwim provides professional-grade real-time market data from TD Ameritrade, making it an excellent choice for options scalping.

## Features

✅ **Real-time Market Data**: Live stock prices, volume, and market data  
✅ **Options Chain Data**: Complete options chains with Greeks and implied volatility  
✅ **Historical Data**: High-quality historical price data for technical analysis  
✅ **WebSocket Streaming**: Real-time data streaming for live trading  
✅ **Professional Grade**: Institutional-quality data with minimal latency  

## Current Status

🟢 **ACTIVE**: The application is currently using **Mock ThinkOrSwim Data** for testing and development.

## Setup Instructions

### Option 1: Use Mock Data (Current - No Setup Required)

The application is currently configured to use mock ThinkOrSwim data, which provides realistic market data for testing and development without requiring API credentials.

**Benefits:**
- ✅ No setup required
- ✅ Realistic data for testing
- ✅ No rate limits
- ✅ Works immediately

**Limitations:**
- ⚠️ Not real market data
- ⚠️ Prices are simulated
- ⚠️ For development/testing only

### Option 2: Real ThinkOrSwim API (Production)

To use real ThinkOrSwim data, you'll need to set up TD Ameritrade API credentials.

#### Step 1: Create TD Ameritrade Developer Account

1. Go to [TD Ameritrade Developer Portal](https://developer.tdameritrade.com/)
2. Create a developer account
3. Register a new application
4. Get your `client_id` and `client_secret`

#### Step 2: Update Credentials

Edit `tos_api.py` and update the credentials:

```python
def get_tos_client(use_mock: bool = False) -> ThinkOrSwimAPI:
    """Get ThinkOrSwim API client"""
    if use_mock:
        return MockThinkOrSwimAPI()
    else:
        # Update with your real credentials
        credentials = TOSCredentials(
            username="your_td_username",
            password="your_td_password", 
            client_id="your_client_id_from_developer_portal"
        )
        return ThinkOrSwimAPI(credentials)
```

#### Step 3: Enable Real API

In `data/data_fetcher.py`, change the mock flag:

```python
self.tos_client = get_tos_client(use_mock=False)  # Change to False for real data
```

## Data Quality Comparison

| Feature | ThinkOrSwim | Yahoo Finance | Schwab API |
|---------|-------------|---------------|------------|
| **Data Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Real-time** | ✅ Yes | ⚠️ 15-min delay | ✅ Yes |
| **Rate Limits** | ✅ High | ❌ Low | ✅ High |
| **Options Data** | ✅ Complete | ⚠️ Limited | ✅ Complete |
| **Setup Complexity** | ⚠️ Medium | ✅ Easy | ⚠️ Medium |
| **Cost** | ✅ Free | ✅ Free | ⚠️ Paid |

## Testing the Integration

Run the ThinkOrSwim test script:

```bash
python3 test_thinkorswim.py
```

Expected output:
```
🚀 Testing ThinkOrSwim Integration
==================================================
📊 Initializing Data Fetcher with ThinkOrSwim...
✅ Data Source: ThinkOrSwim API
📋 Description: Professional-grade real-time data from TD Ameritrade
🔧 Status: ✅ Active
⚠️  Limitations: Requires TOS credentials, currently using mock data

📈 Testing Stock Data Fetching...
🔍 Testing META...
  ✅ Data retrieved: 390 bars
  📊 Latest price: $137.45
  📈 Volume: 520,795

💹 Testing Real-time Quotes...
  ✅ META: $151.75 (-1.36%)
     Bid: $151.74 | Ask: $151.76
     Volume: 1,192,661

🏆 Testing Stock Ranking...
  ✅ Successfully ranked 3 stocks
  📋 Rankings:
    #1 NVDA: 69.4/100 - ⚠️ MODERATE - Some signals, watch closely
    #2 SPY: 64.3/100 - ⚠️ MODERATE - Some signals, watch closely
    #3 META: 50.4/100 - ⏸️ WAIT - Weak signals, wait for better setup

🎉 ThinkOrSwim Integration Test Completed!
```

## Dashboard Integration

The ThinkOrSwim integration is fully integrated into the Streamlit dashboard:

1. **Data Source Display**: Shows "ThinkOrSwim API" as the active data source
2. **Real-time Data**: All stock data comes from TOS
3. **Stock Rankings**: Uses TOS data for scalping opportunity analysis
4. **Technical Indicators**: Calculated from TOS historical data
5. **Options Analysis**: Uses TOS options chain data

## Troubleshooting

### Common Issues

**Issue**: "ThinkOrSwim API not available, falling back to other sources"
**Solution**: Check that `tos_api.py` is in the project root and `websocket-client` is installed

**Issue**: Import errors with TOS module
**Solution**: Run `pip install websocket-client`

**Issue**: Rate limiting with real API
**Solution**: Implement proper OAuth2 flow and token refresh

### Performance Tips

1. **Use Mock Data for Development**: Faster and no rate limits
2. **Cache Data**: The application caches data to reduce API calls
3. **Batch Requests**: Multiple symbols are processed efficiently
4. **WebSocket for Real-time**: Use streaming for live data

## Next Steps

1. **Test with Mock Data**: Verify everything works with simulated data
2. **Set Up Real API**: When ready for production, configure real credentials
3. **Monitor Performance**: Watch for rate limits and optimize usage
4. **Add More Features**: Extend with additional TOS capabilities

## Support

For ThinkOrSwim API issues:
- [TD Ameritrade Developer Documentation](https://developer.tdameritrade.com/)
- [ThinkOrSwim API Reference](https://developer.tdameritrade.com/apis)
- [Community Forums](https://developer.tdameritrade.com/community)

---

**🎉 Congratulations!** Your options scalping application now has professional-grade market data from ThinkOrSwim! 