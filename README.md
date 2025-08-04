# 🚀 Options Scalping Application

A sophisticated automated options scalping application with real-time market data analysis, technical indicators, and sentiment analysis. Built with Python, Streamlit, and multiple data sources including ThinkOrSwim, Yahoo Finance, and Alpaca.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Data Sources](#-data-sources)
- [Technical Indicators](#-technical-indicators)
- [API Setup](#-api-setup)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 Core Functionality
- **Real-time Market Data**: Live price feeds from multiple sources
- **Stock Ranking System**: AI-powered stock selection for scalping opportunities
- **Technical Analysis**: 9+ technical indicators for signal generation
- **Sentiment Analysis**: News sentiment integration for market context
- **Risk Management**: Automated position sizing and stop-loss management
- **Paper Trading**: Safe testing environment with simulated trades

### 📊 Technical Indicators
- **RSI (Relative Strength Index)**: Momentum oscillator
- **MACD (Moving Average Convergence Divergence)**: Trend following indicator
- **VWAP (Volume Weighted Average Price)**: Intraday price reference
- **EMA (Exponential Moving Averages)**: Trend identification
- **Bollinger Bands**: Volatility and price levels
- **ADX (Average Directional Index)**: Trend strength measurement
- **OBV (On-Balance Volume)**: Volume-price relationship
- **ATR (Average True Range)**: Volatility measurement
- **Stochastic RSI**: Momentum oscillator

### 🔌 Data Sources
- **ThinkOrSwim API**: Professional-grade real-time data
- **Yahoo Finance**: Free market data (fallback)
- **Alpaca API**: Real-time trading and data
- **Schwab API**: Professional market data
- **Alpha Vantage**: Alternative data source
- **Finnhub**: Market data and financial statements

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Git
- Virtual environment (recommended)

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
cp tos_config.py.example tos_config.py
# Edit the files with your API keys
```

5. **Run the application**
```bash
python main.py
```

The application will open in your browser at `http://localhost:8501`

## 📦 Installation

### Detailed Setup

1. **System Requirements**
   - Python 3.11+
   - 4GB RAM minimum
   - Stable internet connection
   - Modern web browser

2. **Dependencies Installation**
```bash
# Core dependencies
pip install streamlit pandas numpy plotly yfinance

# Trading and analysis
pip install alpaca-py ta scipy vaderSentiment

# Data sources
pip install requests newsapi-python python-dotenv

# Additional tools
pip install ccxt python-dateutil pytz websocket-client
```

3. **Configuration Files**
```bash
# Copy example configurations
cp config.json.example config.json
cp tos_config.py.example tos_config.py

# Edit with your settings
nano config.json
nano tos_config.py
```

## ⚙️ Configuration

### API Keys Setup

1. **ThinkOrSwim (Recommended)**
```python
# tos_config.py
TOS_CONFIG = {
    "use_real_api": True,
    "client_id": "your_client_id_here",
    "username": "your_td_username",
    "password": "your_td_password"
}
```

2. **Alpaca API**
```bash
export ALPACA_API_KEY="your_alpaca_key"
export ALPACA_SECRET_KEY="your_alpaca_secret"
```

3. **News API**
```bash
export NEWS_API_KEY="your_newsapi_key"
```

### Configuration Options

```json
{
  "api_keys": {
    "schwab": "your_schwab_api_key",
    "alpaca": "your_alpaca_api_key",
    "newsapi": "your_newsapi_key"
  },
  "default_symbols": ["META", "NVDA", "SPY", "TSLA", "MSFT"],
  "update_interval": 30,
  "risk_management": {
    "max_position_size": 0.1,
    "max_daily_loss": 0.05,
    "stop_loss": 0.02,
    "take_profit": 0.03
  }
}
```

## 🎮 Usage

### Manual Mode
1. **Stock Rankings**: View ranked stocks for scalping opportunities
2. **Signal Analysis**: Analyze technical indicators and signals
3. **Options Chain**: Browse available options contracts
4. **Trade History**: Review past trades and performance
5. **Performance Metrics**: Track trading performance

### Auto Trading Mode
1. **Enable Auto Trading**: Toggle automated trading
2. **Set Parameters**: Configure risk management settings
3. **Monitor**: Watch automated trades in real-time
4. **Performance**: Track automated trading results

### Key Features

#### Stock Ranking System
```python
# The app automatically ranks stocks based on:
- Technical indicator signals
- Volume and liquidity
- Volatility patterns
- Momentum strength
- Trend consistency
```

#### Risk Management
```python
# Built-in risk controls:
- Position size limits
- Daily loss limits
- Stop-loss orders
- Take-profit targets
- Maximum concurrent positions
```

## 📡 Data Sources

### Primary Sources
- **ThinkOrSwim**: Professional real-time data (120 req/min)
- **Alpaca**: Real-time trading and data (1000+ req/min)
- **Schwab**: Professional market data (100-1000 req/min)

### Fallback Sources
- **Yahoo Finance**: Free data (60-120 req/min)
- **Alpha Vantage**: Alternative data (5 req/min free)
- **Finnhub**: Market data (60 req/min free)

### Rate Limiting
The application includes intelligent rate limiting:
- Batch processing with delays
- Exponential backoff for retries
- Caching to reduce API calls
- Automatic fallback to available sources

## 📈 Technical Indicators

### Momentum Indicators
- **RSI**: Identifies overbought/oversold conditions
- **Stochastic RSI**: Momentum oscillator
- **MACD**: Trend following with signal line

### Trend Indicators
- **EMA**: Exponential moving averages
- **ADX**: Trend strength measurement
- **VWAP**: Volume-weighted average price

### Volatility Indicators
- **Bollinger Bands**: Price volatility and levels
- **ATR**: Average true range for volatility

### Volume Indicators
- **OBV**: On-balance volume for price-volume relationship

## 🔧 API Setup

### ThinkOrSwim Setup
1. Go to [TD Ameritrade Developer Portal](https://developer.tdameritrade.com/)
2. Create developer account
3. Register new application
4. Set callback URL: `http://localhost:8080/callback`
5. Copy Client ID to `tos_config.py`

### Alpaca Setup
1. Sign up at [Alpaca](https://alpaca.markets/)
2. Get API keys from dashboard
3. Set environment variables:
```bash
export ALPACA_API_KEY="your_key"
export ALPACA_SECRET_KEY="your_secret"
```

### Schwab Setup
1. Contact Schwab for API access
2. Get API credentials
3. Add to `config.json`

## 🚀 Deployment

### Local Development
```bash
# Run with Streamlit
streamlit run ui/streamlit_app.py --server.port 8501

# Run with Python
python main.py
```

### Docker Deployment
```bash
# Build Docker image
docker build -t options-scalping-app .

# Run container
docker run -p 8501:8501 options-scalping-app
```

### Cloud Deployment
- **Streamlit Cloud**: Connect GitHub repo
- **Heroku**: Use Procfile deployment
- **Railway**: Direct GitHub integration

## 📊 Performance

### Rate Limits
- **Optimized**: 40-50 requests/minute
- **Conservative**: 20-30 requests/minute
- **Emergency**: 10-15 requests/minute

### Caching
- **Data Cache**: 5-minute cache duration
- **Indicator Cache**: 1-minute cache duration
- **Quote Cache**: 30-second cache duration

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Commit changes: `git commit -m 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit pull request

### Code Standards
- Follow PEP 8 style guide
- Add type hints
- Include docstrings
- Write unit tests
- Update documentation

### Testing
```bash
# Run tests
python -m pytest tests/

# Run specific test
python test_stock_rankings.py
python test_thinkorswim.py
```

## 📚 Documentation

### Guides
- [Rate Limiting Guide](RATE_LIMITING_GUIDE.md)
- [ThinkOrSwim Setup](TOS_SETUP.md)
- [Schwab API Setup](SCHWAB_API_SETUP.md)
- [Deployment Guide](DEPLOYMENT.md)

### API Documentation
- [Data Fetcher API](data/data_fetcher.py)
- [Technical Indicators](signals/technical_indicators.py)
- [Risk Manager](trading/risk_manager.py)

## 🐛 Troubleshooting

### Common Issues

1. **Rate Limiting**
```bash
# Check current rate
python -c "from data.data_fetcher import DataFetcher; df = DataFetcher(); print(df.get_data_source_info())"
```

2. **Import Errors**
```bash
# Verify virtual environment
which python
pip list | grep streamlit
```

3. **API Connection Issues**
```bash
# Test API connections
python test_thinkorswim.py
python test_yfinance_with_fallback.py
```

### Debug Mode
```bash
# Run with debug logging
python -u main.py --debug

# Check logs
tail -f options_scalping.log
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Always consult with a financial advisor before making investment decisions.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework
- [yfinance](https://github.com/ranaroussi/yfinance) for Yahoo Finance data
- [TA-Lib](https://github.com/TA-Lib/ta-lib) for technical indicators
- [Alpaca](https://alpaca.markets/) for trading API
- [TD Ameritrade](https://developer.tdameritrade.com/) for market data

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/options-scalping-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/options-scalping-app/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/options-scalping-app/wiki)

---

**Made with ❤️ for the trading community** 