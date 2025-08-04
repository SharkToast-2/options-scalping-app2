import pandas as pd
import numpy as np
from scipy import stats

class RiskManager:
    def __init__(self):
        self.risk_metrics = {}
    
    def calculate_var(self, returns, confidence_level=0.05):
        """Calculate Value at Risk"""
        return np.percentile(returns, confidence_level * 100)
    
    def calculate_cvar(self, returns, confidence_level=0.05):
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        var = self.calculate_var(returns, confidence_level)
        return returns[returns <= var].mean()
    
    def calculate_beta(self, stock_returns, market_returns):
        """Calculate Beta relative to market"""
        covariance = np.cov(stock_returns, market_returns)[0, 1]
        market_variance = np.var(market_returns)
        return covariance / market_variance if market_variance > 0 else 0
    
    def calculate_correlation_matrix(self, returns_df):
        """Calculate correlation matrix for portfolio"""
        return returns_df.corr()
    
    def calculate_portfolio_risk(self, weights, returns_df):
        """Calculate portfolio risk metrics"""
        portfolio_returns = (returns_df * weights).sum(axis=1)
        
        risk_metrics = {
            'volatility': portfolio_returns.std() * np.sqrt(252),
            'var_95': self.calculate_var(portfolio_returns, 0.05),
            'cvar_95': self.calculate_cvar(portfolio_returns, 0.05),
            'skewness': stats.skew(portfolio_returns),
            'kurtosis': stats.kurtosis(portfolio_returns)
        }
        
        return risk_metrics 