import pandas as pd
import sqlite3
import json
from datetime import datetime, timedelta
import os

class DataCache:
    def __init__(self, cache_file="stock_cache.db"):
        self.cache_file = cache_file
        self.init_cache()
    
    def init_cache(self):
        """Initialize the cache database"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        # Create cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_cache (
                symbol TEXT,
                period TEXT,
                data TEXT,
                timestamp DATETIME,
                PRIMARY KEY (symbol, period)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_cached_data(self, symbol, period):
        """Get cached data if it exists and is recent"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        # Check if we have recent data (within 1 hour for intraday, 1 day for longer periods)
        cache_duration = 1 if period in ["1d", "5d", "1mo"] else 24
        
        cursor.execute('''
            SELECT data, timestamp FROM stock_cache 
            WHERE symbol = ? AND period = ?
        ''', (symbol, period))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            data_json, timestamp_str = result
            timestamp = datetime.fromisoformat(timestamp_str)
            
            # Check if data is still fresh
            if datetime.now() - timestamp < timedelta(hours=cache_duration):
                try:
                    data_dict = json.loads(data_json)
                    data = pd.DataFrame(data_dict)
                    data.index = pd.to_datetime(data.index)
                    return data
                except:
                    pass
        
        return None
    
    def cache_data(self, symbol, period, data):
        """Cache the data"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        # Convert DataFrame to JSON
        data_json = data.to_json()
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT OR REPLACE INTO stock_cache (symbol, period, data, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (symbol, period, data_json, timestamp))
        
        conn.commit()
        conn.close()
    
    def clear_old_cache(self, days=7):
        """Clear cache older than specified days"""
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        cursor.execute('DELETE FROM stock_cache WHERE timestamp < ?', (cutoff_date,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count 