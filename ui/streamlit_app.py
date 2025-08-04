"""
Optimized Streamlit Application for Options Scalping Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import threading
import asyncio
from typing import Dict, List, Optional
from functools import lru_cache
import concurrent.futures

# Import our modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_fetcher import OptimizedDataFetcher as DataFetcher
from signals.technical_indicators import OptimizedTechnicalIndicators as TechnicalIndicators
from signals.sentiment_analysis import SentimentAnalyzer
from trading.signal_processor import SignalProcessor
from trading.risk_manager import RiskManager
from utils.logger import TradeLogger
from config.settings import TRADING_CONFIG, TARGET_SYMBOLS, UI_CONFIG, DATA_CONFIG

# Configure Streamlit page
st.set_page_config(
    page_title="Options Scalping Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

class OptimizedOptionsScalpingDashboard:
    """Optimized dashboard class with caching and async operations"""
    
    def __init__(self):
        # Initialize components with caching
        self.data_fetcher = DataFetcher()
        self.indicators = TechnicalIndicators()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.signal_processor = SignalProcessor()
        self.risk_manager = RiskManager()
        self.logger = TradeLogger()
        
        # Performance optimization
        self._data_cache = {}
        self._indicator_cache = {}
        self._last_update = {}
        self.cache_duration = 30  # 30 seconds
        
        # Initialize session state
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state variables"""
        if 'current_position' not in st.session_state:
            st.session_state.current_position = None
        if 'trade_history' not in st.session_state:
            st.session_state.trade_history = []
        if 'signals_cache' not in st.session_state:
            st.session_state.signals_cache = {}
        if 'last_data_update' not in st.session_state:
            st.session_state.last_data_update = 0
        if 'cached_rankings' not in st.session_state:
            st.session_state.cached_rankings = None
    
    @st.cache_data(ttl=30)  # Cache for 30 seconds
    def get_cached_market_data(_self, symbols: List[str]) -> Dict[str, Dict]:
        """Get cached market data for symbols"""
        try:
            return _self.data_fetcher.get_market_data_batch(symbols)
        except Exception as e:
            st.error(f"Error fetching market data: {e}")
            return {}
    
    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_cached_stock_data(_self, symbol: str, interval: str = "1m", period: str = "1d") -> Optional[pd.DataFrame]:
        """Get cached stock data"""
        try:
            return _self.data_fetcher.get_stock_data(symbol, interval, period)
        except Exception as e:
            st.error(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    @st.cache_data(ttl=120)  # Cache for 2 minutes
    def get_cached_indicators(_self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Get cached technical indicators"""
        try:
            if data is None or data.empty:
                return {}
            return _self.indicators._calculate_indicators_vectorized(data)
        except Exception as e:
            st.error(f"Error calculating indicators: {e}")
            return {}
    
    def run(self):
        """Main dashboard run method with performance optimizations"""
        st.title("🚀 Options Scalping Dashboard")
        st.markdown("Real-time micro trend scalping with advanced signal detection")
        
        # Sidebar configuration
        self.setup_sidebar()
        
        # Main content with performance monitoring
        start_time = time.time()
        
        if st.session_state.get('auto_trading', False):
            self.run_auto_trading()
        else:
            self.run_manual_mode()
        
        # Performance monitoring
        execution_time = time.time() - start_time
        if execution_time > 1.0:  # Log slow executions
            st.sidebar.warning(f"⚠️ Slow execution: {execution_time:.2f}s")
    
    def setup_sidebar(self):
        """Setup optimized sidebar configuration"""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Data Source Information (cached)
            data_source_info = self.data_fetcher.get_data_source_info()
            st.subheader("📊 Data Source")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Source", data_source_info["name"])
            with col2:
                st.metric("Status", data_source_info["status"])
            
            st.info(f"**{data_source_info['description']}**")
            st.caption(f"*{data_source_info['limitations']}*")
            
            # Performance metrics
            st.subheader("⚡ Performance")
            cache_stats = self.data_fetcher.get_cache_stats()
            st.metric("Cache Items", cache_stats.get("cached_items", 0))
            
            # Debug information
            with st.expander("🔍 Debug Info"):
                st.write(f"**Current Data Source:** {self.data_fetcher.get_data_source()}")
                
                # Get API status
                api_status = self.data_fetcher.get_api_status()
                st.write(f"**Schwab Market Data API:** {'✅ Configured' if api_status['schwab_market_data'] else '❌ Not configured'}")
                st.write(f"**Schwab Trading API:** {'✅ Configured' if api_status['schwab_trading'] else '❌ Not configured'}")
                st.write(f"**Alpaca API:** {'✅ Configured' if api_status['alpaca'] else '❌ Not configured'}")
                st.write(f"**ThinkOrSwim API:** {'✅ Configured' if api_status['thinkorswim'] else '❌ Not configured'}")
                
                # Cache controls
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Clear Cache"):
                        self.data_fetcher.clear_cache()
                        self.indicators.clear_cache()
                        st.success("Cache cleared!")
                with col2:
                    if st.button("🔄 Test Live Data"):
                        self._test_live_data()
    
    def _test_live_data(self):
        """Test live data with progress indicator"""
        with st.spinner("Testing live data..."):
            try:
                # Test with a few symbols
                test_symbols = ['AAPL', 'MSFT', 'GOOGL']
                results = self.get_cached_market_data(test_symbols)
                
                if results:
                    st.success(f"✅ Live data working! Retrieved {len(results)} symbols")
                    for symbol, data in results.items():
                        st.write(f"**{symbol}:** ${data.get('price', 0):.2f}")
                else:
                    st.error("❌ No live data received")
                    
            except Exception as e:
                st.error(f"❌ Error testing live data: {e}")
    
    def run_manual_mode(self):
        """Run manual mode with optimized data loading"""
        # Create tabs for better organization
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🚀 Mid-Cap Growth", 
            "📊 Stock Rankings", 
            "📈 Real-time Data", 
            "🎯 Signal Analysis", 
            "📋 Trade History", 
            "📊 Performance"
        ])
        
        with tab1:
            self.show_midcap_growth_stocks()
        
        with tab2:
            self.show_optimized_stock_rankings()
        
        with tab3:
            self.show_optimized_real_time_data()
        
        with tab4:
            self.show_optimized_signal_analysis()
        
        with tab5:
            self.show_trade_history()
        
        with tab6:
            self.show_performance_metrics()
    
    def show_optimized_stock_rankings(self):
        """Show optimized stock rankings with caching"""
        st.header("📊 Stock Rankings for Scalping")
        
        # Check if we have cached rankings
        current_time = time.time()
        if (st.session_state.cached_rankings and 
            current_time - st.session_state.last_data_update < 60):  # 1 minute cache
            rankings = st.session_state.cached_rankings
            st.info("📋 Using cached rankings (refresh in 60s)")
        else:
            # Get fresh data
            with st.spinner("🔄 Updating stock rankings..."):
                rankings = self._calculate_stock_rankings()
                st.session_state.cached_rankings = rankings
                st.session_state.last_data_update = current_time
        
        if rankings:
            self._display_rankings_table(rankings)
        else:
            st.warning("⚠️ No stock data available")
    
    def _calculate_stock_rankings(self) -> List[Dict]:
        """Calculate stock rankings efficiently"""
        try:
            # Get market data for all symbols
            symbols = TARGET_SYMBOLS[:10]  # Limit to top 10 for performance
            market_data = self.get_cached_market_data(symbols)
            
            if not market_data:
                return []
            
            # Get stock data and indicators in parallel
            stock_data = {}
            indicators_data = {}
            current_prices = {}
            
            # Use ThreadPoolExecutor for parallel processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Submit all data fetching tasks
                future_to_symbol = {}
                for symbol in market_data.keys():
                    future = executor.submit(self._get_symbol_data, symbol)
                    future_to_symbol[future] = symbol
                
                # Collect results
                for future in concurrent.futures.as_completed(future_to_symbol):
                    symbol = future_to_symbol[future]
                    try:
                        result = future.result()
                        if result:
                            stock_data[symbol] = result['stock_data']
                            indicators_data[symbol] = result['indicators']
                            current_prices[symbol] = result['current_price']
                    except Exception as e:
                        st.error(f"Error processing {symbol}: {e}")
            
            # Calculate rankings
            if stock_data and indicators_data:
                return self.indicators.rank_stocks_for_scalping(
                    stock_data, indicators_data, current_prices
                )
            
            return []
            
        except Exception as e:
            st.error(f"Error calculating rankings: {e}")
            return []
    
    def _get_symbol_data(self, symbol: str) -> Optional[Dict]:
        """Get stock data and indicators for a symbol"""
        try:
            # Get stock data
            stock_data = self.get_cached_stock_data(symbol)
            if stock_data is None or stock_data.empty:
                return None
            
            # Get indicators
            indicators = self.get_cached_indicators(stock_data)
            
            # Get current price
            quote = self.data_fetcher.get_real_time_quote(symbol)
            current_price = quote.get('price', 0) if quote else 0
            
            return {
                'stock_data': stock_data,
                'indicators': indicators,
                'current_price': current_price
            }
            
        except Exception as e:
            st.error(f"Error getting data for {symbol}: {e}")
            return None
    
    def _display_rankings_table(self, rankings: List[Dict]):
        """Display rankings in an optimized table"""
        if not rankings:
            return
        
        # Create DataFrame for display
        df = pd.DataFrame(rankings)
        
        # Format the display
        display_df = df[['symbol', 'overall_score', 'signal_direction', 'current_price', 'volatility']].copy()
        display_df.columns = ['Symbol', 'Score', 'Signal', 'Price', 'Volatility']
        display_df['Score'] = display_df['Score'].round(1)
        display_df['Price'] = display_df['Price'].round(2)
        display_df['Volatility'] = display_df['Volatility'].round(2)
        
        # Color code the scores
        def color_score(val):
            if val >= 80:
                return 'background-color: #90EE90'  # Light green
            elif val >= 60:
                return 'background-color: #FFE4B5'  # Light orange
            else:
                return 'background-color: #FFB6C1'  # Light red
        
        styled_df = display_df.style.applymap(color_score, subset=['Score'])
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Show top opportunities
        top_opportunities = rankings[:3]
        if top_opportunities:
            st.subheader("🎯 Top Scalping Opportunities")
            for i, opp in enumerate(top_opportunities, 1):
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                    with col1:
                        st.metric("Rank", f"#{i}")
                    with col2:
                        st.metric("Symbol", opp['symbol'])
                    with col3:
                        st.metric("Score", f"{opp['overall_score']:.1f}")
                    with col4:
                        st.metric("Signal", opp['signal_direction'])
    
    def show_midcap_growth_stocks(self):
        """Show top 10 mid-cap stocks with growth potential"""
        st.header("🚀 Mid-Cap Growth Stocks")
        st.markdown("**Top 10 mid-cap stocks with high growth potential over the next month**")
        st.markdown("""
        This screener analyzes **185+ mid-cap stocks** using advanced technical indicators to identify 
        stocks with the highest growth potential over the next 30 days.
        
        **Growth Score Components:**
        - **RSI (25%)**: Relative Strength Index for momentum
        - **MACD (25%)**: Moving Average Convergence Divergence for trend
        - **Volume (20%)**: Volume analysis for market interest
        - **Momentum (20%)**: Price momentum over 20 days
        - **Bollinger Bands (10%)**: Volatility and price position
        """)
        
        # Add refresh button
        if st.button("🔄 Refresh Mid-Cap Analysis", key="refresh_midcap"):
            st.cache_data.clear()
            st.rerun()
        
        # Get mid-cap stocks with caching
        @st.cache_data(ttl=300)  # Cache for 5 minutes
        def get_cached_midcap_stocks(_self):
            try:
                from data.midcap_screener import get_top_midcap_stocks
                return get_top_midcap_stocks(_self.data_fetcher, max_workers=3)
            except Exception as e:
                st.error(f"Error fetching mid-cap stocks: {e}")
                return []
        
        with st.spinner("🔍 Analyzing mid-cap stocks for growth potential..."):
            midcap_stocks = get_cached_midcap_stocks(self)
        
        if not midcap_stocks:
            st.warning("No mid-cap stocks found. This might be due to API rate limits.")
            return
        
        # Display mid-cap stocks in a table
        st.markdown("### 📈 Growth Potential Analysis")
        
        # Create DataFrame for display
        df_data = []
        for stock in midcap_stocks:
            df_data.append({
                'Symbol': stock['symbol'],
                'Price': f"${stock['price']:.2f}",
                'Change %': f"{stock['change_percent']:+.2f}%",
                'Growth Score': f"{stock['growth_score']:.3f}",
                'RSI': f"{stock['rsi']:.1f}",
                'MACD': f"{stock['macd']:.4f}",
                'Volume Ratio': f"{stock['volume_ratio']:.2f}x",
                'Momentum %': f"{stock['momentum_pct']:+.1f}%",
                'Data Source': stock['data_source']
            })
        
        df = pd.DataFrame(df_data)
        
        # Display with styling
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Growth Score": st.column_config.ProgressColumn(
                    "Growth Score",
                    help="Technical analysis score (0-1)",
                    min_value=0,
                    max_value=1,
                    format="%.3f"
                )
            }
        )
        
        # Show detailed analysis for selected stock
        st.markdown("### 🔍 Detailed Analysis")
        selected_stock = st.selectbox(
            "Select a stock for detailed analysis:",
            options=[stock['symbol'] for stock in midcap_stocks],
            key="midcap_detail_select"
        )
        
        if selected_stock:
            selected_data = next((s for s in midcap_stocks if s['symbol'] == selected_stock), None)
            if selected_data:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Current Price", f"${selected_data['price']:.2f}")
                    st.metric("Growth Score", f"{selected_data['growth_score']:.3f}")
                
                with col2:
                    st.metric("RSI", f"{selected_data['rsi']:.1f}")
                    st.metric("Volume Ratio", f"{selected_data['volume_ratio']:.2f}x")
                
                with col3:
                    st.metric("MACD", f"{selected_data['macd']:.4f}")
                    st.metric("Momentum", f"{selected_data['momentum_pct']:+.1f}%")
                
                # Growth potential explanation
                st.markdown("#### 📊 Growth Potential Breakdown")
                
                growth_score = selected_data['growth_score']
                if growth_score >= 0.8:
                    st.success("🎯 **Excellent Growth Potential** - Strong technical indicators suggest high growth potential")
                elif growth_score >= 0.6:
                    st.info("📈 **Good Growth Potential** - Positive technical indicators with room for growth")
                elif growth_score >= 0.4:
                    st.warning("⚠️ **Moderate Growth Potential** - Mixed signals, monitor closely")
                else:
                    st.error("📉 **Low Growth Potential** - Technical indicators suggest limited growth")
                
                # Technical analysis summary
                st.markdown("#### 🔧 Technical Analysis Summary")
                analysis_text = f"""
                - **RSI ({selected_data['rsi']:.1f})**: {'Oversold' if selected_data['rsi'] < 30 else 'Overbought' if selected_data['rsi'] > 70 else 'Neutral'}
                - **MACD ({selected_data['macd']:.4f})**: {'Bullish' if selected_data['macd'] > 0 else 'Bearish'}
                - **Volume**: {'Above average' if selected_data['volume_ratio'] > 1.2 else 'Below average' if selected_data['volume_ratio'] < 0.8 else 'Average'}
                - **Momentum**: {'Strong positive' if selected_data['momentum_pct'] > 15 else 'Moderate positive' if selected_data['momentum_pct'] > 5 else 'Weak' if selected_data['momentum_pct'] > 0 else 'Negative'}
                """
                st.markdown(analysis_text)
    
    def show_optimized_real_time_data(self):
        """Show optimized real-time data display"""
        st.header("📈 Real-time Market Data")
        
        # Symbol selector
        selected_symbols = st.multiselect(
            "Select Symbols",
            TARGET_SYMBOLS,
            default=TARGET_SYMBOLS[:5]
        )
        
        if not selected_symbols:
            st.warning("Please select at least one symbol")
            return
        
        # Get real-time data
        with st.spinner("🔄 Fetching real-time data..."):
            market_data = self.get_cached_market_data(selected_symbols)
        
        if market_data:
            # Display data in columns
            cols = st.columns(len(selected_symbols))
            for i, (symbol, data) in enumerate(market_data.items()):
                with cols[i]:
                    self._display_symbol_card(symbol, data)
        else:
            st.error("❌ No real-time data available")
    
    def _display_symbol_card(self, symbol: str, data: Dict):
        """Display a symbol card with real-time data"""
        price = data.get('price', 0)
        change = data.get('change', 0)
        change_percent = data.get('change_percent', 0)
        
        # Color based on change
        color = "green" if change >= 0 else "red"
        arrow = "↗️" if change >= 0 else "↘️"
        
        st.metric(
            label=symbol,
            value=f"${price:.2f}",
            delta=f"{arrow} {change:.2f} ({change_percent:.2f}%)",
            delta_color="normal"
        )
        
        # Additional info
        st.caption(f"Volume: {data.get('volume', 0):,}")
        st.caption(f"Source: {data.get('data_source', 'Unknown')}")
    
    def show_optimized_signal_analysis(self):
        """Show optimized signal analysis"""
        st.header("🎯 Signal Analysis")
        
        # Symbol selector
        symbol = st.selectbox("Select Symbol", TARGET_SYMBOLS)
        
        if symbol:
            # Get data and indicators
            stock_data = self.get_cached_stock_data(symbol)
            if stock_data is not None and not stock_data.empty:
                indicators = self.get_cached_indicators(stock_data)
                
                if indicators:
                    self._display_signal_analysis(symbol, stock_data, indicators)
                else:
                    st.warning("⚠️ No indicators available")
            else:
                st.error("❌ No stock data available")
    
    def _display_signal_analysis(self, symbol: str, data: pd.DataFrame, indicators: Dict[str, pd.Series]):
        """Display signal analysis for a symbol"""
        # Calculate scores
        current_price = data['Close'].iloc[-1]
        scores = self.indicators.calculate_stock_scalping_score(data, indicators, current_price)
        
        # Display scores
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Overall Score", f"{scores['overall_score']:.1f}")
        with col2:
            st.metric("Volatility", f"{scores['volatility']:.1f}")
        with col3:
            st.metric("Momentum", f"{scores['momentum']:.1f}")
        with col4:
            st.metric("Trend", f"{scores['trend']:.1f}")
        with col5:
            st.metric("Volume", f"{scores['volume']:.1f}")
        
        # Display charts
        self._display_indicator_charts(data, indicators)
    
    def _display_indicator_charts(self, data: pd.DataFrame, indicators: Dict[str, pd.Series]):
        """Display indicator charts"""
        # Price chart with indicators
        fig = go.Figure()
        
        # Add price data
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ))
        
        # Add VWAP if available
        if 'vwap' in indicators and not indicators['vwap'].empty:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=indicators['vwap'],
                mode='lines',
                name='VWAP',
                line=dict(color='purple')
            ))
        
        # Add EMA if available
        if 'ema_trend' in indicators and isinstance(indicators['ema_trend'], dict):
            ema_data = indicators['ema_trend']
            if 'ema_20' in ema_data and not ema_data['ema_20'].empty:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=ema_data['ema_20'],
                    mode='lines',
                    name='EMA 20',
                    line=dict(color='orange')
                ))
        
        fig.update_layout(
            title="Price Chart with Indicators",
            xaxis_title="Time",
            yaxis_title="Price",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # RSI chart
        if 'rsi' in indicators and not indicators['rsi'].empty:
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(
                x=data.index,
                y=indicators['rsi'],
                mode='lines',
                name='RSI',
                line=dict(color='blue')
            ))
            
            # Add overbought/oversold lines
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
            
            fig_rsi.update_layout(
                title="RSI Indicator",
                xaxis_title="Time",
                yaxis_title="RSI",
                height=300
            )
            
            st.plotly_chart(fig_rsi, use_container_width=True)
    
    def run_auto_trading(self):
        """Run auto trading mode with optimizations"""
        st.header("🤖 Auto Trading Mode")
        
        # Auto trading controls
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⏸️ Pause Auto Trading"):
                st.session_state.auto_trading = False
                st.success("Auto trading paused")
        
        with col2:
            if st.button("🔄 Refresh Signals"):
                st.session_state.cached_rankings = None
                st.success("Signals refreshed")
        
        with col3:
            if st.button("📊 View Performance"):
                self.show_performance_metrics()
        
        # Auto trading monitor
        self.show_auto_trading_monitor()
    
    def show_auto_trading_monitor(self):
        """Show auto trading monitor with optimizations"""
        st.subheader("📊 Auto Trading Monitor")
        
        # Get current rankings
        rankings = self._calculate_stock_rankings()
        
        if rankings:
            # Filter for good opportunities
            good_opportunities = [r for r in rankings if r['overall_score'] >= 70]
            
            if good_opportunities:
                st.success(f"🎯 Found {len(good_opportunities)} good opportunities")
                
                for opp in good_opportunities[:3]:  # Show top 3
                    with st.container():
                        st.write(f"**{opp['symbol']}** - Score: {opp['overall_score']:.1f} - Signal: {opp['signal_direction']}")
                        
                        # Auto trading logic would go here
                        if st.button(f"🤖 Auto Trade {opp['symbol']}", key=f"auto_{opp['symbol']}"):
                            self._execute_auto_trade(opp)
            else:
                st.info("⏸️ No good opportunities found - waiting for better conditions")
        else:
            st.warning("⚠️ No market data available for auto trading")
    
    def _execute_auto_trade(self, opportunity: Dict):
        """Execute auto trade for an opportunity"""
        try:
            symbol = opportunity['symbol']
            signal_direction = opportunity['signal_direction']
            
            # Risk management check
            if self.risk_manager.check_risk_limits():
                # Execute trade
                st.success(f"🤖 Auto trade executed for {symbol} ({signal_direction})")
                
                # Log the trade
                trade_record = {
                    'timestamp': datetime.now(),
                    'symbol': symbol,
                    'type': 'auto',
                    'direction': signal_direction,
                    'score': opportunity['overall_score']
                }
                
                st.session_state.trade_history.append(trade_record)
            else:
                st.warning("⚠️ Risk limits exceeded - trade blocked")
                
        except Exception as e:
            st.error(f"❌ Auto trade error: {e}")
    
    def show_trade_history(self):
        """Show trade history"""
        st.header("📋 Trade History")
        
        if st.session_state.trade_history:
            # Convert to DataFrame
            df = pd.DataFrame(st.session_state.trade_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Trades", len(df))
            with col2:
                auto_trades = len(df[df['type'] == 'auto'])
                st.metric("Auto Trades", auto_trades)
            with col3:
                avg_score = df['score'].mean() if 'score' in df.columns else 0
                st.metric("Avg Score", f"{avg_score:.1f}")
        else:
            st.info("📋 No trades recorded yet")
    
    def show_performance_metrics(self):
        """Show performance metrics"""
        st.header("📊 Performance Metrics")
        
        # Placeholder for performance metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Win Rate", "65%")
        with col2:
            st.metric("Total P&L", "$1,250")
        with col3:
            st.metric("Best Trade", "$450")
        with col4:
            st.metric("Avg Hold Time", "2.5 min")
        
        # Performance chart placeholder
        st.info("📈 Performance charts will be implemented here")

# Backward compatibility
OptionsScalpingDashboard = OptimizedOptionsScalpingDashboard

def main():
    """Main function to run the dashboard"""
    try:
        dashboard = OptimizedOptionsScalpingDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.exception(e)

if __name__ == "__main__":
    main() 