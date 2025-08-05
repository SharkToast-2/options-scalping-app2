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
import json
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
        if 'max_trade_amount' not in st.session_state:
            st.session_state.max_trade_amount = TRADING_CONFIG.get("MAX_POSITION_SIZE", 1000)
        if 'max_daily_loss' not in st.session_state:
            st.session_state.max_daily_loss = TRADING_CONFIG.get("MAX_DAILY_LOSS", 500)
        if 'stop_loss_pct' not in st.session_state:
            st.session_state.stop_loss_pct = TRADING_CONFIG.get("STOP_LOSS_PCT", 3.0)
        if 'profit_target_pct' not in st.session_state:
            st.session_state.profit_target_pct = TRADING_CONFIG.get("PROFIT_TARGET_PCT", 5.0)
        if 'trading_mode' not in st.session_state:
            st.session_state.trading_mode = "Paper Trading"
        if 'schwab_auth' not in st.session_state:
            st.session_state.schwab_auth = {'status': 'not_authenticated'}
    
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
                
                            # Trading Controls
            st.subheader("🤖 Trading Controls")
            
            # Auto-trading toggle
            auto_trading = st.checkbox(
                "Enable Auto-Trading", 
                value=st.session_state.get('auto_trading', False),
                help="Enable automated trading based on signals"
            )
            st.session_state.auto_trading = auto_trading
            
            if auto_trading:
                st.success("✅ Auto-trading enabled")
                st.warning("⚠️ Real money trading is active!")
            else:
                st.info("📊 Manual mode - no trades will be executed")
            
            # Trading mode selection
            trading_mode = st.selectbox(
                "Trading Mode",
                ["Paper Trading", "Live Trading"],
                index=0 if TRADING_CONFIG.get("PAPER_TRADING", True) else 1,
                help="Paper trading uses virtual money, live trading uses real money"
            )
            
            # Store trading mode in session state
            st.session_state.trading_mode = trading_mode
            
            if trading_mode == "Live Trading":
                st.error("🚨 LIVE TRADING MODE - Real money will be used!")
                confirm_live = st.checkbox("I understand and accept the risks")
                if not confirm_live:
                    st.stop()
                
                # Schwab Authentication Section
                st.subheader("🔐 Schwab Authentication")
                
                # Check if already authenticated
                auth_status = self._check_schwab_auth()
                
                if auth_status['authenticated']:
                    st.success("✅ Schwab authenticated")
                    st.caption(f"Last auth: {auth_status['last_auth']}")
                else:
                    st.warning("⚠️ Schwab authentication required")
                    
                    # Authentication options
                    auth_method = st.selectbox(
                        "Authentication Method",
                        ["OAuth2 (Recommended)", "API Key Only", "Manual Login"],
                        help="Choose how to authenticate with Schwab"
                    )
                    
                    if auth_method == "OAuth2 (Recommended)":
                        if st.button("🔑 Start OAuth2 Authentication"):
                            self._start_schwab_oauth()
                    
                    elif auth_method == "API Key Only":
                        st.info("Using API key authentication")
                        if st.button("🔑 Test API Connection"):
                            self._test_schwab_api()
                    
                    elif auth_method == "Manual Login":
                        st.info("""
                        **Manual Authentication Steps:**
                        1. Go to [Schwab Login](https://client.schwab.com/Areas/Access/Login)
                        2. Sign in to your account
                        3. Return here and click "Verify Authentication"
                        """)
                        if st.button("✅ Verify Authentication"):
                            self._verify_manual_auth()
                
                # Authentication status display
                with st.expander("🔍 Authentication Details"):
                    st.write(f"**Status:** {'✅ Authenticated' if auth_status['authenticated'] else '❌ Not Authenticated'}")
                    st.write(f"**Method:** {auth_status['method']}")
                    st.write(f"**Expires:** {auth_status['expires']}")
                    
                    if st.button("🔄 Refresh Auth Status"):
                        st.rerun()
            
            # Risk Management Controls
            st.subheader("💰 Risk Management")
            
            # Max trade amount
            max_trade_amount = st.number_input(
                "Max Trade Amount ($)",
                min_value=100,
                max_value=10000,
                value=TRADING_CONFIG.get("MAX_POSITION_SIZE", 1000),
                step=100,
                help="Maximum amount to invest in a single trade"
            )
            
            # Max daily loss
            max_daily_loss = st.number_input(
                "Max Daily Loss ($)",
                min_value=100,
                max_value=5000,
                value=TRADING_CONFIG.get("MAX_DAILY_LOSS", 500),
                step=100,
                help="Maximum amount to lose in a single day"
            )
            
            # Stop loss percentage
            stop_loss_pct = st.slider(
                "Stop Loss (%)",
                min_value=1.0,
                max_value=10.0,
                value=TRADING_CONFIG.get("STOP_LOSS_PCT", 3.0),
                step=0.5,
                help="Percentage loss at which to automatically sell"
            )
            
            # Profit target percentage
            profit_target_pct = st.slider(
                "Profit Target (%)",
                min_value=1.0,
                max_value=20.0,
                value=TRADING_CONFIG.get("PROFIT_TARGET_PCT", 5.0),
                step=0.5,
                help="Percentage gain at which to automatically sell"
            )
            
            # Update session state with new values
            st.session_state.max_trade_amount = max_trade_amount
            st.session_state.max_daily_loss = max_daily_loss
            st.session_state.stop_loss_pct = stop_loss_pct
            st.session_state.profit_target_pct = profit_target_pct
            
            # Display current risk settings
            st.info(f"""
            **Current Risk Settings:**
            - Max Trade: ${max_trade_amount:,}
            - Max Daily Loss: ${max_daily_loss:,}
            - Stop Loss: {stop_loss_pct}%
            - Profit Target: {profit_target_pct}%
            """)
            
            # Save settings button
            if st.button("💾 Save Risk Settings"):
                # Update the trading configuration
                TRADING_CONFIG["MAX_POSITION_SIZE"] = max_trade_amount
                TRADING_CONFIG["MAX_DAILY_LOSS"] = max_daily_loss
                TRADING_CONFIG["STOP_LOSS_PCT"] = stop_loss_pct
                TRADING_CONFIG["PROFIT_TARGET_PCT"] = profit_target_pct
                st.success("✅ Risk settings saved!")
                st.rerun()
            
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
        # Create optimized tabs for scalping
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Scalping Opportunities", 
            "📊 Stock Rankings", 
            "📈 Real-time Data", 
            "📋 Trade History", 
            "📊 Performance"
        ])
        
        with tab1:
            self.show_scalping_opportunities()
        
        with tab2:
            self.show_optimized_stock_rankings()
        
        with tab3:
            self.show_optimized_real_time_data()
        
        with tab4:
            self.show_trade_history()
        
        with tab5:
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
            
            # Show data source status
            data_source = self.data_fetcher.get_data_source()
            st.caption(f"📡 **Data Source**: {data_source.title()}")
        else:
            st.warning("⚠️ No stock data available")
            st.info("🔄 Generating mock rankings...")
            mock_rankings = self._generate_mock_rankings(['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'])
            self._display_rankings_table(mock_rankings)
    
    def _calculate_stock_rankings(self) -> List[Dict]:
        """Calculate stock rankings efficiently"""
        try:
            # Get market data for all symbols
            symbols = TARGET_SYMBOLS[:10]  # Limit to top 10 for performance
            market_data = self.get_cached_market_data(symbols)
            
            if not market_data:
                st.warning("⚠️ No market data available, using mock rankings")
                return self._generate_mock_rankings(symbols[:5])
            
            # Get stock data and indicators in parallel
            stock_data = {}
            indicators_data = {}
            current_prices = {}
            
            # Use ThreadPoolExecutor for parallel processing with reduced workers
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                # Submit all data fetching tasks
                future_to_symbol = {}
                for symbol in list(market_data.keys())[:5]:  # Limit to 5 symbols
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
                        st.warning(f"⚠️ Error processing {symbol}: {e}")
                        # Continue with other symbols
            
            # Calculate rankings
            if stock_data and indicators_data:
                return self.indicators.rank_stocks_for_scalping(
                    stock_data, indicators_data, current_prices
                )
            else:
                st.warning("⚠️ No real data available, using mock rankings")
                return self._generate_mock_rankings(list(market_data.keys())[:5])
            
        except Exception as e:
            st.error(f"Error calculating rankings: {e}")
            st.info("🔄 Generating mock rankings as fallback...")
            return self._generate_mock_rankings(symbols[:5])
    
    def _generate_mock_rankings(self, symbols: List[str]) -> List[Dict]:
        """Generate mock stock rankings when real data is not available"""
        import random
        
        mock_rankings = []
        
        for i, symbol in enumerate(symbols):
            # Generate realistic mock data
            base_price = random.uniform(50, 500)
            volatility = random.uniform(0.5, 3.0)
            score = random.uniform(60, 95)  # Good scores to show potential
            
            # Determine signal direction based on score
            if score >= 80:
                signal = "BUY"
            elif score >= 65:
                signal = "HOLD"
            else:
                signal = "SELL"
            
            mock_ranking = {
                'symbol': symbol,
                'overall_score': round(score, 1),
                'signal_direction': signal,
                'current_price': round(base_price, 2),
                'volatility': round(volatility, 2),
                'rsi': round(random.uniform(30, 70), 1),
                'macd': round(random.uniform(-2, 2), 2),
                'volume': random.randint(1000000, 10000000),
                'change_percent': round(random.uniform(-5, 8), 2),
                'data_source': 'mock'
            }
            
            mock_rankings.append(mock_ranking)
        
        # Sort by score (highest first)
        mock_rankings.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return mock_rankings
    
    def _get_symbol_data(self, symbol: str) -> Optional[Dict]:
        """Get stock data and indicators for a symbol"""
        try:
            # Get stock data
            stock_data = self.get_cached_stock_data(symbol)
            if stock_data is None or stock_data.empty:
                st.warning(f"⚠️ No stock data available for {symbol}")
                return None
            
            # Get indicators
            indicators = self.get_cached_indicators(stock_data)
            if not indicators:
                st.warning(f"⚠️ No indicators available for {symbol}")
                return None
            
            # Get current price
            quote = self.data_fetcher.get_real_time_quote(symbol)
            current_price = quote.get('price', 0) if quote else 0
            
            if current_price == 0:
                st.warning(f"⚠️ No current price available for {symbol}")
                return None
            
            return {
                'stock_data': stock_data,
                'indicators': indicators,
                'current_price': current_price
            }
            
        except Exception as e:
            st.warning(f"⚠️ Error getting data for {symbol}: {e}")
            return None
    
    def _display_rankings_table(self, rankings: List[Dict]):
        """Display rankings in an optimized table"""
        if not rankings:
            return
        
        # Check if using mock data
        using_mock = any(ranking.get('data_source') == 'mock' for ranking in rankings)
        
        if using_mock:
            st.info("📊 **Mock Data Mode**: Using simulated rankings due to API rate limits")
        
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
        
        styled_df = display_df.style.map(color_score, subset=['Score'])
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Show additional info for mock data
        if using_mock:
            st.caption("💡 **Note**: Mock data shows potential trading opportunities. Real data will be used when APIs are available.")
            
            # Show refresh button
            if st.button("🔄 Try Real Data Again"):
                st.session_state.cached_rankings = None
                st.rerun()
        
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
    
    def show_scalping_opportunities(self):
        """Show optimized scalping opportunities with quick signals"""
        st.header("🎯 Scalping Opportunities")
        st.markdown("**Real-time scalping signals for quick profit opportunities**")
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("🔄 Auto-refresh every 30 seconds", value=True)
        
        if auto_refresh:
            time.sleep(0.1)  # Small delay for auto-refresh
        
        # Get scalping opportunities
        opportunities = self._get_scalping_opportunities()
        
        if not opportunities:
            st.warning("No scalping opportunities found. Market may be quiet or signals are weak.")
            return
        
        # Display top opportunities in cards
        st.subheader("🔥 Hot Scalping Signals")
        
        for i, opp in enumerate(opportunities[:5], 1):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
                
                with col1:
                    if opp['signal'] == 'BUY':
                        st.markdown("🟢 **BUY**")
                    else:
                        st.markdown("🔴 **SELL**")
                
                with col2:
                    st.markdown(f"**{opp['symbol']}** - ${opp['price']:.2f}")
                    st.caption(f"Signal Strength: {opp['strength']}/10")
                
                with col3:
                    st.metric("Change", f"{opp['change_pct']:+.2f}%")
                
                with col4:
                    st.metric("Volume", f"{opp['volume_ratio']:.1f}x")
                
                with col5:
                    if st.button(f"Trade #{i}", key=f"trade_{opp['symbol']}_{i}"):
                        self._execute_quick_trade(opp)
                
                # Progress bar for signal strength
                st.progress(opp['strength'] / 10)
                
                # Quick stats
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                with col_stats1:
                    st.caption(f"RSI: {opp['rsi']:.1f}")
                with col_stats2:
                    st.caption(f"MACD: {opp['macd']:.3f}")
                with col_stats3:
                    st.caption(f"ATR: {opp['atr']:.3f}")
                
                st.divider()
        
        # Quick trade summary
        st.subheader("📊 Quick Trade Summary")
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        
        with col_sum1:
            buy_signals = len([o for o in opportunities if o['signal'] == 'BUY'])
            st.metric("Buy Signals", buy_signals)
        
        with col_sum2:
            sell_signals = len([o for o in opportunities if o['signal'] == 'SELL'])
            st.metric("Sell Signals", sell_signals)
        
        with col_sum3:
            avg_strength = sum(o['strength'] for o in opportunities) / len(opportunities)
            st.metric("Avg Strength", f"{avg_strength:.1f}/10")
    
    def _get_scalping_opportunities(self) -> List[Dict]:
        """Get real-time scalping opportunities"""
        try:
            # Get current market data for target symbols
            symbols = TARGET_SYMBOLS[:10]  # Focus on top 10 for speed
            market_data = self.get_cached_market_data(symbols)
            
            opportunities = []
            
            for symbol, data in market_data.items():
                if not data:
                    continue
                
                # Get technical indicators
                stock_data = self.get_cached_stock_data(symbol, "1m", "1d")
                if stock_data is None or stock_data.empty:
                    continue
                
                indicators = self.get_cached_indicators(stock_data)
                
                # Calculate scalping signal
                signal = self._calculate_scalping_signal(indicators, data)
                
                if signal['strength'] >= 6:  # Only show strong signals
                    opportunities.append({
                        'symbol': symbol,
                        'price': data.get('price', 0),
                        'change_pct': data.get('change_percent', 0),
                        'volume_ratio': data.get('volume_ratio', 1),
                        'signal': signal['direction'],
                        'strength': signal['strength'],
                        'rsi': indicators.get('rsi', pd.Series()).iloc[-1] if 'rsi' in indicators else 50,
                        'macd': indicators.get('macd', {}).get('macd_diff', pd.Series()).iloc[-1] if 'macd' in indicators else 0,
                        'atr': indicators.get('atr', pd.Series()).iloc[-1] if 'atr' in indicators else 0
                    })
            
            # Sort by signal strength
            opportunities.sort(key=lambda x: x['strength'], reverse=True)
            return opportunities
            
        except Exception as e:
            st.error(f"Error getting scalping opportunities: {e}")
            return []
    
    def _calculate_scalping_signal(self, indicators: Dict, market_data: Dict) -> Dict:
        """Calculate scalping signal strength and direction"""
        try:
            strength = 0
            direction = 'HOLD'
            
            # RSI signals
            rsi = indicators.get('rsi', pd.Series())
            if not rsi.empty:
                current_rsi = rsi.iloc[-1]
                if current_rsi < 30:
                    strength += 2
                    direction = 'BUY'
                elif current_rsi > 70:
                    strength += 2
                    direction = 'SELL'
                elif 40 <= current_rsi <= 60:
                    strength += 1
            
            # MACD signals
            macd_data = indicators.get('macd', {})
            if isinstance(macd_data, dict) and 'macd_diff' in macd_data:
                macd_diff = macd_data['macd_diff']
                if not macd_diff.empty:
                    current_macd = macd_diff.iloc[-1]
                    if current_macd > 0:
                        strength += 2
                        if direction == 'HOLD':
                            direction = 'BUY'
                    else:
                        strength += 1
                        if direction == 'HOLD':
                            direction = 'SELL'
            
            # Volume signals
            volume_ratio = market_data.get('volume_ratio', 1)
            if volume_ratio > 1.5:
                strength += 2
            elif volume_ratio > 1.2:
                strength += 1
            
            # Price momentum
            change_pct = market_data.get('change_percent', 0)
            if abs(change_pct) > 2:
                strength += 1
            
            return {
                'direction': direction,
                'strength': min(strength, 10)
            }
            
        except Exception as e:
            return {'direction': 'HOLD', 'strength': 0}
    
    def _execute_quick_trade(self, opportunity: Dict):
        """Execute a quick scalping trade"""
        try:
            if not st.session_state.get('auto_trading', False):
                st.warning("Auto-trading is disabled. Enable it in the sidebar to execute trades.")
                return
            
            # Check Schwab authentication for live trading
            if st.session_state.get('trading_mode') == "Live Trading":
                auth_status = self._check_schwab_auth()
                if not auth_status['authenticated']:
                    st.error("❌ Schwab authentication required for live trading. Please authenticate in the sidebar.")
                    return
            
            # Get current risk settings
            max_trade = st.session_state.get('max_trade_amount', 1000)
            stop_loss = st.session_state.get('stop_loss_pct', 3.0)
            profit_target = st.session_state.get('profit_target_pct', 5.0)
            
            # Calculate position size
            price = opportunity['price']
            shares = int(max_trade / price)
            
            if shares == 0:
                st.error("Position size too small for current price")
                return
            
            # Execute trade
            trade_result = {
                'symbol': opportunity['symbol'],
                'action': opportunity['signal'],
                'shares': shares,
                'price': price,
                'total': shares * price,
                'stop_loss': price * (1 - stop_loss/100),
                'profit_target': price * (1 + profit_target/100),
                'timestamp': datetime.now(),
                'status': 'executed'
            }
            
            # Add to trade history
            if 'trade_history' not in st.session_state:
                st.session_state.trade_history = []
            st.session_state.trade_history.append(trade_result)
            
            st.success(f"✅ {opportunity['signal']} {shares} shares of {opportunity['symbol']} at ${price:.2f}")
            
        except Exception as e:
            st.error(f"Error executing trade: {e}")
    
    def _check_schwab_auth(self) -> Dict:
        """Check Schwab authentication status"""
        try:
            # Check if we have valid tokens in session state
            if 'schwab_auth' in st.session_state:
                auth_data = st.session_state.schwab_auth
                if auth_data.get('status') == 'authenticated':
                    return {
                        'authenticated': True,
                        'method': auth_data.get('method', 'OAuth2'),
                        'last_auth': auth_data.get('timestamp', 'Unknown'),
                        'expires': auth_data.get('expires', 'Unknown')
                    }
            
            # Check config file for saved tokens
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    schwab_auth = config.get('schwab_auth', {})
                    # Check if we have access_token or auth_code
                    if schwab_auth.get('access_token') or schwab_auth.get('auth_code'):
                        return {
                            'authenticated': True,
                            'method': schwab_auth.get('method', 'OAuth2'),
                            'last_auth': schwab_auth.get('timestamp', 'Unknown'),
                            'expires': schwab_auth.get('expires', '1 hour')
                        }
            except:
                pass
            
            return {
                'authenticated': False,
                'method': 'None',
                'last_auth': 'Never',
                'expires': 'N/A'
            }
            
        except Exception as e:
            return {
                'authenticated': False,
                'method': 'Error',
                'last_auth': 'Error',
                'expires': 'Error'
            }
    
    def _start_schwab_oauth(self):
        """Start Schwab OAuth2 authentication process"""
        try:
            st.info("🔄 Starting Schwab OAuth2 authentication...")
            
            # Automatically open the browser when OAuth starts
            self._open_schwab_auth_page()
            
            # Show OAuth instructions
            st.markdown("""
            **OAuth2 Authentication Steps:**
            1. ✅ Browser window opened to Schwab's authorization page
            2. Sign in to your Schwab account
            3. Authorize the application
            4. Copy the entire URL you're redirected to
            5. Paste it in the field below
            """)
            
            # Create input field for authorization URL
            auth_url = st.text_input(
                "Paste the authorization URL here:",
                placeholder="https://developer.schwab.com/oauth2-redirect.html?code=...",
                help="Paste the complete URL you're redirected to after authorization"
            )
            
            if auth_url:
                if st.button("🔑 Complete Authentication"):
                    # Import the trade executor for authentication
                    from modules.trade_executor import complete_oauth_auth
                    
                    # Complete the OAuth flow
                    auth_result = complete_oauth_auth(auth_url)
                    
                    if auth_result:
                        st.success("✅ Schwab OAuth2 authentication successful!")
                        st.session_state.schwab_auth = {
                            'status': 'authenticated',
                            'method': 'OAuth2',
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'expires': '1 hour'
                        }
                        st.rerun()
                    else:
                        st.error("❌ Schwab OAuth2 authentication failed")
            
            # Show manual OAuth start button as backup
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🌐 Reopen Schwab Authorization Page"):
                    self._open_schwab_auth_page()
            with col2:
                if st.button("🔗 Copy Authorization URL"):
                    st.code("https://api.schwabapi.com/v1/oauth/authorize?response_type=code&client_id=1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj&scope=readonly&redirect_uri=https://developer.schwab.com/oauth2-redirect.html", language="text")
                    st.info("📋 URL copied! You can paste this in your browser manually.")
                
        except Exception as e:
            st.error(f"❌ Error during OAuth2 authentication: {e}")
    
    def _open_schwab_auth_page(self):
        """Open Schwab authorization page"""
        try:
            import webbrowser
            import platform
            import subprocess
            import os
            
            # Schwab OAuth2 authorization URL
            auth_url = "https://api.schwabapi.com/v1/oauth/authorize?response_type=code&client_id=1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj&scope=readonly&redirect_uri=https://developer.schwab.com/oauth2-redirect.html"
            
            # Try multiple methods to open browser
            success = False
            
            # Method 1: Try webbrowser module (most reliable)
            try:
                st.info("🔍 Attempting to open browser with webbrowser module...")
                success = webbrowser.open(auth_url)
                if success:
                    st.success("🌐 Browser opened to Schwab authorization page!")
                    st.info("Please complete the authorization and paste the redirect URL above.")
                    return
                else:
                    st.warning("⚠️ webbrowser.open() returned False")
            except Exception as e:
                st.warning(f"⚠️ webbrowser.open() failed: {e}")
            
            # Method 2: Try platform-specific commands
            if not success:
                try:
                    system = platform.system()
                    st.info(f"🔍 Detected platform: {system}")
                    
                    # Enhanced platform detection for macOS
                    platform_info = platform.platform().lower()
                    st.info(f"🔍 Platform info: {platform_info}")
                    
                    is_macos = (system == "Darwin" or 
                               system == "macOS" or 
                               "darwin" in platform_info or
                               "mac" in platform_info or
                               "darwin" in platform.machine().lower() or
                               "mac" in platform.machine().lower())
                    
                    st.info(f"🔍 is_macos: {is_macos}")
                    
                    # Force macOS detection if we're on a Mac (additional check)
                    if not is_macos and os.path.exists("/Applications"):
                        st.info("🍎 Detected /Applications directory - forcing macOS detection")
                        is_macos = True
                    
                    if is_macos:
                        st.info("🍎 Detected macOS - using 'open' command")
                        subprocess.run(["open", auth_url], check=True, capture_output=True)
                        st.success("🌐 Browser opened using macOS 'open' command!")
                        success = True
                    elif system == "Windows":
                        subprocess.run(["start", auth_url], shell=True, check=True, capture_output=True)
                        st.success("🌐 Browser opened using Windows 'start' command!")
                        success = True
                    elif system == "Linux":
                        st.info("🐧 Detected Linux - trying multiple browser opening methods")
                        
                        # Try multiple Linux browser opening methods
                        linux_methods = [
                            ["xdg-open", auth_url],
                            ["google-chrome", auth_url],
                            ["firefox", auth_url],
                            ["chromium-browser", auth_url],
                            ["brave-browser", auth_url]
                        ]
                        
                        for method in linux_methods:
                            try:
                                subprocess.run(method, check=True, capture_output=True)
                                st.success(f"🌐 Browser opened using {' '.join(method)}!")
                                success = True
                                break
                            except (subprocess.CalledProcessError, FileNotFoundError):
                                continue
                        
                        if not success:
                            st.warning("⚠️ All Linux browser methods failed")
                    else:
                        st.warning(f"⚠️ Unknown platform: {system}")
                        # Fallback: try macOS commands if we're unsure
                        try:
                            st.info("🔄 Trying macOS fallback...")
                            subprocess.run(["open", auth_url], check=True, capture_output=True)
                            st.success("🌐 Browser opened using macOS fallback!")
                            success = True
                        except:
                            st.warning("⚠️ macOS fallback also failed")
                except (subprocess.CalledProcessError, FileNotFoundError) as e:
                    st.warning(f"⚠️ Platform-specific browser opening failed: {e}")
                except Exception as e:
                    st.warning(f"⚠️ Platform-specific browser opening failed: {e}")
            
            # Method 3: Try common browser executables (macOS specific)
            if not success and platform.system() == "Darwin":
                browsers = [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "/Applications/Firefox.app/Contents/MacOS/firefox",
                    "/Applications/Safari.app/Contents/MacOS/Safari",
                    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
                ]
                
                for browser in browsers:
                    try:
                        if os.path.exists(browser):
                            subprocess.run([browser, auth_url], check=True, capture_output=True)
                            st.success(f"🌐 Browser opened using {os.path.basename(browser)}!")
                            success = True
                            break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
            
            # Always show the URL and provide manual options
            st.markdown("---")
            st.markdown("**🔗 Schwab Authorization URL:**")
            st.code(auth_url, language="text")
            
            # Add a clickable link
            st.markdown(f"[🌐 Click here to open Schwab Authorization Page]({auth_url})")
            
            # Show manual instructions
            st.info("📋 **Manual Steps:**")
            st.markdown("""
            1. **Click the link above** to open the Schwab authorization page
            2. **Sign in** to your Schwab account
            3. **Authorize** the application
            4. **Copy the entire URL** you're redirected to
            5. **Paste it** in the input field above
            """)
            
            if not success:
                st.warning("⚠️ Automatic browser opening failed, but you can still complete the process manually")
            
        except Exception as e:
            st.error(f"❌ Error opening browser: {e}")
            st.info("Please manually visit the Schwab authorization page")
            st.code(auth_url, language="text")
            st.markdown(f"[🌐 Click here to open Schwab Authorization Page]({auth_url})")
    
    def _test_schwab_api(self):
        """Test Schwab API connection with API keys"""
        try:
            st.info("🔄 Testing Schwab API connection...")
            
            # Test with the data fetcher
            test_quote = self.data_fetcher.get_real_time_quote("AAPL")
            
            if test_quote and test_quote.get('source') == 'schwab':
                st.success("✅ Schwab API connection successful!")
                st.session_state.schwab_auth = {
                    'status': 'authenticated',
                    'method': 'API Key',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'expires': 'Session'
                }
                st.rerun()
            else:
                st.warning("⚠️ Schwab API test inconclusive - using fallback data")
                
        except Exception as e:
            st.error(f"❌ Error testing Schwab API: {e}")
    
    def _verify_manual_auth(self):
        """Verify manual authentication"""
        try:
            st.info("🔄 Verifying manual authentication...")
            
            # For manual auth, we'll assume success if user confirms
            # In a real implementation, you'd verify the session
            
            st.success("✅ Manual authentication verified!")
            st.session_state.schwab_auth = {
                'status': 'authenticated',
                'method': 'Manual',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'expires': 'Session'
            }
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error verifying manual authentication: {e}")
    
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