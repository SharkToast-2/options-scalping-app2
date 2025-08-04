#!/usr/bin/env python3
"""
Performance Monitoring Utility for Options Scalping Application
"""

import time
import psutil
import threading
import logging
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, deque
import asyncio
import functools

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data class"""
    name: str
    value: float
    timestamp: datetime
    unit: str = ""
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class FunctionProfile:
    """Function profiling data"""
    name: str
    call_count: int = 0
    total_time: float = 0.0
    avg_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    last_call: Optional[datetime] = None

class PerformanceMonitor:
    """Performance monitoring and profiling utility"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history = defaultdict(lambda: deque(maxlen=max_history))
        self.function_profiles = {}
        self.start_time = time.time()
        self.monitoring_enabled = True
        
        # System metrics
        self.system_metrics = {
            'cpu_percent': 0.0,
            'memory_percent': 0.0,
            'disk_usage': 0.0,
            'network_io': {'bytes_sent': 0, 'bytes_recv': 0}
        }
        
        # Performance thresholds
        self.thresholds = {
            'cpu_warning': 80.0,
            'memory_warning': 85.0,
            'disk_warning': 90.0,
            'response_time_warning': 1.0,
            'error_rate_warning': 0.05
        }
        
        # Start monitoring thread
        self._start_monitoring()
    
    def _start_monitoring(self):
        """Start background monitoring thread"""
        def monitor_system():
            while self.monitoring_enabled:
                try:
                    self._update_system_metrics()
                    time.sleep(5)  # Update every 5 seconds
                except Exception as e:
                    logger.error(f"Error in system monitoring: {e}")
        
        self.monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        self.monitor_thread.start()
    
    def _update_system_metrics(self):
        """Update system metrics"""
        try:
            # CPU usage
            self.system_metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.system_metrics['memory_percent'] = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            self.system_metrics['disk_usage'] = disk.percent
            
            # Network I/O
            network = psutil.net_io_counters()
            self.system_metrics['network_io'] = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv
            }
            
            # Record metrics
            self.record_metric('system.cpu_percent', self.system_metrics['cpu_percent'], '%')
            self.record_metric('system.memory_percent', self.system_metrics['memory_percent'], '%')
            self.record_metric('system.disk_usage', self.system_metrics['disk_usage'], '%')
            
        except Exception as e:
            logger.error(f"Error updating system metrics: {e}")
    
    def record_metric(self, name: str, value: float, unit: str = "", tags: Dict[str, str] = None):
        """Record a performance metric"""
        if not self.monitoring_enabled:
            return
        
        metric = PerformanceMetric(
            name=name,
            value=value,
            timestamp=datetime.now(),
            unit=unit,
            tags=tags or {}
        )
        
        self.metrics_history[name].append(metric)
        
        # Check thresholds
        self._check_thresholds(metric)
    
    def _check_thresholds(self, metric: PerformanceMetric):
        """Check if metric exceeds thresholds"""
        if metric.name == 'system.cpu_percent' and metric.value > self.thresholds['cpu_warning']:
            logger.warning(f"High CPU usage: {metric.value}%")
        
        elif metric.name == 'system.memory_percent' and metric.value > self.thresholds['memory_warning']:
            logger.warning(f"High memory usage: {metric.value}%")
        
        elif metric.name == 'system.disk_usage' and metric.value > self.thresholds['disk_warning']:
            logger.warning(f"High disk usage: {metric.value}%")
    
    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile function performance"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self.monitoring_enabled:
                return func(*args, **kwargs)
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                success = False
                raise e
            finally:
                execution_time = time.time() - start_time
                self._update_function_profile(func.__name__, execution_time, success)
            
            return result
        
        return wrapper
    
    def profile_async_function(self, func: Callable) -> Callable:
        """Decorator to profile async function performance"""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not self.monitoring_enabled:
                return await func(*args, **kwargs)
            
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                success = True
            except Exception as e:
                success = False
                raise e
            finally:
                execution_time = time.time() - start_time
                self._update_function_profile(func.__name__, execution_time, success)
            
            return result
        
        return wrapper
    
    def _update_function_profile(self, func_name: str, execution_time: float, success: bool):
        """Update function profiling data"""
        if func_name not in self.function_profiles:
            self.function_profiles[func_name] = FunctionProfile(name=func_name)
        
        profile = self.function_profiles[func_name]
        profile.call_count += 1
        profile.total_time += execution_time
        profile.avg_time = profile.total_time / profile.call_count
        profile.min_time = min(profile.min_time, execution_time)
        profile.max_time = max(profile.max_time, execution_time)
        profile.last_call = datetime.now()
        
        # Record metric
        self.record_metric(f'function.{func_name}.execution_time', execution_time, 'seconds')
        self.record_metric(f'function.{func_name}.success_rate', 1.0 if success else 0.0, '%')
    
    def get_metrics_summary(self, metric_name: str = None, time_window: timedelta = None) -> Dict:
        """Get metrics summary"""
        summary = {}
        
        if metric_name:
            metrics = self.metrics_history.get(metric_name, [])
        else:
            # Get all metrics
            all_metrics = []
            for metrics_list in self.metrics_history.values():
                all_metrics.extend(metrics_list)
            metrics = all_metrics
        
        if time_window:
            cutoff_time = datetime.now() - time_window
            metrics = [m for m in metrics if m.timestamp > cutoff_time]
        
        if metrics:
            values = [m.value for m in metrics]
            summary = {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values),
                'latest': values[-1] if values else None
            }
        
        return summary
    
    def get_function_profiles(self) -> Dict[str, FunctionProfile]:
        """Get function profiling data"""
        return self.function_profiles.copy()
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            'uptime': time.time() - self.start_time,
            'metrics': self.system_metrics.copy(),
            'thresholds': self.thresholds.copy(),
            'warnings': self._get_active_warnings()
        }
    
    def _get_active_warnings(self) -> List[str]:
        """Get active performance warnings"""
        warnings = []
        
        if self.system_metrics['cpu_percent'] > self.thresholds['cpu_warning']:
            warnings.append(f"High CPU usage: {self.system_metrics['cpu_percent']}%")
        
        if self.system_metrics['memory_percent'] > self.thresholds['memory_warning']:
            warnings.append(f"High memory usage: {self.system_metrics['memory_percent']}%")
        
        if self.system_metrics['disk_usage'] > self.thresholds['disk_warning']:
            warnings.append(f"High disk usage: {self.system_metrics['disk_usage']}%")
        
        return warnings
    
    def clear_history(self):
        """Clear metrics history"""
        for metrics_list in self.metrics_history.values():
            metrics_list.clear()
        self.function_profiles.clear()
    
    def export_metrics(self, filename: str = None) -> Dict:
        """Export metrics to file or return as dict"""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'system_status': self.get_system_status(),
            'function_profiles': {
                name: {
                    'call_count': profile.call_count,
                    'total_time': profile.total_time,
                    'avg_time': profile.avg_time,
                    'min_time': profile.min_time,
                    'max_time': profile.max_time,
                    'last_call': profile.last_call.isoformat() if profile.last_call else None
                }
                for name, profile in self.function_profiles.items()
            },
            'metrics_summary': {
                name: self.get_metrics_summary(name)
                for name in self.metrics_history.keys()
            }
        }
        
        if filename:
            import json
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
        
        return export_data
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_enabled = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5)

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# Convenience decorators
def monitor_performance(func: Callable) -> Callable:
    """Decorator to monitor function performance"""
    return performance_monitor.profile_function(func)

def monitor_async_performance(func: Callable) -> Callable:
    """Decorator to monitor async function performance"""
    return performance_monitor.profile_async_function(func)

def record_metric(name: str, value: float, unit: str = "", tags: Dict[str, str] = None):
    """Record a performance metric"""
    performance_monitor.record_metric(name, value, unit, tags)

# Context manager for timing operations
class Timer:
    """Context manager for timing operations"""
    
    def __init__(self, name: str, tags: Dict[str, str] = None):
        self.name = name
        self.tags = tags or {}
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            execution_time = time.time() - self.start_time
            record_metric(f'timer.{self.name}', execution_time, 'seconds', self.tags)

# Utility functions
def get_performance_summary() -> Dict:
    """Get performance summary"""
    return {
        'system_status': performance_monitor.get_system_status(),
        'function_profiles': performance_monitor.get_function_profiles(),
        'metrics_summary': {
            name: performance_monitor.get_metrics_summary(name)
            for name in performance_monitor.metrics_history.keys()
        }
    }

def check_performance_health() -> Dict:
    """Check overall performance health"""
    system_status = performance_monitor.get_system_status()
    warnings = system_status['warnings']
    
    health_status = {
        'healthy': len(warnings) == 0,
        'warnings': warnings,
        'cpu_usage': system_status['metrics']['cpu_percent'],
        'memory_usage': system_status['metrics']['memory_percent'],
        'disk_usage': system_status['metrics']['disk_usage']
    }
    
    return health_status

def optimize_performance():
    """Provide performance optimization recommendations"""
    recommendations = []
    
    # Check system metrics
    system_status = performance_monitor.get_system_status()
    metrics = system_status['metrics']
    
    if metrics['cpu_percent'] > 70:
        recommendations.append("Consider reducing concurrent operations or optimizing CPU-intensive tasks")
    
    if metrics['memory_percent'] > 80:
        recommendations.append("Consider implementing memory caching or reducing data load")
    
    if metrics['disk_usage'] > 85:
        recommendations.append("Consider cleaning up temporary files or increasing disk space")
    
    # Check function profiles
    function_profiles = performance_monitor.get_function_profiles()
    slow_functions = [
        name for name, profile in function_profiles.items()
        if profile.avg_time > 1.0 and profile.call_count > 10
    ]
    
    if slow_functions:
        recommendations.append(f"Consider optimizing slow functions: {', '.join(slow_functions)}")
    
    return recommendations 