#!/usr/bin/env python3
"""
Sentiment Analysis for Options Scalping Bot
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
import requests
import time

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer"""
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def get_sentiment_score(self, ticker: str) -> float:
        """Get sentiment score for a ticker (-1 to 1)"""
        try:
            # Check cache first
            if ticker in self.cache:
                cached_data, timestamp = self.cache[ticker]
                if time.time() - timestamp < self.cache_duration:
                    return cached_data
            
            # Calculate sentiment using multiple sources
            sentiment_score = self.calculate_sentiment(ticker)
            
            # Cache the result
            self.cache[ticker] = (sentiment_score, time.time())
            
            return sentiment_score
            
        except Exception as e:
            print(f"Error getting sentiment for {ticker}: {e}")
            return 0.0
    
    def calculate_sentiment(self, ticker: str) -> float:
        """Calculate sentiment using multiple indicators"""
        try:
            # Get various sentiment indicators
            news_sentiment = self.get_news_sentiment(ticker)
            social_sentiment = self.get_social_sentiment(ticker)
            technical_sentiment = self.get_technical_sentiment(ticker)
            
            # Weight the different sentiment sources
            weighted_sentiment = (
                news_sentiment * 0.4 +
                social_sentiment * 0.3 +
                technical_sentiment * 0.3
            )
            
            # Normalize to -1 to 1 range
            return max(-1.0, min(1.0, weighted_sentiment))
            
        except Exception as e:
            print(f"Error calculating sentiment: {e}")
            return 0.0
    
    def get_news_sentiment(self, ticker: str) -> float:
        """Get news sentiment score"""
        try:
            # Simulate news sentiment analysis
            # In a real implementation, you would:
            # 1. Fetch news articles about the ticker
            # 2. Use NLP to analyze sentiment
            # 3. Return a score between -1 and 1
            
            # For now, return a random sentiment score
            # This simulates the variability of news sentiment
            import random
            return random.uniform(-0.5, 0.5)
            
        except Exception as e:
            print(f"Error getting news sentiment: {e}")
            return 0.0
    
    def get_social_sentiment(self, ticker: str) -> float:
        """Get social media sentiment score"""
        try:
            # Simulate social media sentiment analysis
            # In a real implementation, you would:
            # 1. Fetch social media posts about the ticker
            # 2. Analyze sentiment using NLP
            # 3. Return a score between -1 and 1
            
            # For now, return a random sentiment score
            import random
            return random.uniform(-0.3, 0.3)
            
        except Exception as e:
            print(f"Error getting social sentiment: {e}")
            return 0.0
    
    def get_technical_sentiment(self, ticker: str) -> float:
        """Get technical sentiment based on price action"""
        try:
            # This would analyze technical patterns for sentiment
            # For now, return a neutral score
            return 0.0
            
        except Exception as e:
            print(f"Error getting technical sentiment: {e}")
            return 0.0
    
    def analyze_sentiment_trend(self, ticker: str, period: str = "1d") -> Dict:
        """Analyze sentiment trend over time"""
        try:
            # Simulate sentiment trend analysis
            current_sentiment = self.get_sentiment_score(ticker)
            
            # Simulate historical sentiment
            import random
            historical_sentiments = [
                current_sentiment + random.uniform(-0.2, 0.2) for _ in range(5)
            ]
            
            # Calculate trend
            if len(historical_sentiments) >= 2:
                trend = (historical_sentiments[-1] - historical_sentiments[0]) / len(historical_sentiments)
            else:
                trend = 0.0
            
            return {
                'current_sentiment': current_sentiment,
                'historical_sentiments': historical_sentiments,
                'trend': trend,
                'trend_direction': 'positive' if trend > 0.05 else 'negative' if trend < -0.05 else 'neutral'
            }
            
        except Exception as e:
            print(f"Error analyzing sentiment trend: {e}")
            return {
                'current_sentiment': 0.0,
                'historical_sentiments': [],
                'trend': 0.0,
                'trend_direction': 'neutral'
            }
    
    def get_sentiment_signal(self, ticker: str) -> Dict:
        """Get sentiment-based trading signal"""
        try:
            sentiment_score = self.get_sentiment_score(ticker)
            sentiment_trend = self.analyze_sentiment_trend(ticker)
            
            # Generate signal based on sentiment
            signal = 'HOLD'
            confidence = 0
            
            if sentiment_score > 0.3:
                signal = 'BUY'
                confidence = min(100, sentiment_score * 100)
            elif sentiment_score < -0.3:
                signal = 'SELL'
                confidence = min(100, abs(sentiment_score) * 100)
            
            # Adjust based on trend
            if sentiment_trend['trend_direction'] == 'positive' and signal == 'BUY':
                confidence += 10
            elif sentiment_trend['trend_direction'] == 'negative' and signal == 'SELL':
                confidence += 10
            
            return {
                'signal': signal,
                'confidence': confidence,
                'sentiment_score': sentiment_score,
                'trend': sentiment_trend['trend_direction'],
                'reasons': self.get_sentiment_reasons(sentiment_score, sentiment_trend)
            }
            
        except Exception as e:
            print(f"Error getting sentiment signal: {e}")
            return {
                'signal': 'HOLD',
                'confidence': 0,
                'sentiment_score': 0.0,
                'trend': 'neutral',
                'reasons': ['Error analyzing sentiment']
            }
    
    def get_sentiment_reasons(self, sentiment_score: float, sentiment_trend: Dict) -> list:
        """Get reasons for sentiment signal"""
        reasons = []
        
        if sentiment_score > 0.3:
            reasons.append("Positive sentiment")
        elif sentiment_score < -0.3:
            reasons.append("Negative sentiment")
        
        if sentiment_trend['trend_direction'] == 'positive':
            reasons.append("Improving sentiment trend")
        elif sentiment_trend['trend_direction'] == 'negative':
            reasons.append("Deteriorating sentiment trend")
        
        if abs(sentiment_score) < 0.1:
            reasons.append("Neutral sentiment")
        
        return reasons
    
    def clear_cache(self):
        """Clear sentiment cache"""
        self.cache.clear()
        print("Sentiment cache cleared")
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'cached_tickers': len(self.cache),
            'cache_duration': self.cache_duration
        } 