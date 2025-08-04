# 🚀 Deployment Guide for Streamlit Community Cloud

## 📋 Prerequisites

1. **GitHub Account**: You need a GitHub account
2. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **API Keys**: Collect your API keys (see Configuration section)

## 🔧 Setup Steps

### 1. Create GitHub Repository

```bash
# Initialize git repository (already done)
git init
git add .
git commit -m "Initial commit"

# Create new repository on GitHub.com
# Then link your local repo:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Configure API Keys

1. **Copy the example config**:
   ```bash
   cp config.json.example config.json
   ```

2. **Add your API keys** to `config.json`:
   - Polygon.io API key
   - Schwab API credentials (if using)
   - Alpaca API keys (if using)

3. **For Streamlit Cloud**: Add secrets in the Streamlit dashboard:
   - Go to your app settings
   - Add secrets in the "Secrets" section

### 3. Deploy to Streamlit Cloud

1. **Visit [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Select your repository**
5. **Set the main file path**: `ui/streamlit_app.py`
6. **Click "Deploy"**

## 🔐 Environment Variables for Streamlit Cloud

Add these to your Streamlit Cloud secrets:

```toml
[api_keys]
schwab_market_data_key = "your_key_here"
schwab_market_data_secret = "your_secret_here"
schwab_trading_key = "your_trading_key_here"
schwab_trading_secret = "your_trading_secret_here"
alpaca_api_key = "your_alpaca_key_here"
alpaca_secret_key = "your_alpaca_secret_here"
polygon_api_key = "your_polygon_key_here"
news_api_key = "your_news_key_here"

[schwab_auth]
client_id = "your_client_id_here"
client_secret = "your_client_secret_here"
redirect_uri = "https://developer.schwab.com/oauth2-redirect.html"
```

## 📁 File Structure for Deployment

```
options_scalping_project/
├── ui/
│   └── streamlit_app.py          # Main Streamlit app
├── data/
│   ├── data_fetcher.py           # Data fetching logic
│   ├── polygon_data.py           # Polygon.io integration
│   ├── midcap_screener.py        # Mid-cap stock screener
│   └── mock_data.py              # Mock data fallback
├── modules/
│   └── trade_executor.py         # Trading execution
├── signals/
│   └── technical_indicators.py   # Technical analysis
├── trading/
│   └── risk_manager.py           # Risk management
├── utils/
│   └── logger.py                 # Logging utilities
├── requirements.txt              # Python dependencies
├── config.json.example           # Example configuration
├── .gitignore                    # Git ignore rules
└── README.md                     # Project documentation
```

## 🚀 Features Available After Deployment

- ✅ **Real-time Market Data** (Polygon.io)
- ✅ **Mid-Cap Stock Screener** (185+ stocks analyzed)
- ✅ **Technical Indicators** (RSI, MACD, VWAP, etc.)
- ✅ **Stock Rankings** (Real-time analysis)
- ✅ **Signal Analysis** (Trading signals)
- ✅ **Performance Monitoring** (System metrics)
- ✅ **Mock Data Fallback** (When APIs are rate-limited)

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **API Rate Limits**: The app has built-in fallbacks to mock data
3. **Configuration Issues**: Check that secrets are properly set in Streamlit Cloud
4. **Memory Issues**: The app is optimized for Streamlit Cloud's memory limits

### Debug Commands:

```bash
# Test locally before deployment
streamlit run ui/streamlit_app.py

# Check dependencies
pip install -r requirements.txt

# Test data fetching
python -c "from data.data_fetcher import OptimizedDataFetcher; print('Data fetcher works!')"
```

## 📊 Performance Optimization

The app is optimized for Streamlit Cloud with:
- **Caching**: All data operations are cached
- **Async Processing**: Parallel data fetching
- **Rate Limiting**: Built-in API rate limit handling
- **Fallback Systems**: Multiple data sources with automatic fallback

## 🎯 Next Steps After Deployment

1. **Test all features** in the deployed app
2. **Configure your API keys** in Streamlit Cloud secrets
3. **Monitor performance** and adjust caching settings if needed
4. **Share your app** with others using the public URL

## 📞 Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify your API keys are correct
3. Test locally first
4. Check the `CURRENT_STATUS.md` file for known issues

---

**Happy Trading! 🚀📈** 