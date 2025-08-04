# Schwab API Setup Guide

## 🔧 How to Add Your Schwab API Key

### Step 1: Get Your Schwab API Key
1. **Contact Schwab**: Call Schwab at 1-800-435-4000
2. **Request API Access**: Ask for API access for algorithmic trading
3. **Complete Application**: Fill out their API application form
4. **Get Credentials**: They will provide you with API key and documentation

### Step 2: Update Your Configuration

**Option A: Edit config.json directly**
```bash
# Open config.json in a text editor
nano config.json
```

Replace this line:
```json
"schwab": "YOUR_ACTUAL_SCHWAB_API_KEY_HERE",
```

With your actual API key:
```json
"schwab": "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz",
```

**Option B: Use the command line**
```bash
# Replace YOUR_ACTUAL_KEY with your real Schwab API key
sed -i '' 's/YOUR_ACTUAL_SCHWAB_API_KEY_HERE/YOUR_ACTUAL_KEY/g' config.json
```

### Step 3: Test Your Setup
```bash
python3 test_schwab_live_data.py
```

### Step 4: Run Your Application
```bash
python3 main.py
```

## 🚨 Important Notes

### If You Don't Have a Schwab API Key:
- **Schwab API is for institutional clients only**
- **Individual investors typically cannot get API access**
- **You may need to use alternative data sources**

### Alternative Data Sources (No API Key Required):
1. **Yahoo Finance** (Free, but rate limited)
2. **Alpha Vantage** (Free tier: 5 requests/minute)
3. **Finnhub** (Free tier: 60 requests/minute)

### If You Want to Use Alternative Sources:
The application will automatically fall back to Yahoo Finance if Schwab is not available.

## 🔍 Troubleshooting

### "API Key Not Found" Error:
- Make sure you replaced the placeholder text
- Check that the JSON format is correct
- Verify the API key is valid

### "Rate Limited" Error:
- Yahoo Finance has rate limits
- Wait a few minutes and try again
- Consider using a paid data source

### "Connection Failed" Error:
- Check your internet connection
- Verify the API endpoint is accessible
- Contact Schwab support if using their API

## 📞 Support

### Schwab API Support:
- **Phone**: 1-800-435-4000
- **Email**: api-support@schwab.com
- **Documentation**: https://developer.schwab.com

### Application Support:
- Check the README.md file
- Review the troubleshooting guides
- Test with alternative data sources

## 🎯 Quick Test

After updating your API key, run this test:

```bash
python3 test_schwab_live_data.py
```

You should see:
```
✅ Live Quote for AAPL:
   Price: $150.25
   Change: +1.25
   Volume: 1234567
   Data Source: schwab
```

If you see this, your live data is working! 🎉 