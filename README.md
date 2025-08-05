# 📈 Options Scalping Bot (Automated with Schwab API)

This is a real-time momentum-based options scalping bot built with Python. It uses technical indicators, sentiment filters, and Schwab API integration to automatically detect short-term trade opportunities and execute them securely.

---

## 🚀 Features

- ✅ Trades options for high-volume tickers (e.g., $META, $AAPL, $TSLA)
- ✅ One trade at a time, up to **$500 per trade**
- ✅ Stops trading if daily loss hits **$500 max**
- ✅ Closes trades on **3–5% gain or loss**
- ✅ Securely integrates with Schwab API using OAuth2
- ✅ Saves and refreshes tokens automatically
- ✅ Designed for low-latency 1-minute scalping
- ✅ Modular, beginner-friendly codebase (Python 3.9+)
- ✅ Real-time Streamlit dashboard for monitoring
- ✅ Comprehensive logging and performance tracking

---

## 📂 Project Structure

```
options_scalping_project/
├── app.py                     # Main Streamlit dashboard
├── bot.py                     # Automated trading bot
├── config/
│   └── env_config.py         # Environment configuration
├── data/
│   └── market_data.py        # Market data fetching
├── modules/
│   └── schwab_auth.py        # Schwab authentication
├── signals/
│   ├── technical_indicators.py # Technical analysis
│   └── sentiment_analysis.py   # Sentiment analysis
├── utils/
│   └── logger.py             # Logging utilities
├── requirements.txt          # Dependencies
├── schwab_backup.json        # Schwab credentials backup
└── README.md                # This file
```

---

## 🛠️ Quick Start

### Prerequisites
- Python 3.9+
- Schwab API credentials
- Internet connection for real-time data

### Installation

1. **Clone and setup:**
   ```bash
   git clone <repository>
   cd options_scalping_project
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Schwab API:**
   - Your credentials are already configured in `config/env_config.py`
   - Use the authentication interface in the dashboard

3. **Run the dashboard:**
   ```bash
   streamlit run app.py
   ```
   - Open: http://localhost:8501 (or 8502 if 8501 is busy)

4. **Run the bot (optional):**
   ```bash
   python3 bot.py
   ```

---

## 📊 Dashboard Features

### Real-time Monitoring
- **Market Data Tab**: Live prices, volume, and technical indicators
- **Analysis Tab**: Interactive charts with RSI, MACD, Bollinger Bands
- **Signals Tab**: Automated trading signals with confidence scores
- **Schwab Auth Tab**: OAuth2 authentication and API key management

### Interactive Controls
- Symbol selection (META, AAPL, TSLA, NVDA, SPY, QQQ)
- Time period adjustment (1d to 1y)
- Real-time data refresh
- Manual authentication setup

---

## 🤖 Bot Features

### Automated Trading
- **Continuous Monitoring**: Scans markets every minute
- **Signal Generation**: Combines technical and sentiment analysis
- **Risk Management**: Position sizing and stop losses
- **Performance Tracking**: Win rate, P&L, trade history

### Trading Strategy
- **Entry Conditions**:
  - RSI < 30 (oversold)
  - MACD bullish crossover
  - Price below lower Bollinger Band
  - Volume > 1.5x average
  - Positive sentiment score

- **Exit Conditions**:
  - 3-5% profit target
  - 3-5% stop loss
  - 5-minute time limit
  - Signal reversal

### Risk Management
- **Position Sizing**: Maximum $500 per trade
- **Daily Limits**: $500 maximum daily loss
- **Stop Losses**: Automatic 3-5% stops
- **One Trade at a Time**: Prevents overexposure

---

## 🔐 Schwab API Integration

### Authentication Flow
1. **OAuth2 Authorization**: Secure token-based authentication
2. **Token Management**: Automatic refresh and storage
3. **API Endpoints**: Real-time quotes, order placement, account info
4. **Error Handling**: Graceful fallbacks and retry logic

### Current Status
- ✅ **Credentials Configured**: All API keys and secrets loaded
- ✅ **OAuth2 URLs**: Authorization and token endpoints set
- ✅ **Authentication Interface**: Manual and automatic auth options
- 🔄 **Order Execution**: Simulated (ready for live trading)

### API Endpoints Used
- `/oauth/authorize` - Authentication
- `/oauth/token` - Token exchange
- `/trading/v1/accounts` - Account information
- `/trading/v1/orders` - Order placement
- `/marketdata/v1/quotes` - Real-time quotes

---

## 📈 Technical Indicators

### Core Indicators
- **RSI (14)**: Momentum oscillator (0-100)
- **MACD (12,26,9)**: Trend following with signal line
- **Bollinger Bands (20,2)**: Volatility and price position
- **Moving Averages**: SMA 20/50, EMA 12/26
- **Volume Analysis**: Volume SMA and ratio
- **ATR (14)**: Average True Range for volatility
- **VWAP**: Volume Weighted Average Price

### Signal Generation
- **Buy Signals**: RSI oversold, MACD bullish, price below BB
- **Sell Signals**: RSI overbought, MACD bearish, price above BB
- **Confidence Scoring**: Weighted combination of indicators
- **Volume Confirmation**: High volume validates signals

---

## 🎯 Target Tickers

### High-Volume Options
- **META**: Meta Platforms (Facebook)
- **AAPL**: Apple Inc.
- **TSLA**: Tesla Inc.
- **NVDA**: NVIDIA Corporation
- **SPY**: SPDR S&P 500 ETF
- **QQQ**: Invesco QQQ Trust

### Selection Criteria
- High daily volume (>10M shares)
- Liquid options chains
- Volatility suitable for scalping
- Strong technical patterns

---

## 📊 Performance Tracking

### Metrics Tracked
- **Win/Loss Ratio**: Percentage of profitable trades
- **Average P&L**: Mean profit per trade
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted returns
- **Daily P&L**: Real-time profit/loss tracking

### Logging System
- **Trade Logs**: Complete trade history
- **Signal Logs**: All trading signals
- **Error Logs**: Exception tracking
- **Performance Logs**: Daily summaries

---

## 🛡️ Safety Features

### Paper Trading Mode
- **Risk-Free Testing**: No real money involved
- **Full Functionality**: All features available
- **Performance Validation**: Test strategies safely

### Emergency Controls
- **Emergency Stop**: Instant shutdown capability
- **Position Limits**: Maximum exposure controls
- **Daily Loss Limits**: Automatic shutdown on limits
- **Error Recovery**: Graceful failure handling

### Risk Controls
- **Position Sizing**: Dynamic based on volatility
- **Stop Losses**: Automatic exit on losses
- **Time Limits**: Maximum trade duration
- **Signal Validation**: Multiple confirmation sources

---

## 🚨 Current Status

### ✅ Working Features
- **Dashboard**: Fully functional on http://localhost:8502
- **Market Data**: Real-time quotes via Yahoo Finance
- **Technical Analysis**: All indicators calculated
- **Schwab Auth**: OAuth2 interface ready
- **Bot Framework**: Complete trading logic
- **Logging**: Comprehensive audit trail

### 🔄 In Development
- **Live Trading**: Order execution simulation
- **Options Chains**: Options-specific data
- **Advanced Signals**: Machine learning integration
- **Backtesting**: Historical performance analysis

### 📋 Next Steps
1. **Test Authentication**: Complete Schwab OAuth2 flow
2. **Paper Trading**: Run bot in simulation mode
3. **Performance Analysis**: Monitor and optimize signals
4. **Live Trading**: Enable real order placement

---

## ⚠️ Disclaimer

This bot is for **educational and research purposes**. Trading options involves substantial risk of loss. Always:

- **Test thoroughly** in paper trading mode
- **Start with small amounts** when going live
- **Monitor performance** closely
- **Understand the risks** involved
- **Consult a financial advisor** before live trading

**Past performance does not guarantee future results.**

---

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 coding standards
- Add proper error handling
- Include comprehensive logging
- Test all new features
- Update documentation

---

## 📞 Support

### Getting Help
- **Check Logs**: Review error messages in log files
- **Verify Configuration**: Ensure API keys are correct
- **Test Connectivity**: Check internet and API access
- **Review Documentation**: Check this README and code comments

### Common Issues
- **Import Errors**: Install all dependencies from `requirements.txt`
- **API Errors**: Verify Schwab credentials and authentication
- **Data Issues**: Check Yahoo Finance connectivity
- **Performance Issues**: Monitor system resources

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Schwab**: Trading platform and API
- **Yahoo Finance**: Market data provider
- **Streamlit**: Web application framework
- **Pandas/NumPy**: Data analysis libraries
- **Plotly**: Interactive visualizations

---

**Happy Scalping! 🚀📈**

*Last Updated: January 2025*
*Version: 1.0.0* 