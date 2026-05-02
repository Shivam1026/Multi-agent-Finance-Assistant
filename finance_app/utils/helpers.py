import json
import os
import functools
import time
from typing import Any, Callable, Optional
from dotenv import load_dotenv

load_dotenv()

class InMemoryCache:
    """
    A simple in-memory cache using a Python dictionary.
  
    """
    def __init__(self):
        # Dictionary structure: {key: (value, expiry_timestamp)}
        self._cache = {}

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            else:
                # Cache expired, remove it
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)

# Global cache instance for shared use
cache_instance = InMemoryCache()

def cache_data(ttl: int = 3600):
    """
    Decorator for caching function results in memory.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique key from function name and arguments
            key_parts = [func.__name__] + list(map(str, args)) + [f"{k}={v}" for k, v in kwargs.items()]
            key = ":".join(key_parts)
            
            cached_val = cache_instance.get(key)
            if cached_val is not None:
                return cached_val
            
            result = func(*args, **kwargs)
            
            # Special handling for DataFrames if they occur (convert to dict for consistency)
            serializable_result = result
            if hasattr(result, 'to_dict'):
                serializable_result = result.to_dict()

            cache_instance.set(key, serializable_result, ttl=ttl)
            return result
        return wrapper
    return decorator
