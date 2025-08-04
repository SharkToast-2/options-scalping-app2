import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import time
import random
from data_cache import DataCache
from schwab_api import get_schwab_client

st.set_page_config(page_title="Advanced Stock Analysis", layout="wide")

def create_mock_data(symbol, days=252):
    """Create mock stock data for demonstration when API is rate limited"""
    np.random.seed(42)  # For reproducible results
    
    # Generate realistic stock data
    start_price = 150.0
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate price movements
    returns = np.random.normal(0.0005, 0.02, days)  # Daily returns
    prices = [start_price]
    
    for i in range(1, days):
        new_price = prices[-1] * (1 + returns[i])
        prices.append(new_price)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
        'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)
    
    return data

def get_stock_data_with_schwab(symbol, period="1y", use_cache=True, use_mock=True):
    """Fetch stock data using Schwab API with fallback options"""
    cache = DataCache()
    
    # Try to get cached data first
    if use_cache:
        cached_data = cache.get_cached_data(symbol, period)
        if cached_data is not None:
            return None, cached_data, False, "cached"  # False = not mock data, but cached
    
    try:
        # Get Schwab API client
        schwab_client = get_schwab_client(use_mock=use_mock)
        
        # Fetch historical data
        data = schwab_client.get_historical_data(symbol, period)
        
        if data is not None and not data.empty:
            # Cache the successful data
            if use_cache:
                cache.cache_data(symbol, period, data)
            return schwab_client, data, False, "schwab"  # False = not mock data
        
        # Fallback to mock data
        st.warning(f"⚠️ No data available for {symbol}. Using mock data for demonstration.")
        return None, create_mock_data(symbol), True, "mock"  # True = mock data
        
    except Exception as e:
        st.error(f"Error accessing Schwab API: {e}")
        st.info("Using mock data for demonstration.")
        return None, create_mock_data(symbol), True, "mock"

def main():
    st.title("📈 Advanced Stock Analysis Dashboard")
    st.write("Comprehensive stock analysis powered by Schwab API")
    
    # Add API info
    with st.sidebar:
        st.info("💡 **Data Source:** Schwab API\nMock data used for demonstration. Get real API access at developer.schwab.com")
    
    # Sidebar
    st.sidebar.header("Settings")
    symbol = st.sidebar.text_input("Stock Symbol", "AAPL").upper()
    period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])
    
    # Add options
    use_cache = st.sidebar.checkbox("Use data cache", value=True, help="Reduces API calls by caching data")
    use_mock = st.sidebar.checkbox("Use mock data", value=True, help="Use mock data for demonstration")
    
    # API Key input (optional)
    api_key = st.sidebar.text_input("Schwab API Key (optional)", type="password", help="Enter your Schwab API key for real data")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Technical Analysis", "Backtesting", "Risk Analysis"])
    
    if st.sidebar.button("Analyze"):
        with st.spinner("Fetching data..."):
            try:
                # Fetch data using Schwab API
                client, data, is_mock, data_source = get_stock_data_with_schwab(
                    symbol, period, use_cache=use_cache, use_mock=use_mock
                )
                
                # Show data source info
                if data_source == "mock":
                    st.warning(f"📊 Using mock data for {symbol} (no API access)")
                elif data_source == "cached":
                    st.success(f"📊 Using cached data for {symbol}")
                elif data_source == "schwab":
                    st.success(f"📊 Using Schwab API data for {symbol}")
                
                if not data.empty:
                    with tab1:
                        show_overview(data, symbol, is_mock, data_source)
                    
                    with tab2:
                        show_technical_analysis(data, symbol, is_mock, data_source)
                    
                    with tab3:
                        show_backtesting(data, symbol, is_mock, data_source)
                    
                    with tab4:
                        show_risk_analysis(data, symbol, is_mock, data_source)
                else:
                    st.error("No data found for this symbol")
                    
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Try using mock data or check your API key.")

def show_overview(data, symbol, is_mock=False, data_source="unknown"):
    """Show overview tab"""
    st.header("📊 Overview")
    
    if is_mock:
        st.info("📊 **Mock Data Mode**: This is simulated data for demonstration purposes.")
    elif data_source == "cached":
        st.info("📊 **Cached Data**: Using previously fetched data.")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"${data['Close'].iloc[-1]:.2f}")
    
    with col2:
        change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
        change_pct = (change / data['Close'].iloc[-2]) * 100
        st.metric("Daily Change", f"${change:.2f}", f"{change_pct:+.2f}%")
    
    with col3:
        st.metric("52-Week High", f"${data['High'].max():.2f}")
    
    with col4:
        st.metric("52-Week Low", f"${data['Low'].min():.2f}")
    
    # Price chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='OHLC'
    ))
    fig.update_layout(title=f"{symbol} Stock Price", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

def show_technical_analysis(data, symbol, is_mock=False, data_source="unknown"):
    """Show technical analysis tab"""
    st.header("📈 Technical Analysis")
    
    if is_mock:
        st.info("📊 **Mock Data Mode**: Technical indicators calculated from simulated data.")
    
    # Calculate indicators
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Moving averages
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='MA20'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA50'))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA200'], name='MA200'))
        fig.update_layout(title="Moving Averages", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # RSI
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'))
        fig.add_hline(y=70, line_dash="dash", line_color="red")
        fig.add_hline(y=30, line_dash="dash", line_color="green")
        fig.update_layout(title="RSI", xaxis_title="Date", yaxis_title="RSI")
        st.plotly_chart(fig, use_container_width=True)

def show_backtesting(data, symbol, is_mock=False, data_source="unknown"):
    """Show backtesting tab"""
    st.header("🔄 Strategy Backtesting")
    
    if is_mock:
        st.info("📊 **Mock Data Mode**: Backtesting results based on simulated data.")
    
    # Simple backtesting example
    if st.button("Run Simple Backtest"):
        with st.spinner("Running backtest..."):
            # Simple buy and hold strategy
            initial_price = data['Close'].iloc[0]
            final_price = data['Close'].iloc[-1]
            total_return = (final_price - initial_price) / initial_price
            
            # Calculate some basic metrics
            returns = data['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252)
            sharpe_ratio = (returns.mean() * 252) / volatility if volatility > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Return", f"{total_return:.2%}")
            with col2:
                st.metric("Annual Volatility", f"{volatility:.2%}")
            with col3:
                st.metric("Sharpe Ratio", f"{sharpe_ratio:.3f}")
            with col4:
                st.metric("Days Analyzed", len(data))
            
            # Simple performance chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Stock Price',
                line=dict(color='blue')
            ))
            fig.update_layout(title="Buy & Hold Strategy Performance", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig, use_container_width=True)

def show_risk_analysis(data, symbol, is_mock=False, data_source="unknown"):
    """Show risk analysis tab"""
    st.header("⚠️ Risk Analysis")
    
    if is_mock:
        st.info("📊 **Mock Data Mode**: Risk metrics calculated from simulated data.")
    
    # Calculate returns
    returns = data['Close'].pct_change().dropna()
    
    # Risk metrics
    volatility = returns.std() * np.sqrt(252)
    var_95 = np.percentile(returns, 5)  # 95% VaR
    max_drawdown = (returns.cumsum().min())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Annual Volatility", f"{volatility:.2%}")
    with col2:
        st.metric("VaR (95%)", f"{var_95:.2%}")
    with col3:
        st.metric("Skewness", f"{returns.skew():.3f}")
    with col4:
        st.metric("Max Drawdown", f"{max_drawdown:.2%}")
    
    # Returns distribution
    fig = px.histogram(returns, title="Returns Distribution", nbins=30)
    fig.update_layout(xaxis_title="Daily Returns", yaxis_title="Frequency")
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional risk info
    st.subheader("Risk Management Tips")
    st.markdown("""
    - **Volatility**: Higher volatility means more price swings
    - **VaR**: 95% VaR shows the maximum expected loss in 95% of cases
    - **Skewness**: Negative skewness indicates more downside risk
    - **Max Drawdown**: The largest peak-to-trough decline
    """)

if __name__ == "__main__":
    main() 