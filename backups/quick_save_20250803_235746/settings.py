"""
Optimized Configuration Settings for Options Scalping Application
"""

import os
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Base configuration
BASE_CONFIG = {
    "APP_NAME": "Options Scalping Dashboard",
    "VERSION": "2.0.0",
    "DEBUG": os.getenv("DEBUG", "False").lower() == "true",
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "TIMEZONE": "US/Eastern"
}

# API Configuration
API_CONFIG = {
    "ALPACA": {
        "API_KEY": os.getenv("ALPACA_API_KEY", "your_alpaca_api_key_here"),
        "SECRET_KEY": os.getenv("ALPACA_SECRET_KEY", "your_alpaca_secret_key_here"),
        "BASE_URL": "https://paper-api.alpaca.markets",
        "DATA_URL": "https://data.alpaca.markets"
    },
    "SCHWAB": {
        "MARKET_DATA_KEY": os.getenv("SCHWAB_MARKET_DATA_KEY", ""),
        "MARKET_DATA_SECRET": os.getenv("SCHWAB_MARKET_DATA_SECRET", ""),
        "TRADING_KEY": os.getenv("SCHWAB_TRADING_KEY", ""),
        "TRADING_SECRET": os.getenv("SCHWAB_TRADING_SECRET", ""),
        "BASE_URL": "https://api.schwab.com"
    },
    "TOS": {
        "CONSUMER_KEY": os.getenv("TOS_CONSUMER_KEY", ""),
        "CONSUMER_SECRET": os.getenv("TOS_CONSUMER_SECRET", ""),
        "CALLBACK_URL": os.getenv("TOS_CALLBACK_URL", "http://localhost:8501/callback")
    },
    "NEWS_API": {
        "API_KEY": os.getenv("NEWS_API_KEY", ""),
        "BASE_URL": "https://newsapi.org/v2",
        "MAX_REQUESTS_PER_DAY": 1000
    }
}

# Data Configuration
DATA_CONFIG = {
    "CACHE_DURATION": 300,  # 5 minutes
    "RATE_LIMIT_DELAY": 1.0,  # 1 second between requests
    "MAX_SYMBOLS_PER_BATCH": 5,
    "BATCH_DELAY": 1.0,
    "RETRY_ATTEMPTS": 3,
    "RETRY_DELAY": 2.0,
    "TIMEOUT": 30,
    "DEFAULT_INTERVAL": "1m",
    "DEFAULT_PERIOD": "1d"
}

# Trading Configuration
TRADING_CONFIG = {
    "MAX_POSITION_SIZE": 1000,  # Maximum position size in dollars
    "PROFIT_TARGET_PCT": 5.0,   # Profit target percentage
    "STOP_LOSS_PCT": 3.0,       # Stop loss percentage
    "MIN_SIGNAL_STRENGTH": 7,   # Minimum signal strength (1-9)
    "MAX_DAILY_LOSS": 500,      # Maximum daily loss in dollars
    "MAX_CONCURRENT_POSITIONS": 3,
    "MIN_ACCOUNT_BALANCE": 26000,
    "ACCOUNT_BALANCE_BUFFER": 1200,
    "AUTO_TRADING_ENABLED": False,
    "PAPER_TRADING": True
}

# Technical Indicators Configuration
INDICATOR_CONFIG = {
    "RSI": {
        "PERIOD": 14,
        "OVERBOUGHT": 70,
        "OVERSOLD": 30,
        "SPIKE_THRESHOLD": 5
    },
    "MACD": {
        "FAST_PERIOD": 12,
        "SLOW_PERIOD": 26,
        "SIGNAL_PERIOD": 9
    },
    "VWAP": {
        "PERIOD": 20
    },
    "EMA": {
        "SHORT_PERIOD": 20,
        "LONG_PERIOD": 50,
        "TREND_DELTA": 0.001
    },
    "BOLLINGER_BANDS": {
        "PERIOD": 20,
        "STD_DEV": 2.0,
        "WIDTH_THRESHOLD": 0.02
    },
    "ADX": {
        "PERIOD": 14,
        "THRESHOLD": 25
    },
    "OBV": {
        "MOMENTUM_PERIOD": 10
    },
    "ATR": {
        "PERIOD": 14,
        "VOLATILITY_THRESHOLD": 0.01
    },
    "STOCH_RSI": {
        "PERIOD": 14,
        "K_PERIOD": 3,
        "D_PERIOD": 3,
        "OVERBOUGHT": 80,
        "OVERSOLD": 20
    }
}

# Target Symbols for Scalping
TARGET_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "META", "NVDA", "NFLX", "AMD", "INTC",
    "SPY", "QQQ", "IWM", "VTI", "VOO"
]

# UI Configuration
UI_CONFIG = {
    "CHART_HEIGHT": 500,
    "REFRESH_INTERVAL": 30,  # seconds
    "MAX_DISPLAY_SYMBOLS": 10,
    "DEFAULT_THEME": "light",
    "SIDEBAR_WIDTH": 300
}

# Risk Management Configuration
RISK_CONFIG = {
    "MAX_POSITION_RISK": 0.02,  # 2% of account per position
    "MAX_PORTFOLIO_RISK": 0.06,  # 6% of account total
    "DAILY_LOSS_LIMIT": 0.05,   # 5% daily loss limit
    "CORRELATION_LIMIT": 0.7,   # Maximum correlation between positions
    "VOLATILITY_LIMIT": 0.5,    # Maximum position volatility
    "LIQUIDITY_MINIMUM": 1000000  # Minimum volume for position
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "CACHE_ENABLED": True,
    "CACHE_TTL": 300,  # 5 minutes
    "MAX_CACHE_SIZE": 1000,
    "ASYNC_ENABLED": True,
    "THREAD_POOL_SIZE": 5,
    "BATCH_PROCESSING": True,
    "COMPRESSION_ENABLED": True
}

# Logging Configuration
LOGGING_CONFIG = {
    "LEVEL": "INFO",
    "FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "FILE": "options_scalping.log",
    "MAX_SIZE": 10 * 1024 * 1024,  # 10MB
    "BACKUP_COUNT": 5,
    "ENABLE_CONSOLE": True
}

# Database Configuration
DB_CONFIG = {
    "TYPE": "sqlite",
    "PATH": "stock_data.db",
    "BACKUP_ENABLED": True,
    "BACKUP_INTERVAL": 24,  # hours
    "MAX_CONNECTIONS": 10
}

# Notification Configuration
NOTIFICATION_CONFIG = {
    "EMAIL_ENABLED": False,
    "EMAIL_SMTP": "smtp.gmail.com",
    "EMAIL_PORT": 587,
    "EMAIL_USER": os.getenv("EMAIL_USER", ""),
    "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD", ""),
    "DISCORD_ENABLED": False,
    "DISCORD_WEBHOOK": os.getenv("DISCORD_WEBHOOK", ""),
    "TELEGRAM_ENABLED": False,
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID", "")
}

# Market Hours Configuration
MARKET_HOURS = {
    "REGULAR": {
        "OPEN": "09:30",
        "CLOSE": "16:00",
        "TIMEZONE": "US/Eastern"
    },
    "PRE_MARKET": {
        "OPEN": "04:00",
        "CLOSE": "09:30",
        "TIMEZONE": "US/Eastern"
    },
    "AFTER_HOURS": {
        "OPEN": "16:00",
        "CLOSE": "20:00",
        "TIMEZONE": "US/Eastern"
    }
}

# Signal Weights Configuration
SIGNAL_WEIGHTS = {
    "RSI_SPIKE": 1.0,
    "MACD_TREND": 1.0,
    "VWAP_POSITION": 1.0,
    "EMA_TREND": 1.0,
    "BB_WIDTH": 1.0,
    "ADX": 1.0,
    "OBV_MOMENTUM": 1.0,
    "ATR_VOLATILITY": 1.0,
    "SENTIMENT": 1.0
}

# Scalping Strategy Configuration
SCALPING_CONFIG = {
    "ENTRY_SIGNALS": {
        "RSI_OVERSOLD": True,
        "RSI_OVERBOUGHT": True,
        "MACD_CROSSOVER": True,
        "VWAP_BOUNCE": True,
        "EMA_TREND": True,
        "BB_SQUEEZE": True,
        "ADX_STRONG": True,
        "OBV_CONFIRMATION": True
    },
    "EXIT_SIGNALS": {
        "PROFIT_TARGET": True,
        "STOP_LOSS": True,
        "TIME_BASED": True,
        "SIGNAL_REVERSAL": True,
        "VOLUME_DROP": True
    },
    "TIMING": {
        "MIN_HOLD_TIME": 30,  # seconds
        "MAX_HOLD_TIME": 300,  # 5 minutes
        "ENTRY_DELAY": 5,     # seconds
        "EXIT_DELAY": 2       # seconds
    },
    "FILTERS": {
        "MIN_VOLUME": 1000000,
        "MIN_PRICE": 10.0,
        "MAX_SPREAD": 0.02,   # 2%
        "MIN_MARKET_CAP": 1000000000  # 1B
    }
}

# Backtesting Configuration
BACKTEST_CONFIG = {
    "START_DATE": "2024-01-01",
    "END_DATE": datetime.now().strftime("%Y-%m-%d"),
    "INITIAL_CAPITAL": 100000,
    "COMMISSION": 0.005,  # $0.50 per contract
    "SLIPPAGE": 0.001,    # 0.1%
    "POSITION_SIZING": "fixed",  # fixed, kelly, optimal
    "REBALANCE_FREQ": "daily"
}

# Optimization Configuration
OPTIMIZATION_CONFIG = {
    "PARAMETER_RANGES": {
        "RSI_PERIOD": [10, 20],
        "MACD_FAST": [8, 16],
        "MACD_SLOW": [20, 30],
        "VWAP_PERIOD": [15, 25],
        "EMA_SHORT": [15, 25],
        "EMA_LONG": [40, 60]
    },
    "OPTIMIZATION_METHOD": "genetic",  # genetic, grid, bayesian
    "POPULATION_SIZE": 50,
    "GENERATIONS": 100,
    "CROSSOVER_RATE": 0.8,
    "MUTATION_RATE": 0.1
}

# Machine Learning Configuration
ML_CONFIG = {
    "ENABLED": True,
    "MODEL_TYPE": "ensemble",  # ensemble, neural_network, random_forest
    "FEATURES": [
        "rsi", "macd", "vwap", "ema_trend", "bb_width",
        "adx", "obv", "atr", "volume", "price_change"
    ],
    "TARGET": "next_price_direction",  # next_price_direction, volatility, volume
    "TRAINING_SPLIT": 0.8,
    "VALIDATION_SPLIT": 0.1,
    "TEST_SPLIT": 0.1,
    "RETRAIN_FREQUENCY": 24,  # hours
    "MIN_TRAINING_SAMPLES": 1000
}

# Sentiment Analysis Configuration
SENTIMENT_CONFIG = {
    "ENABLED": True,
    "SOURCES": ["news", "social", "earnings"],
    "MODEL": "finbert",  # finbert, vader, textblob
    "UPDATE_FREQUENCY": 60,  # minutes
    "MIN_CONFIDENCE": 0.6,
    "WEIGHT": 0.2  # Weight in overall signal calculation
}

# Webhook Configuration
WEBHOOK_CONFIG = {
    "ENABLED": False,
    "URL": os.getenv("WEBHOOK_URL", ""),
    "SECRET": os.getenv("WEBHOOK_SECRET", ""),
    "EVENTS": ["trade_executed", "signal_generated", "risk_alert"]
}

# Security Configuration
SECURITY_CONFIG = {
    "API_KEY_ENCRYPTION": True,
    "SESSION_TIMEOUT": 3600,  # 1 hour
    "MAX_LOGIN_ATTEMPTS": 5,
    "PASSWORD_MIN_LENGTH": 8,
    "ENABLE_2FA": False,
    "ALLOWED_IPS": []
}

# Development Configuration
DEV_CONFIG = {
    "MOCK_DATA_ENABLED": True,
    "FAST_REFRESH": True,
    "DEBUG_MODE": True,
    "PROFILING_ENABLED": False,
    "TEST_MODE": False
}

# Load custom configuration from file if exists
def load_custom_config() -> Dict[str, Any]:
    """Load custom configuration from config.json"""
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                custom_config = json.load(f)
                return custom_config
    except Exception as e:
        print(f"Warning: Could not load custom config: {e}")
    return {}

# Merge custom configuration
CUSTOM_CONFIG = load_custom_config()

def get_config(section: str) -> Dict[str, Any]:
    """Get configuration section with custom overrides"""
    config_map = {
        "api": API_CONFIG,
        "data": DATA_CONFIG,
        "trading": TRADING_CONFIG,
        "indicators": INDICATOR_CONFIG,
        "ui": UI_CONFIG,
        "risk": RISK_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "logging": LOGGING_CONFIG,
        "database": DB_CONFIG,
        "notifications": NOTIFICATION_CONFIG,
        "market_hours": MARKET_HOURS,
        "scalping": SCALPING_CONFIG,
        "backtest": BACKTEST_CONFIG,
        "optimization": OPTIMIZATION_CONFIG,
        "ml": ML_CONFIG,
        "sentiment": SENTIMENT_CONFIG,
        "webhook": WEBHOOK_CONFIG,
        "security": SECURITY_CONFIG,
        "dev": DEV_CONFIG
    }
    
    base_config = config_map.get(section.lower(), {})
    
    # Apply custom overrides
    if section.lower() in CUSTOM_CONFIG:
        base_config.update(CUSTOM_CONFIG[section.lower()])
    
    return base_config

def update_config(section: str, updates: Dict[str, Any]) -> bool:
    """Update configuration section"""
    try:
        if not os.path.exists("config.json"):
            config_data = {}
        else:
            with open("config.json", "r") as f:
                config_data = json.load(f)
        
        if section.lower() not in config_data:
            config_data[section.lower()] = {}
        
        config_data[section.lower()].update(updates)
        
        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

def get_all_config() -> Dict[str, Any]:
    """Get all configuration as a single dictionary"""
    return {
        "base": BASE_CONFIG,
        "api": get_config("api"),
        "data": get_config("data"),
        "trading": get_config("trading"),
        "indicators": get_config("indicators"),
        "ui": get_config("ui"),
        "risk": get_config("risk"),
        "performance": get_config("performance"),
        "logging": get_config("logging"),
        "database": get_config("database"),
        "notifications": get_config("notifications"),
        "market_hours": get_config("market_hours"),
        "scalping": get_config("scalping"),
        "backtest": get_config("backtest"),
        "optimization": get_config("optimization"),
        "ml": get_config("ml"),
        "sentiment": get_config("sentiment"),
        "webhook": get_config("webhook"),
        "security": get_config("security"),
        "dev": get_config("dev"),
        "target_symbols": TARGET_SYMBOLS
    }

# Export all configurations
__all__ = [
    "BASE_CONFIG", "API_CONFIG", "DATA_CONFIG", "TRADING_CONFIG",
    "INDICATOR_CONFIG", "TARGET_SYMBOLS", "UI_CONFIG", "RISK_CONFIG",
    "PERFORMANCE_CONFIG", "LOGGING_CONFIG", "DB_CONFIG", "NOTIFICATION_CONFIG",
    "MARKET_HOURS", "SCALPING_CONFIG", "BACKTEST_CONFIG", "OPTIMIZATION_CONFIG",
    "ML_CONFIG", "SENTIMENT_CONFIG", "WEBHOOK_CONFIG", "SECURITY_CONFIG",
    "DEV_CONFIG", "SIGNAL_WEIGHTS", "get_config", "update_config", "get_all_config"
] 