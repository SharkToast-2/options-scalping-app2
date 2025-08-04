# 🔑 Schwab API Setup Guide

## How to Add Your Schwab API Key

### **Step 1: Edit the Configuration File**

Open the `config.json` file in your project root and replace the placeholder with your actual Schwab API key:

```json
{
    "api_keys": {
        "schwab": "YOUR_ACTUAL_SCHWAB_API_KEY_HERE",
        "alpaca_api_key": "your_alpaca_api_key_here",
        "alpaca_secret_key": "your_alpaca_secret_key_here",
        "news_api_key": "your_news_api_key_here",
        "alpha_vantage": "your_alpha_vantage_api_key_here"
    }
}
```

### **Step 2: Get Your Schwab API Key**

1. **Log into your Schwab account**
2. **Navigate to API Access** (usually in Account Settings)
3. **Generate a new API key** or use an existing one
4. **Copy the API key** to your clipboard

### **Step 3: Update the Config File**

Replace `"YOUR_ACTUAL_SCHWAB_API_KEY_HERE"` with your real Schwab API key.

### **Step 4: Restart the Application**

After updating the config file, restart the Streamlit application:

```bash
# Stop the current application
pkill -f streamlit

# Restart the application
streamlit run ui/streamlit_app.py --server.headless true --browser.gatherUsageStats false
```

## **Benefits of Using Schwab API**

✅ **No Rate Limiting**: Unlike yfinance, Schwab API has higher rate limits  
✅ **Real-time Data**: Get live market data without delays  
✅ **Reliable**: Professional-grade API with better uptime  
✅ **Options Data**: Access to options chain data  
✅ **Account Integration**: Direct access to your Schwab account  

## **Data Source Priority**

The application will use data sources in this order:

1. **Schwab API** (if API key is provided)
2. **Alpaca API** (if API key is provided)
3. **yfinance** (fallback)

## **Troubleshooting**

### **If you get "API key not found" errors:**
- Make sure you've saved the `config.json` file
- Check that the API key is correctly formatted
- Restart the application after making changes

### **If you get "Schwab API error" messages:**
- Verify your API key is valid
- Check your Schwab account has API access enabled
- Ensure you're not hitting rate limits

### **If the app falls back to yfinance:**
- This is normal if Schwab API is unavailable
- The app will automatically retry Schwab API on the next request

## **Security Note**

⚠️ **Never commit your API keys to version control!**
- The `config.json` file should be in your `.gitignore`
- Keep your API keys secure and private
- Rotate your API keys regularly for security

## **Need Help?**

If you're having trouble with the Schwab API setup:
1. Check the `SCHWAB_API_GUIDE.md` file for detailed API documentation
2. Verify your Schwab account has API access enabled
3. Contact Schwab support if you need help with API access 