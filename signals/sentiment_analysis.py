"""
Sentiment analysis module for options scalping signals
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

from config.settings import API_CONFIG, SENTIMENT_CONFIG

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Sentiment analysis for market news and social media"""
    
    def __init__(self):
        self.news_api_key = API_CONFIG["NEWS_API"]["API_KEY"]
        self.news_base_url = API_CONFIG["NEWS_API"]["BASE_URL"]
        self.analyzer = SentimentIntensityAnalyzer()
        self.config = SENTIMENT_CONFIG
        
        # Cache for sentiment results
        self.sentiment_cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def get_news_sentiment(self, symbol: str, hours_back: int = None) -> Dict:
        """Get sentiment analysis from news articles"""
        try:
            hours_back = hours_back or self.config["NEWS_LOOKBACK_HOURS"]
            
            # Check cache first
            cache_key = f"{symbol}_{hours_back}"
            if cache_key in self.sentiment_cache:
                cached_time, cached_result = self.sentiment_cache[cache_key]
                if datetime.now() - cached_time < timedelta(seconds=self.cache_duration):
                    return cached_result
            
            # Fetch news articles
            articles = self._fetch_news_articles(symbol, hours_back)
            
            if not articles:
                return {
                    "sentiment_score": 0.0,
                    "sentiment_label": "neutral",
                    "article_count": 0,
                    "confidence": 0.0
                }
            
            # Analyze sentiment for each article
            sentiments = []
            for article in articles:
                sentiment = self._analyze_article_sentiment(article)
                if sentiment:
                    sentiments.append(sentiment)
            
            if not sentiments:
                return {
                    "sentiment_score": 0.0,
                    "sentiment_label": "neutral",
                    "article_count": 0,
                    "confidence": 0.0
                }
            
            # Calculate aggregate sentiment
            sentiment_df = pd.DataFrame(sentiments)
            avg_sentiment = sentiment_df['compound'].mean()
            confidence = sentiment_df['compound'].std()  # Lower std = higher confidence
            
            # Determine sentiment label
            if avg_sentiment > self.config["POSITIVE_THRESHOLD"]:
                label = "positive"
            elif avg_sentiment < self.config["NEGATIVE_THRESHOLD"]:
                label = "negative"
            else:
                label = "neutral"
            
            result = {
                "sentiment_score": avg_sentiment,
                "sentiment_label": label,
                "article_count": len(sentiments),
                "confidence": 1.0 - min(confidence, 1.0),  # Convert to confidence (0-1)
                "articles": articles[:5]  # Include first 5 articles for reference
            }
            
            # Cache the result
            self.sentiment_cache[cache_key] = (datetime.now(), result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting news sentiment for {symbol}: {e}")
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "neutral",
                "article_count": 0,
                "confidence": 0.0
            }
    
    def _fetch_news_articles(self, symbol: str, hours_back: int) -> List[Dict]:
        """Fetch news articles from NewsAPI"""
        try:
            if not self.news_api_key:
                logger.warning("No NewsAPI key provided, using mock data")
                return self._get_mock_news_articles(symbol)
            
            # Calculate time range
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours_back)
            
            # NewsAPI parameters
            params = {
                'q': f'"{symbol}" OR "{symbol} stock" OR "{symbol} shares"',
                'from': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'to': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'language': 'en',
                'sortBy': 'relevancy',
                'pageSize': self.config["MAX_NEWS_ARTICLES"],
                'apiKey': self.news_api_key
            }
            
            response = requests.get(f"{self.news_base_url}/everything", params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                # Filter and clean articles
                filtered_articles = []
                for article in articles:
                    if self._is_relevant_article(article, symbol):
                        filtered_articles.append(article)
                
                return filtered_articles[:self.config["MAX_NEWS_ARTICLES"]]
            
            else:
                logger.error(f"NewsAPI error: {response.status_code} - {response.text}")
                return self._get_mock_news_articles(symbol)
                
        except Exception as e:
            logger.error(f"Error fetching news articles: {e}")
            return self._get_mock_news_articles(symbol)
    
    def _is_relevant_article(self, article: Dict, symbol: str) -> bool:
        """Check if article is relevant to the symbol"""
        try:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            content = article.get('content', '').lower()
            
            # Check if symbol appears in title or description
            symbol_lower = symbol.lower()
            if symbol_lower in title or symbol_lower in description:
                return True
            
            # Check for stock-related keywords
            stock_keywords = ['stock', 'shares', 'trading', 'market', 'earnings', 'revenue', 'profit']
            if any(keyword in title or keyword in description for keyword in stock_keywords):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking article relevance: {e}")
            return False
    
    def _analyze_article_sentiment(self, article: Dict) -> Optional[Dict]:
        """Analyze sentiment of a single article"""
        try:
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            
            # Combine text for analysis
            text = f"{title}. {description}. {content}"
            
            # Clean text
            text = self._clean_text(text)
            
            if not text.strip():
                return None
            
            # Analyze sentiment
            sentiment_scores = self.analyzer.polarity_scores(text)
            
            return {
                'title': title,
                'compound': sentiment_scores['compound'],
                'positive': sentiment_scores['pos'],
                'negative': sentiment_scores['neg'],
                'neutral': sentiment_scores['neu']
            }
            
        except Exception as e:
            logger.error(f"Error analyzing article sentiment: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean text for sentiment analysis"""
        try:
            # Remove special characters and extra whitespace
            import re
            text = re.sub(r'[^\w\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        except Exception as e:
            logger.error(f"Error cleaning text: {e}")
            return text
    
    def _get_mock_news_articles(self, symbol: str) -> List[Dict]:
        """Generate mock news articles for testing"""
        import random
        
        mock_articles = [
            {
                'title': f'{symbol} Reports Strong Q4 Earnings',
                'description': f'{symbol} exceeded analyst expectations with record quarterly revenue.',
                'content': f'{symbol} has shown remarkable growth in the latest quarter.',
                'publishedAt': datetime.now().isoformat()
            },
            {
                'title': f'{symbol} Announces New Product Launch',
                'description': f'{symbol} is expanding its product portfolio with innovative solutions.',
                'content': f'The new product from {symbol} is expected to drive future growth.',
                'publishedAt': datetime.now().isoformat()
            },
            {
                'title': f'Analysts Upgrade {symbol} Price Target',
                'description': f'Multiple analysts have raised their price targets for {symbol}.',
                'content': f'{symbol} continues to receive positive analyst coverage.',
                'publishedAt': datetime.now().isoformat()
            }
        ]
        
        # Randomly select articles and add some negative ones occasionally
        if random.random() < 0.3:  # 30% chance of negative news
            mock_articles.append({
                'title': f'{symbol} Faces Regulatory Challenges',
                'description': f'{symbol} is dealing with new regulatory requirements.',
                'content': f'The regulatory environment for {symbol} has become more challenging.',
                'publishedAt': datetime.now().isoformat()
            })
        
        return random.sample(mock_articles, min(len(mock_articles), 3))
    
    def get_sentiment_signal(self, sentiment_data: Dict) -> Tuple[bool, bool]:
        """Get sentiment signals for call/put options"""
        try:
            sentiment_score = sentiment_data.get('sentiment_score', 0.0)
            confidence = sentiment_data.get('confidence', 0.0)
            
            # Only use sentiment if confidence is high enough
            if confidence < 0.5:
                return False, False
            
            # Call signal: positive sentiment above threshold
            call_signal = sentiment_score > self.config["POSITIVE_THRESHOLD"]
            
            # Put signal: negative sentiment below threshold
            put_signal = sentiment_score < self.config["NEGATIVE_THRESHOLD"]
            
            return call_signal, put_signal
            
        except Exception as e:
            logger.error(f"Error getting sentiment signal: {e}")
            return False, False
    
    def get_market_sentiment_summary(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get sentiment summary for multiple symbols"""
        try:
            summary = {}
            
            for symbol in symbols:
                try:
                    sentiment = self.get_news_sentiment(symbol)
                    summary[symbol] = sentiment
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error getting sentiment for {symbol}: {e}")
                    summary[symbol] = {
                        "sentiment_score": 0.0,
                        "sentiment_label": "neutral",
                        "article_count": 0,
                        "confidence": 0.0
                    }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting market sentiment summary: {e}")
            return {}
    
    def analyze_social_sentiment(self, symbol: str) -> Dict:
        """Analyze social media sentiment (placeholder for future implementation)"""
        try:
            # This is a placeholder for social media sentiment analysis
            # In a real implementation, you would integrate with Twitter API, Reddit API, etc.
            
            # For now, return mock data
            import random
            
            return {
                "social_sentiment_score": random.uniform(-0.5, 0.5),
                "social_volume": random.randint(100, 1000),
                "trending": random.choice([True, False]),
                "platforms": ["twitter", "reddit"],
                "confidence": random.uniform(0.3, 0.8)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing social sentiment: {e}")
            return {
                "social_sentiment_score": 0.0,
                "social_volume": 0,
                "trending": False,
                "platforms": [],
                "confidence": 0.0
            }
    
    def get_combined_sentiment(self, symbol: str) -> Dict:
        """Get combined sentiment from news and social media"""
        try:
            news_sentiment = self.get_news_sentiment(symbol)
            social_sentiment = self.analyze_social_sentiment(symbol)
            
            # Weight the sentiments (news is more reliable)
            news_weight = 0.7
            social_weight = 0.3
            
            combined_score = (
                news_sentiment.get('sentiment_score', 0.0) * news_weight +
                social_sentiment.get('social_sentiment_score', 0.0) * social_weight
            )
            
            # Determine combined label
            if combined_score > self.config["POSITIVE_THRESHOLD"]:
                label = "positive"
            elif combined_score < self.config["NEGATIVE_THRESHOLD"]:
                label = "negative"
            else:
                label = "neutral"
            
            return {
                "combined_score": combined_score,
                "combined_label": label,
                "news_sentiment": news_sentiment,
                "social_sentiment": social_sentiment,
                "confidence": (news_sentiment.get('confidence', 0.0) + social_sentiment.get('confidence', 0.0)) / 2
            }
            
        except Exception as e:
            logger.error(f"Error getting combined sentiment: {e}")
            return {
                "combined_score": 0.0,
                "combined_label": "neutral",
                "news_sentiment": {},
                "social_sentiment": {},
                "confidence": 0.0
            } 