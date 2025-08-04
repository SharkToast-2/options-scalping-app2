#!/usr/bin/env python3
"""
Large-Cap Stock Screener
Identifies large-cap stocks with high growth potential based on technical indicators
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

logger = logging.getLogger(__name__)

class LargeCapScreener:
    """Screens large-cap stocks for growth potential"""
    
    def __init__(self):
        # Large-cap stocks (market cap > $10B) - S&P 500 and major companies
        self.largecap_symbols = [
            # Technology (FAANG + Major Tech)
            'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA', 'NFLX', 'ADBE',
            'CRM', 'ORCL', 'INTU', 'AMD', 'INTC', 'QCOM', 'AVGO', 'MU', 'KLAC', 'LRCX',
            'AMAT', 'ADI', 'TXN', 'MRVL', 'WDC', 'STX', 'HPQ', 'DELL', 'IBM', 'CSCO',
            
            # Healthcare (Major Pharma & Biotech)
            'JNJ', 'PFE', 'UNH', 'ABBV', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN', 'GILD',
            'REGN', 'VRTX', 'BIIB', 'ALXN', 'ILMN', 'DXCM', 'IDXX', 'ALGN', 'WST', 'COO',
            'TFX', 'HOLX', 'BAX', 'ZBH', 'ABMD', 'ISRG', 'EW', 'CI', 'ANTM', 'HUM',
            
            # Consumer (Major Retail & Brands)
            'PG', 'KO', 'PEP', 'WMT', 'COST', 'HD', 'LOW', 'TGT', 'NKE', 'SBUX',
            'MCD', 'YUM', 'CMG', 'CHD', 'CLX', 'ULTA', 'TJX', 'ROST', 'DIS', 'CMCSA',
            'FOX', 'NWSA', 'PARA', 'NFLX', 'AMZN', 'TSLA', 'F', 'GM', 'TM', 'HMC',
            
            # Financial (Major Banks & Financial Services)
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'BLK', 'SCHW', 'ICE', 'CME', 'SPGI',
            'MCO', 'FIS', 'FISV', 'V', 'MA', 'AXP', 'COF', 'DFS', 'SYF', 'TFC',
            'USB', 'PNC', 'C', 'TFC', 'USB', 'PNC', 'WFC', 'JPM', 'BAC', 'C',
            
            # Industrial (Major Industrials)
            'CAT', 'DE', 'BA', 'LMT', 'RTX', 'GD', 'NOC', 'HON', 'GE', 'MMM',
            'EMR', 'ETN', 'ROK', 'DOV', 'XYL', 'FTV', 'AME', 'ITW', 'PH', 'DHR',
            'UPS', 'FDX', 'UNP', 'CSX', 'NSC', 'CP', 'KSU', 'JBHT', 'LSTR', 'ODFL',
            
            # Energy (Major Oil & Gas)
            'XOM', 'CVX', 'COP', 'EOG', 'PXD', 'OXY', 'SLB', 'HAL', 'BKR', 'KMI',
            'ENB', 'TRP', 'WMB', 'OKE', 'MPC', 'VLO', 'PSX', 'HES', 'DVN', 'APA',
            'EOG', 'PXD', 'COP', 'OXY', 'CVX', 'XOM', 'SLB', 'HAL', 'BKR', 'KMI',
            
            # Materials (Major Materials)
            'LIN', 'APD', 'FCX', 'NEM', 'NUE', 'STLD', 'X', 'AA', 'ALB', 'LTHM',
            'DD', 'DOW', 'LIN', 'APD', 'FCX', 'NEM', 'NUE', 'STLD', 'X', 'AA',
            'ALB', 'LTHM', 'DD', 'DOW', 'LIN', 'APD', 'FCX', 'NEM', 'NUE', 'STLD',
            
            # Real Estate (Major REITs)
            'PLD', 'AMT', 'CCI', 'EQIX', 'DLR', 'PSA', 'SPG', 'O', 'DLR', 'WELL',
            'VICI', 'MAA', 'EQR', 'AVB', 'ESS', 'UDR', 'CPT', 'AIV', 'BXP', 'SLG',
            'PLD', 'AMT', 'CCI', 'EQIX', 'DLR', 'PSA', 'SPG', 'O', 'DLR', 'WELL',
            
            # Utilities (Major Utilities)
            'NEE', 'DUK', 'SO', 'D', 'AEP', 'XEL', 'SRE', 'WEC', 'DTE', 'ED',
            'PEG', 'EIX', 'PCG', 'AEE', 'CMS', 'CNP', 'NI', 'ATO', 'LNT', 'BKH',
            'NEE', 'DUK', 'SO', 'D', 'AEP', 'XEL', 'SRE', 'WEC', 'DTE', 'ED',
            
            # Communication (Major Telecom)
            'T', 'VZ', 'TMUS', 'CHTR', 'CMCSA', 'DIS', 'NFLX', 'FOX', 'NWSA', 'PARA',
            'T', 'VZ', 'TMUS', 'CHTR', 'CMCSA', 'DIS', 'NFLX', 'FOX', 'NWSA', 'PARA'
        ]
        
        # Remove duplicates and sort
        self.largecap_symbols = sorted(list(set(self.largecap_symbols)))
        
    def calculate_growth_score(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate growth potential score based on technical indicators"""
        if data.empty or len(data) < 20:
            return {'score': 0, 'rsi': 0, 'macd': 0, 'volume': 0, 'momentum': 0}
        
        try:
            # RSI (Relative Strength Index)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            # RSI Score (30-70 is good, 40-60 is excellent)
            if 40 <= current_rsi <= 60:
                rsi_score = 1.0
            elif 30 <= current_rsi <= 70:
                rsi_score = 0.7
            else:
                rsi_score = 0.3
            
            # MACD (Moving Average Convergence Divergence)
            exp1 = data['Close'].ewm(span=12).mean()
            exp2 = data['Close'].ewm(span=26).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9).mean()
            macd_histogram = macd - signal
            
            # MACD Score (positive histogram is bullish)
            current_macd = macd_histogram.iloc[-1]
            if current_macd > 0:
                macd_score = min(abs(current_macd) / 2, 1.0)  # Normalize to 0-1
            else:
                macd_score = 0.1
            
            # Volume Analysis
            avg_volume = data['Volume'].rolling(window=20).mean()
            current_volume = data['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume.iloc[-1] if avg_volume.iloc[-1] > 0 else 1
            
            # Volume Score (higher volume is better)
            volume_score = min(volume_ratio / 2, 1.0)
            
            # Price Momentum
            price_20d_ago = data['Close'].iloc[-20] if len(data) >= 20 else data['Close'].iloc[0]
            current_price = data['Close'].iloc[-1]
            momentum_pct = ((current_price - price_20d_ago) / price_20d_ago) * 100
            
            # Momentum Score (positive momentum is good, but not too extreme)
            if 5 <= momentum_pct <= 25:
                momentum_score = 1.0
            elif 0 <= momentum_pct <= 30:
                momentum_score = 0.7
            elif momentum_pct > 30:
                momentum_score = 0.3  # Too much growth might be unsustainable
            else:
                momentum_score = 0.2
            
            # Bollinger Bands
            bb_20 = data['Close'].rolling(window=20).mean()
            bb_std = data['Close'].rolling(window=20).std()
            bb_upper = bb_20 + (bb_std * 2)
            bb_lower = bb_20 - (bb_std * 2)
            
            current_price = data['Close'].iloc[-1]
            bb_position = (current_price - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])
            
            # Bollinger Bands Score (not too overbought)
            if 0.3 <= bb_position <= 0.7:
                bb_score = 1.0
            elif 0.2 <= bb_position <= 0.8:
                bb_score = 0.7
            else:
                bb_score = 0.3
            
            # Overall Growth Score (weighted average)
            growth_score = (
                rsi_score * 0.25 +
                macd_score * 0.25 +
                volume_score * 0.20 +
                momentum_score * 0.20 +
                bb_score * 0.10
            )
            
            return {
                'score': round(growth_score, 3),
                'rsi': round(current_rsi, 2),
                'rsi_score': round(rsi_score, 3),
                'macd': round(current_macd, 4),
                'macd_score': round(macd_score, 3),
                'volume_ratio': round(volume_ratio, 2),
                'volume_score': round(volume_score, 3),
                'momentum_pct': round(momentum_pct, 2),
                'momentum_score': round(momentum_score, 3),
                'bb_position': round(bb_position, 3),
                'bb_score': round(bb_score, 3)
            }
            
        except Exception as e:
            logger.error(f"Error calculating growth score: {e}")
            return {'score': 0, 'rsi': 0, 'macd': 0, 'volume': 0, 'momentum': 0}
    
    def get_stock_data(self, symbol: str, data_fetcher) -> Optional[pd.DataFrame]:
        """Get stock data for analysis"""
        try:
            # Get 30 days of daily data
            data = data_fetcher.get_stock_data(symbol, interval="1d", period="1mo")
            if data is not None and not data.empty:
                return data
            return None
        except Exception as e:
            logger.error(f"Error getting data for {symbol}: {e}")
            return None
    
    def analyze_stock(self, symbol: str, data_fetcher) -> Optional[Dict]:
        """Analyze a single stock for growth potential"""
        try:
            data = self.get_stock_data(symbol, data_fetcher)
            if data is None or data.empty:
                return None
            
            # Get current quote
            quote = data_fetcher.get_real_time_quote(symbol)
            if quote is None:
                return None
            
            # Calculate growth score
            growth_metrics = self.calculate_growth_score(data)
            
            return {
                'symbol': symbol,
                'price': quote.get('price', 0),
                'change': quote.get('change', 0),
                'change_percent': quote.get('change_percent', 0),
                'volume': quote.get('volume', 0),
                'growth_score': growth_metrics['score'],
                'rsi': growth_metrics['rsi'],
                'macd': growth_metrics['macd'],
                'volume_ratio': growth_metrics['volume_ratio'],
                'momentum_pct': growth_metrics['momentum_pct'],
                'bb_position': growth_metrics['bb_position'],
                'data_source': quote.get('source', 'unknown')
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            return None
    
    def screen_largecap_stocks(self, data_fetcher, max_workers: int = 5) -> List[Dict]:
        """Screen large-cap stocks for growth potential"""
        logger.info(f"🔍 Screening {len(self.largecap_symbols)} large-cap stocks...")
        
        results = []
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all analysis tasks
            future_to_symbol = {
                executor.submit(self.analyze_stock, symbol, data_fetcher): symbol 
                for symbol in self.largecap_symbols
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    result = future.result()
                    if result and result['growth_score'] > 0.3:  # Only include stocks with decent growth potential
                        results.append(result)
                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")
                
                # Add small delay to avoid overwhelming APIs
                time.sleep(0.1)
        
        # Sort by growth score (highest first)
        results.sort(key=lambda x: x['growth_score'], reverse=True)
        
        logger.info(f"✅ Found {len(results)} stocks with growth potential")
        return results[:10]  # Return top 10

# Global instance
largecap_screener = LargeCapScreener()

def get_top_largecap_stocks(data_fetcher, max_workers: int = 5) -> List[Dict]:
    """Get top 10 large-cap stocks with growth potential"""
    return largecap_screener.screen_largecap_stocks(data_fetcher, max_workers)

def get_largecap_stock_analysis(symbol: str, data_fetcher) -> Optional[Dict]:
    """Get detailed analysis for a specific large-cap stock"""
    return largecap_screener.analyze_stock(symbol, data_fetcher) 