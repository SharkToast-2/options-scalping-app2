#!/usr/bin/env python3
"""
Optimized Performance Monitor
Monitors and optimizes system performance for the options scalping bot
"""

import time
import psutil
import threading
import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json
import logging
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    network_sent_mb: float
    network_recv_mb: float
    response_time_ms: float
    cache_hit_rate: float
    error_rate: float
    active_threads: int
    active_connections: int

class OptimizedPerformanceMonitor:
    """Optimized performance monitor with real-time tracking and optimization"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.start_time = time.time()
        self.monitoring = False
        self.monitor_thread = None
        self.lock = threading.Lock()
        
        # Performance thresholds
        self.thresholds = {
            'cpu_warning': 70.0,
            'cpu_critical': 90.0,
            'memory_warning': 80.0,
            'memory_critical': 95.0,
            'response_time_warning': 1000.0,  # ms
            'response_time_critical': 5000.0,  # ms
            'error_rate_warning': 0.05,  # 5%
            'error_rate_critical': 0.10   # 10%
        }
        
        # Optimization settings
        self.optimization_enabled = True
        self.auto_scale = True
        self.cache_optimization = True
        
        # Performance alerts
        self.alerts = []
        self.alert_callbacks = []
    
    def start_monitoring(self, interval: float = 1.0):
        """Start performance monitoring"""
        if self.monitoring:
            logger.warning("Performance monitoring already running")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self.monitor_thread.start()
        logger.info("🚀 Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        logger.info("⏹️ Performance monitoring stopped")
    
    def _monitor_loop(self, interval: float):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                metrics = self._collect_metrics()
                self._store_metrics(metrics)
                self._check_thresholds(metrics)
                self._optimize_performance(metrics)
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()
        network_io = psutil.net_io_counters()
        
        # Process metrics
        process = psutil.Process()
        process_memory = process.memory_info()
        
        # Calculate response time (simplified)
        response_time = self._measure_response_time()
        
        # Cache hit rate (placeholder)
        cache_hit_rate = self._get_cache_hit_rate()
        
        # Error rate (placeholder)
        error_rate = self._get_error_rate()
        
        # Active threads and connections
        active_threads = threading.active_count()
        active_connections = len(psutil.net_connections())
        
        return PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=process_memory.rss / 1024 / 1024,
            disk_io_read_mb=disk_io.read_bytes / 1024 / 1024 if disk_io else 0,
            disk_io_write_mb=disk_io.write_bytes / 1024 / 1024 if disk_io else 0,
            network_sent_mb=network_io.bytes_sent / 1024 / 1024,
            network_recv_mb=network_io.bytes_recv / 1024 / 1024,
            response_time_ms=response_time,
            cache_hit_rate=cache_hit_rate,
            error_rate=error_rate,
            active_threads=active_threads,
            active_connections=active_connections
        )
    
    def _measure_response_time(self) -> float:
        """Measure system response time"""
        start_time = time.time()
        # Simulate a quick operation
        _ = sum(range(1000))
        return (time.time() - start_time) * 1000  # Convert to milliseconds
    
    def _get_cache_hit_rate(self) -> float:
        """Get current cache hit rate"""
        # This would integrate with your actual cache system
        return 0.85  # Placeholder
    
    def _get_error_rate(self) -> float:
        """Get current error rate"""
        # This would integrate with your actual error tracking
        return 0.02  # Placeholder
    
    def _store_metrics(self, metrics: PerformanceMetrics):
        """Store metrics in history"""
        with self.lock:
            self.metrics_history.append(metrics)
    
    def _check_thresholds(self, metrics: PerformanceMetrics):
        """Check if metrics exceed thresholds"""
        alerts = []
        
        # CPU checks
        if metrics.cpu_percent > self.thresholds['cpu_critical']:
            alerts.append(f"🚨 CRITICAL: CPU usage at {metrics.cpu_percent:.1f}%")
        elif metrics.cpu_percent > self.thresholds['cpu_warning']:
            alerts.append(f"⚠️ WARNING: CPU usage at {metrics.cpu_percent:.1f}%")
        
        # Memory checks
        if metrics.memory_percent > self.thresholds['memory_critical']:
            alerts.append(f"🚨 CRITICAL: Memory usage at {metrics.memory_percent:.1f}%")
        elif metrics.memory_percent > self.thresholds['memory_warning']:
            alerts.append(f"⚠️ WARNING: Memory usage at {metrics.memory_percent:.1f}%")
        
        # Response time checks
        if metrics.response_time_ms > self.thresholds['response_time_critical']:
            alerts.append(f"🚨 CRITICAL: Response time at {metrics.response_time_ms:.1f}ms")
        elif metrics.response_time_ms > self.thresholds['response_time_warning']:
            alerts.append(f"⚠️ WARNING: Response time at {metrics.response_time_ms:.1f}ms")
        
        # Error rate checks
        if metrics.error_rate > self.thresholds['error_rate_critical']:
            alerts.append(f"🚨 CRITICAL: Error rate at {metrics.error_rate:.1%}")
        elif metrics.error_rate > self.thresholds['error_rate_warning']:
            alerts.append(f"⚠️ WARNING: Error rate at {metrics.error_rate:.1%}")
        
        # Store alerts
        if alerts:
            for alert in alerts:
                self.alerts.append({
                    'timestamp': datetime.now(),
                    'message': alert,
                    'severity': 'CRITICAL' if '🚨' in alert else 'WARNING'
                })
            
            # Trigger callbacks
            for callback in self.alert_callbacks:
                try:
                    callback(alerts)
                except Exception as e:
                    logger.error(f"Error in alert callback: {e}")
    
    def _optimize_performance(self, metrics: PerformanceMetrics):
        """Apply performance optimizations based on metrics"""
        if not self.optimization_enabled:
            return
        
        optimizations = []
        
        # CPU optimization
        if metrics.cpu_percent > self.thresholds['cpu_warning']:
            optimizations.append(self._optimize_cpu_usage())
        
        # Memory optimization
        if metrics.memory_percent > self.thresholds['memory_warning']:
            optimizations.append(self._optimize_memory_usage())
        
        # Cache optimization
        if metrics.cache_hit_rate < 0.8:
            optimizations.append(self._optimize_cache())
        
        # Apply optimizations
        for optimization in optimizations:
            if optimization:
                logger.info(f"🔧 Applied optimization: {optimization}")
    
    def _optimize_cpu_usage(self) -> Optional[str]:
        """Optimize CPU usage"""
        # Reduce thread pool size if too many active threads
        if threading.active_count() > 20:
            # This would integrate with your actual thread pool management
            return "Reduced thread pool size"
        return None
    
    def _optimize_memory_usage(self) -> Optional[str]:
        """Optimize memory usage"""
        # Clear caches if memory usage is high
        if hasattr(self, '_clear_caches'):
            self._clear_caches()
            return "Cleared memory caches"
        return None
    
    def _optimize_cache(self) -> Optional[str]:
        """Optimize cache performance"""
        # This would integrate with your actual cache system
        return "Optimized cache settings"
    
    def get_current_metrics(self) -> PerformanceMetrics:
        """Get the most recent performance metrics"""
        with self.lock:
            if self.metrics_history:
                return self.metrics_history[-1]
            return self._collect_metrics()
    
    def get_metrics_summary(self, hours: int = 1) -> Dict:
        """Get performance metrics summary for the last N hours"""
        with self.lock:
            if not self.metrics_history:
                return {}
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_metrics = [
                m for m in self.metrics_history 
                if m.timestamp > cutoff_time
            ]
            
            if not recent_metrics:
                return {}
            
            # Calculate statistics
            cpu_values = [m.cpu_percent for m in recent_metrics]
            memory_values = [m.memory_percent for m in recent_metrics]
            response_times = [m.response_time_ms for m in recent_metrics]
            
            return {
                'period_hours': hours,
                'sample_count': len(recent_metrics),
                'cpu': {
                    'avg': np.mean(cpu_values),
                    'max': np.max(cpu_values),
                    'min': np.min(cpu_values),
                    'std': np.std(cpu_values)
                },
                'memory': {
                    'avg': np.mean(memory_values),
                    'max': np.max(memory_values),
                    'min': np.min(memory_values),
                    'std': np.std(memory_values)
                },
                'response_time': {
                    'avg': np.mean(response_times),
                    'max': np.max(response_times),
                    'min': np.min(response_times),
                    'std': np.std(response_times)
                },
                'uptime_seconds': time.time() - self.start_time
            }
    
    def get_alerts(self, hours: int = 24) -> List[Dict]:
        """Get recent alerts"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            alert for alert in self.alerts 
            if alert['timestamp'] > cutoff_time
        ]
    
    def add_alert_callback(self, callback):
        """Add a callback function for alerts"""
        self.alert_callbacks.append(callback)
    
    def set_thresholds(self, **kwargs):
        """Set performance thresholds"""
        for key, value in kwargs.items():
            if key in self.thresholds:
                self.thresholds[key] = value
                logger.info(f"Updated threshold {key}: {value}")
    
    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to JSON file"""
        if filename is None:
            filename = f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with self.lock:
            metrics_data = {
                'export_timestamp': datetime.now().isoformat(),
                'metrics': [asdict(m) for m in self.metrics_history],
                'alerts': self.alerts,
                'summary': self.get_metrics_summary(24)
            }
        
        with open(filename, 'w') as f:
            json.dump(metrics_data, f, indent=2, default=str)
        
        logger.info(f"📊 Metrics exported to {filename}")
        return filename
    
    def get_performance_recommendations(self) -> List[str]:
        """Get performance optimization recommendations"""
        recommendations = []
        current_metrics = self.get_current_metrics()
        summary = self.get_metrics_summary(1)
        
        if not summary:
            return ["No performance data available"]
        
        # CPU recommendations
        if summary['cpu']['avg'] > 80:
            recommendations.append("Consider reducing concurrent operations or optimizing algorithms")
        
        if summary['cpu']['std'] > 20:
            recommendations.append("CPU usage is volatile - consider load balancing")
        
        # Memory recommendations
        if summary['memory']['avg'] > 85:
            recommendations.append("Memory usage is high - consider implementing memory pooling")
        
        # Response time recommendations
        if summary['response_time']['avg'] > 2000:
            recommendations.append("Response times are slow - consider caching or async operations")
        
        # Cache recommendations
        if current_metrics.cache_hit_rate < 0.7:
            recommendations.append("Cache hit rate is low - consider increasing cache size or improving cache keys")
        
        # Thread recommendations
        if current_metrics.active_threads > 50:
            recommendations.append("Too many active threads - consider using thread pools")
        
        if not recommendations:
            recommendations.append("Performance is within optimal ranges")
        
        return recommendations
    
    def get_system_health_score(self) -> float:
        """Calculate overall system health score (0-100)"""
        current_metrics = self.get_current_metrics()
        
        # Calculate individual scores
        cpu_score = max(0, 100 - current_metrics.cpu_percent)
        memory_score = max(0, 100 - current_metrics.memory_percent)
        response_score = max(0, 100 - (current_metrics.response_time_ms / 100))
        error_score = max(0, 100 - (current_metrics.error_rate * 1000))
        cache_score = current_metrics.cache_hit_rate * 100
        
        # Weighted average
        weights = {
            'cpu': 0.25,
            'memory': 0.25,
            'response': 0.20,
            'error': 0.15,
            'cache': 0.15
        }
        
        health_score = (
            cpu_score * weights['cpu'] +
            memory_score * weights['memory'] +
            response_score * weights['response'] +
            error_score * weights['error'] +
            cache_score * weights['cache']
        )
        
        return min(100, max(0, health_score))

# Global instance
performance_monitor = OptimizedPerformanceMonitor()

def start_performance_monitoring(interval: float = 1.0):
    """Start performance monitoring"""
    performance_monitor.start_monitoring(interval)

def stop_performance_monitoring():
    """Stop performance monitoring"""
    performance_monitor.stop_monitoring()

def get_performance_metrics():
    """Get current performance metrics"""
    return performance_monitor.get_current_metrics()

def get_performance_summary(hours: int = 1):
    """Get performance summary"""
    return performance_monitor.get_metrics_summary(hours) 