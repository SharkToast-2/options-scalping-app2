# API Rate Limiting Guide

## Current Request Analysis

### **Expected Requests Per Minute:**

| Data Source | Current Rate | Limit | Status |
|-------------|-------------|-------|---------|
| **Yahoo Finance** | 200-250/min | 60-120/min | ❌ **EXCEEDED** |
| **Alpha Vantage** | 200-250/min | 5/min (free) | ❌ **EXCEEDED** |
| **Finnhub** | 200-250/min | 60/min (free) | ❌ **EXCEEDED** |
| **ThinkOrSwim** | 200-250/min | 120/min | ❌ **EXCEEDED** |

### **Request Breakdown:**

1. **Stock Rankings Tab**: 14 requests per load
2. **Real-time Updates**: Every 30 seconds (was 5 seconds)
3. **7 Symbols**: META, NVDA, SPY, TSLA, MSFT, HOOD, PLTR
4. **Total per minute**: ~40-50 requests (reduced from 200-250)

## Optimizations Applied

### **1. Increased Update Frequency**
```python
# Before
"UPDATE_FREQUENCY": 5,  # 5 seconds = 12 updates/minute

# After  
"UPDATE_FREQUENCY": 30, # 30 seconds = 2 updates/minute
```

### **2. Batch Processing**
```python
# Process symbols in smaller batches
"MAX_SYMBOLS_PER_BATCH": 3,  # Process 3 symbols at a time
"BATCH_DELAY": 2.0,          # 2-second delay between batches
```

### **3. Enhanced Rate Limiting**
```python
# Added delays between requests
time.sleep(batch_delay)           # Between individual requests
time.sleep(batch_delay * 2)       # Between batches
```

## Recommended Data Sources

### **For Production Use:**

1. **ThinkOrSwim API** (Recommended)
   - Rate Limit: 120 requests/minute
   - Real-time data
   - Professional-grade
   - Setup: Use OAuth2 authentication

2. **Alpaca API**
   - Rate Limit: 1000+ requests/minute
   - Real-time data
   - Free tier available
   - Setup: Get API key from Alpaca

3. **Schwab API**
   - Rate Limit: 100-1000 requests/minute
   - Real-time data
   - Professional-grade
   - Setup: Get API key from Schwab

### **For Development/Testing:**

1. **Yahoo Finance** (Current)
   - Rate Limit: 60-120 requests/minute
   - Free, no API key required
   - 15-minute delay for some data
   - **Status**: Working with optimizations

2. **Alpha Vantage**
   - Rate Limit: 5 requests/minute (free)
   - Paid plans available
   - **Status**: Too limited for current usage

3. **Finnhub**
   - Rate Limit: 60 requests/minute (free)
   - Paid plans available
   - **Status**: Too limited for current usage

## Configuration Options

### **Current Settings (Optimized):**
```python
DATA_CONFIG = {
    "UPDATE_FREQUENCY": 30,      # 30 seconds between updates
    "BATCH_DELAY": 2.0,          # 2 seconds between requests
    "MAX_SYMBOLS_PER_BATCH": 3,  # Process 3 symbols at a time
    "CACHE_DURATION": 300        # 5-minute cache
}
```

### **Conservative Settings (For Rate-Limited APIs):**
```python
DATA_CONFIG = {
    "UPDATE_FREQUENCY": 60,      # 1 minute between updates
    "BATCH_DELAY": 5.0,          # 5 seconds between requests
    "MAX_SYMBOLS_PER_BATCH": 2,  # Process 2 symbols at a time
    "CACHE_DURATION": 600        # 10-minute cache
}
```

### **Aggressive Settings (For High-Limit APIs):**
```python
DATA_CONFIG = {
    "UPDATE_FREQUENCY": 10,      # 10 seconds between updates
    "BATCH_DELAY": 0.5,          # 0.5 seconds between requests
    "MAX_SYMBOLS_PER_BATCH": 5,  # Process 5 symbols at a time
    "CACHE_DURATION": 120        # 2-minute cache
}
```

## Monitoring Rate Limits

### **Check Current Usage:**
```bash
# Monitor API requests
python3 -c "
from data.data_fetcher import DataFetcher
import time

df = DataFetcher()
start_time = time.time()
quotes = df.get_market_data_batch(['AAPL', 'MSFT', 'GOOGL'])
end_time = time.time()

print(f'Requests: {len(quotes)}')
print(f'Time: {end_time - start_time:.2f} seconds')
print(f'Rate: {len(quotes) / (end_time - start_time) * 60:.1f} requests/minute')
"
```

### **Test Different Data Sources:**
```bash
# Test ThinkOrSwim
python3 test_thinkorswim.py

# Test Yahoo Finance
python3 test_yfinance_with_fallback.py

# Test Alpha Vantage
python3 -c "from alternative_data_sources import AlphaVantageAPI; av = AlphaVantageAPI(); print(av.get_real_time_quote('AAPL'))"
```

## Troubleshooting

### **Rate Limit Errors:**
- **Yahoo Finance**: "Too Many Requests"
- **Alpha Vantage**: "API call frequency limit exceeded"
- **Finnhub**: "Rate limit exceeded"

### **Solutions:**
1. **Increase delays** in `DATA_CONFIG`
2. **Reduce batch size** to `MAX_SYMBOLS_PER_BATCH: 1`
3. **Switch to paid API** with higher limits
4. **Use caching** to reduce redundant requests

### **Emergency Settings (When Rate Limited):**
```python
# Add to config/settings.py for emergency use
EMERGENCY_CONFIG = {
    "UPDATE_FREQUENCY": 120,     # 2 minutes between updates
    "BATCH_DELAY": 10.0,         # 10 seconds between requests
    "MAX_SYMBOLS_PER_BATCH": 1,  # Process 1 symbol at a time
    "USE_MOCK_DATA": True        # Fall back to mock data
}
```

## Next Steps

1. **Set up ThinkOrSwim API** for production use
2. **Configure OAuth2 authentication** using the callback URL
3. **Test with real API credentials**
4. **Monitor request rates** in production
5. **Adjust settings** based on actual usage patterns

## Callback URL for ThinkOrSwim:
```
http://localhost:8080/callback
```

Set this in your TD Ameritrade developer application for OAuth2 authentication. 