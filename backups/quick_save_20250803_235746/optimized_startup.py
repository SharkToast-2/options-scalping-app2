#!/usr/bin/env python3
"""
Optimized Startup Script for Options Scalping Application
"""

import sys
import os
import time
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import optimized components
from data.data_fetcher import OptimizedDataFetcher
from signals.technical_indicators import OptimizedTechnicalIndicators
from signals.sentiment_analysis import SentimentAnalyzer
from trading.signal_processor import SignalProcessor
from trading.risk_manager import RiskManager
from utils.logger import TradeLogger
from utils.performance_monitor import performance_monitor, record_metric, Timer
from config.settings import get_config, BASE_CONFIG

# Configure logging
logging.basicConfig(
    level=getattr(logging, BASE_CONFIG.get("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('options_scalping.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class OptimizedApplication:
    """Optimized application startup and management"""
    
    def __init__(self):
        self.components = {}
        self.startup_time = None
        self.initialized = False
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        # Performance tracking
        self.startup_metrics = {}
    
    async def initialize_async(self):
        """Initialize application components asynchronously"""
        with Timer("app.startup.total"):
            logger.info("🚀 Starting optimized application initialization...")
            
            # Initialize components in parallel
            init_tasks = [
                self._init_data_fetcher(),
                self._init_technical_indicators(),
                self._init_sentiment_analyzer(),
                self._init_signal_processor(),
                self._init_risk_manager(),
                self._init_logger()
            ]
            
            # Wait for all components to initialize
            results = await asyncio.gather(*init_tasks, return_exceptions=True)
            
            # Check for initialization errors
            errors = [r for r in results if isinstance(r, Exception)]
            if errors:
                logger.error(f"❌ Initialization errors: {errors}")
                return False
            
            self.initialized = True
            self.startup_time = time.time()
            
            # Record startup metrics
            record_metric("app.startup.success", 1.0)
            record_metric("app.startup.time", self.startup_time)
            
            logger.info("✅ Application initialized successfully!")
            return True
    
    async def _init_data_fetcher(self):
        """Initialize data fetcher component"""
        with Timer("app.startup.data_fetcher"):
            try:
                data_fetcher = OptimizedDataFetcher()
                
                # Test data source
                test_quote = data_fetcher.get_real_time_quote("AAPL")
                if test_quote:
                    logger.info(f"✅ Data fetcher initialized - Test quote: ${test_quote.get('price', 0):.2f}")
                else:
                    logger.warning("⚠️ Data fetcher initialized but test quote failed")
                
                self.components['data_fetcher'] = data_fetcher
                record_metric("app.startup.data_fetcher.success", 1.0)
                
            except Exception as e:
                logger.error(f"❌ Data fetcher initialization failed: {e}")
                record_metric("app.startup.data_fetcher.success", 0.0)
                raise
    
    async def _init_technical_indicators(self):
        """Initialize technical indicators component"""
        with Timer("app.startup.technical_indicators"):
            try:
                indicators = OptimizedTechnicalIndicators()
                
                # Test indicator calculation
                import pandas as pd
                test_data = pd.DataFrame({
                    'Open': [100, 101, 102],
                    'High': [102, 103, 104],
                    'Low': [99, 100, 101],
                    'Close': [101, 102, 103],
                    'Volume': [1000, 1100, 1200]
                })
                
                test_indicators = indicators._calculate_indicators_vectorized(test_data)
                if test_indicators:
                    logger.info("✅ Technical indicators initialized")
                else:
                    logger.warning("⚠️ Technical indicators initialized but test calculation failed")
                
                self.components['indicators'] = indicators
                record_metric("app.startup.technical_indicators.success", 1.0)
                
            except Exception as e:
                logger.error(f"❌ Technical indicators initialization failed: {e}")
                record_metric("app.startup.technical_indicators.success", 0.0)
                raise
    
    async def _init_sentiment_analyzer(self):
        """Initialize sentiment analyzer component"""
        with Timer("app.startup.sentiment_analyzer"):
            try:
                sentiment_analyzer = SentimentAnalyzer()
                self.components['sentiment_analyzer'] = sentiment_analyzer
                logger.info("✅ Sentiment analyzer initialized")
                record_metric("app.startup.sentiment_analyzer.success", 1.0)
                
            except Exception as e:
                logger.error(f"❌ Sentiment analyzer initialization failed: {e}")
                record_metric("app.startup.sentiment_analyzer.success", 0.0)
                raise
    
    async def _init_signal_processor(self):
        """Initialize signal processor component"""
        with Timer("app.startup.signal_processor"):
            try:
                signal_processor = SignalProcessor()
                self.components['signal_processor'] = signal_processor
                logger.info("✅ Signal processor initialized")
                record_metric("app.startup.signal_processor.success", 1.0)
                
            except Exception as e:
                logger.error(f"❌ Signal processor initialization failed: {e}")
                record_metric("app.startup.signal_processor.success", 0.0)
                raise
    
    async def _init_risk_manager(self):
        """Initialize risk manager component"""
        with Timer("app.startup.risk_manager"):
            try:
                risk_manager = RiskManager()
                self.components['risk_manager'] = risk_manager
                logger.info("✅ Risk manager initialized")
                record_metric("app.startup.risk_manager.success", 1.0)
                
            except Exception as e:
                logger.error(f"❌ Risk manager initialization failed: {e}")
                record_metric("app.startup.risk_manager.success", 0.0)
                raise
    
    async def _init_logger(self):
        """Initialize trade logger component"""
        with Timer("app.startup.logger"):
            try:
                trade_logger = TradeLogger()
                self.components['logger'] = trade_logger
                logger.info("✅ Trade logger initialized")
                record_metric("app.startup.logger.success", 1.0)
                
            except Exception as e:
                logger.error(f"❌ Trade logger initialization failed: {e}")
                record_metric("app.startup.logger.success", 0.0)
                raise
    
    def get_component(self, name: str):
        """Get a component by name"""
        return self.components.get(name)
    
    def get_all_components(self) -> Dict:
        """Get all initialized components"""
        return self.components.copy()
    
    def get_startup_metrics(self) -> Dict:
        """Get startup performance metrics"""
        return {
            'startup_time': self.startup_time,
            'initialized': self.initialized,
            'components_count': len(self.components),
            'performance_summary': performance_monitor.get_metrics_summary()
        }
    
    async def health_check(self) -> Dict:
        """Perform health check on all components"""
        health_status = {
            'overall_healthy': True,
            'components': {},
            'warnings': []
        }
        
        # Check data fetcher
        data_fetcher = self.get_component('data_fetcher')
        if data_fetcher:
            try:
                test_quote = data_fetcher.get_real_time_quote("AAPL")
                health_status['components']['data_fetcher'] = {
                    'healthy': test_quote is not None,
                    'data_source': data_fetcher.get_data_source()
                }
                if not test_quote:
                    health_status['warnings'].append("Data fetcher not returning quotes")
            except Exception as e:
                health_status['components']['data_fetcher'] = {'healthy': False, 'error': str(e)}
                health_status['warnings'].append(f"Data fetcher error: {e}")
        
        # Check technical indicators
        indicators = self.get_component('indicators')
        if indicators:
            health_status['components']['technical_indicators'] = {
                'healthy': True,
                'cache_stats': indicators.get_cache_stats()
            }
        
        # Check system performance
        system_status = performance_monitor.get_system_status()
        health_status['system'] = system_status
        
        # Overall health
        component_health = all(
            comp.get('healthy', False) 
            for comp in health_status['components'].values()
        )
        health_status['overall_healthy'] = component_health and len(health_status['warnings']) == 0
        
        return health_status
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("🧹 Cleaning up application resources...")
        
        # Stop performance monitoring
        performance_monitor.stop_monitoring()
        
        # Shutdown thread pool
        self.executor.shutdown(wait=True)
        
        # Clear component caches
        for component in self.components.values():
            if hasattr(component, 'clear_cache'):
                component.clear_cache()
        
        logger.info("✅ Cleanup completed")

# Global application instance
app = OptimizedApplication()

async def main():
    """Main application startup"""
    try:
        # Initialize application
        success = await app.initialize_async()
        if not success:
            logger.error("❌ Application initialization failed")
            return 1
        
        # Perform health check
        health = await app.health_check()
        if not health['overall_healthy']:
            logger.warning("⚠️ Health check warnings:")
            for warning in health['warnings']:
                logger.warning(f"  - {warning}")
        
        # Start Streamlit app
        logger.info("🌐 Starting Streamlit dashboard...")
        
        # Import and run Streamlit app
        from ui.streamlit_app import main as run_dashboard
        run_dashboard()
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("🛑 Application stopped by user")
        return 0
    except Exception as e:
        logger.error(f"❌ Application error: {e}")
        return 1
    finally:
        await app.cleanup()

def run_sync():
    """Run application synchronously"""
    return asyncio.run(main())

if __name__ == "__main__":
    exit_code = run_sync()
    sys.exit(exit_code) 