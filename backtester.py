import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Backtester:
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.portfolio_values = []
    
    def simple_ma_strategy(self, data, short_window=20, long_window=50):
        """Simple moving average crossover strategy"""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # Calculate moving averages
        signals['short_ma'] = data['Close'].rolling(window=short_window).mean()
        signals['long_ma'] = data['Close'].rolling(window=long_window).mean()
        
        # Generate signals
        signals['signal'] = np.where(signals['short_ma'] > signals['long_ma'], 1.0, 0.0)
        signals['position'] = signals['signal'].diff()
        
        return signals
    
    def run_backtest(self, data, strategy_func, **strategy_params):
        """Run backtest with given strategy"""
        signals = strategy_func(data, **strategy_params)
        
        # Initialize portfolio
        portfolio = pd.DataFrame(index=signals.index)
        portfolio['positions'] = signals['signal'] * self.capital / data['Close']
        portfolio['cash'] = self.capital - (signals['signal'] * self.capital)
        portfolio['total'] = portfolio['positions'] * data['Close'] + portfolio['cash']
        portfolio['returns'] = portfolio['total'].pct_change()
        
        # Calculate metrics
        total_return = (portfolio['total'].iloc[-1] - self.initial_capital) / self.initial_capital
        annual_return = total_return * (252 / len(data))
        volatility = portfolio['returns'].std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        # Maximum drawdown
        cumulative_returns = (1 + portfolio['returns']).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        results = {
            'total_return': total_return,
            'annual_return': annual_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'portfolio': portfolio,
            'signals': signals
        }
        
        return results 