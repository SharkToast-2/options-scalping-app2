# 🚀 Options Scalping Application

A comprehensive real-time options scalping and stock analysis platform built with Streamlit, featuring advanced technical indicators, mid-cap stock screening, and multi-source market data integration.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

### 📊 **Real-Time Market Data**
- **Polygon.io Integration**: Primary data source for real-time quotes and historical data
- **Multi-Source Fallback**: Automatic fallback to yfinance and mock data
- **Rate Limit Handling**: Intelligent rate limiting with exponential backoff
- **Caching System**: Optimized caching for performance

### 🎯 **Mid-Cap Stock Screener**
- **185+ Mid-Cap Stocks**: Comprehensive analysis of growth potential
- **Technical Indicators**: RSI, MACD, Volume Analysis, Price Momentum, Bollinger Bands
- **Growth Scoring**: Weighted algorithm for growth potential assessment
- **Real-Time Updates**: Live data with refresh capabilities

### 📈 **Technical Analysis**
- **Advanced Indicators**: RSI, MACD, VWAP, EMA, Bollinger Bands, ADX, OBV, ATR, Stochastic RSI
- **Signal Generation**: Automated trading signals based on technical analysis
- **Performance Metrics**: Real-time performance tracking and analysis
- **Risk Management**: Built-in risk controls and position sizing

### 🤖 **Trading Integration**
- **Schwab API**: Full integration with Schwab trading platform
- **Alpaca Trading**: Alternative trading platform support
- **ThinkOrSwim**: TOS platform integration
- **Paper Trading**: Safe testing environment

### 🎨 **Modern UI/UX**
- **Streamlit Dashboard**: Beautiful, responsive web interface
- **Real-Time Updates**: Live data streaming and updates
- **Interactive Charts**: Plotly-powered interactive visualizations
- **Mobile Responsive**: Works on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- API Keys (Polygon.io, Schwab, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/options-scalping-app.git
   cd options-scalping-app
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   cp config.json.example config.json
   # Edit config.json with your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run ui/streamlit_app.py
   ```

## 📋 Configuration

### API Keys Setup

1. **Polygon.io** (Primary data source)
   - Sign up at [polygon.io](https://polygon.io)
   - Get your API key
   - Add to `config.json`

2. **Schwab Trading** (Optional)
   - Register at [Schwab Developer Portal](https://developer.schwab.com)
   - Get client ID and secret
   - Configure OAuth2 authentication

3. **Alpaca Trading** (Optional)
   - Sign up at [alpaca.markets](https://alpaca.markets)
   - Get API key and secret
   - Add to `config.json`

### Environment Variables

Create a `.env` file or use Streamlit Cloud secrets:

```bash
POLYGON_API_KEY=your_polygon_key_here
SCHWAB_CLIENT_ID=your_schwab_client_id
SCHWAB_CLIENT_SECRET=your_schwab_secret
ALPACA_API_KEY=your_alpaca_key
ALPACA_SECRET_KEY=your_alpaca_secret
```

## 🎯 Usage

### 1. **Mid-Cap Growth Screener**
- Navigate to the "🚀 Mid-Cap Growth" tab
- View top 10 mid-cap stocks with growth potential
- Analyze technical indicators and growth scores
- Refresh data for latest analysis

### 2. **Real-Time Market Data**
- Select stocks from the dropdown
- View live prices, volume, and technical indicators
- Monitor price changes and trends
- Export data for further analysis

### 3. **Technical Analysis**
- Choose stocks for detailed analysis
- View multiple technical indicators
- Generate trading signals
- Analyze historical performance

### 4. **Trading Signals**
- Review automated trading signals
- Set risk management parameters
- Monitor portfolio performance
- Execute trades (with proper authentication)

## 📊 Features in Detail

### Mid-Cap Stock Screener

The screener analyzes 185+ mid-cap stocks using a weighted scoring system:

- **RSI (25%)**: Relative Strength Index for momentum analysis
- **MACD (25%)**: Moving Average Convergence Divergence for trend analysis
- **Volume Analysis (20%)**: Volume ratio and market interest
- **Price Momentum (20%)**: 20-day price momentum analysis
- **Bollinger Bands (10%)**: Volatility and price position analysis

### Technical Indicators

- **RSI**: Relative Strength Index (14-period)
- **MACD**: Moving Average Convergence Divergence
- **VWAP**: Volume Weighted Average Price
- **EMA**: Exponential Moving Averages (12, 26 periods)
- **Bollinger Bands**: 20-period with 2 standard deviations
- **ADX**: Average Directional Index
- **OBV**: On-Balance Volume
- **ATR**: Average True Range
- **Stochastic RSI**: Stochastic Relative Strength Index

### Risk Management

- **Position Sizing**: Maximum 10% of portfolio per position
- **Daily Loss Limits**: 5% maximum daily loss
- **Stop Loss**: 2% automatic stop loss
- **Portfolio Monitoring**: Real-time risk assessment

## 🚀 Deployment

### Streamlit Community Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set main file: `ui/streamlit_app.py`
   - Add secrets in the dashboard

3. **Configure Secrets**
   ```toml
   [api_keys]
   polygon_api_key = "your_polygon_key_here"
   schwab_trading_key = "your_schwab_key_here"
   schwab_trading_secret = "your_schwab_secret_here"
   ```

### Local Development

```bash
# Run with debug mode
streamlit run ui/streamlit_app.py --logger.level debug

# Run on specific port
streamlit run ui/streamlit_app.py --server.port 8502
```

## 📁 Project Structure

```
options_scalping_project/
├── ui/
│   └── streamlit_app.py          # Main Streamlit application
├── data/
│   ├── data_fetcher.py           # Multi-source data fetching
│   ├── polygon_data.py           # Polygon.io integration
│   ├── midcap_screener.py        # Mid-cap stock analysis
│   └── mock_data.py              # Mock data fallback
├── modules/
│   └── trade_executor.py         # Trading execution logic
├── signals/
│   └── technical_indicators.py   # Technical analysis
├── trading/
│   └── risk_manager.py           # Risk management
├── utils/
│   └── logger.py                 # Logging utilities
├── config/
│   └── settings.py               # Configuration management
├── requirements.txt              # Python dependencies
├── config.json.example           # Example configuration
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🔧 API Integration

### Polygon.io
- **Real-time quotes**: Latest trade data
- **Historical data**: OHLCV data for technical analysis
- **Rate limiting**: 5 requests/minute (free tier)
- **Fallback**: Automatic fallback to yfinance

### Schwab Trading
- **OAuth2 Authentication**: Secure API access
- **Real-time quotes**: Live market data
- **Order execution**: Buy/sell orders
- **Account management**: Portfolio tracking

### Alpaca Trading
- **Paper trading**: Risk-free testing
- **Real-time data**: Live market feeds
- **Order management**: Advanced order types
- **Portfolio tracking**: Real-time positions

## 🛠️ Development

### Adding New Features

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Implement changes**
   - Follow PEP 8 coding standards
   - Add proper error handling
   - Include logging for debugging

3. **Test thoroughly**
   ```bash
   # Test data fetching
   python -c "from data.data_fetcher import OptimizedDataFetcher; print('OK')"
   
   # Test Streamlit app
   streamlit run ui/streamlit_app.py
   ```

4. **Submit pull request**
   - Include detailed description
   - Add screenshots if UI changes
   - Update documentation

### Code Style

- **Python**: Follow PEP 8 standards
- **Streamlit**: Use proper caching and state management
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Use structured logging throughout

## 📈 Performance Optimization

### Caching Strategy
- **Data caching**: 5-minute cache for market data
- **Indicator caching**: 10-minute cache for technical indicators
- **Streamlit caching**: Optimized with `@st.cache_data`

### Rate Limiting
- **Polygon.io**: 1-second delay between requests
- **yfinance**: Exponential backoff on rate limits
- **Fallback systems**: Automatic data source switching

### Memory Management
- **Data cleanup**: Automatic cleanup of old cache entries
- **Streamlit optimization**: Efficient data structures
- **Background processing**: Async operations for heavy tasks

## 🔒 Security

### API Key Protection
- **Environment variables**: Secure key storage
- **Git ignore**: Sensitive files excluded from version control
- **Streamlit secrets**: Cloud deployment security

### Data Privacy
- **No sensitive storage**: No personal data stored
- **Encrypted connections**: HTTPS for all API calls
- **Access controls**: Proper authentication required

## 🐛 Troubleshooting

### Common Issues

1. **API Rate Limits**
   - Solution: App automatically falls back to mock data
   - Check: API key validity and usage limits

2. **Import Errors**
   - Solution: Install all dependencies from `requirements.txt`
   - Check: Python version compatibility

3. **Streamlit Caching Issues**
   - Solution: Clear cache with `st.cache_data.clear()`
   - Check: Method signatures and parameters

4. **Data Not Loading**
   - Solution: Check API keys and network connection
   - Check: Fallback to mock data is working

### Debug Mode

```bash
# Run with debug logging
streamlit run ui/streamlit_app.py --logger.level debug

# Check API connections
python -c "from data.data_fetcher import OptimizedDataFetcher; df = OptimizedDataFetcher(); print(df.get_data_source_info())"
```

## 📞 Support

### Getting Help
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check `DEPLOYMENT.md` and `CURRENT_STATUS.md`
- **Community**: Join our Discord/Telegram for support

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Polygon.io**: Real-time market data
- **Streamlit**: Web application framework
- **yfinance**: Financial data library
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation

## 📊 Current Status

- ✅ **Real-time data**: Polygon.io integration working
- ✅ **Mid-cap screener**: 185+ stocks analyzed
- ✅ **Technical indicators**: All indicators implemented
- ✅ **Trading integration**: Schwab API configured
- ✅ **Performance optimization**: Caching and async processing
- ✅ **Deployment ready**: Streamlit Cloud compatible

---

**Happy Trading! 🚀📈**

*Disclaimer: This application is for educational and research purposes. Always do your own research and consider consulting with a financial advisor before making investment decisions.* 