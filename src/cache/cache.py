"""
Redis cache implementation
Single Responsibility: Handle caching operations
"""
import redis
import json
from typing import Dict, Any, Optional
from interfaces import CacheInterface

class RedisCache(CacheInterface):
    """Redis implementation of our caching interface"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, password: Optional[str] = None):
        try:
            self._redis = redis.Redis(
                host=host,
                port=port,
                password=password,
                decode_responses=True
            )
            self._redis.ping()
            print("✅ Connected to Redis")
        except Exception as e:
            print(f"⚠️ Redis connection failed: {e}")
            self._redis = None
            
    def save(self, key: str, data: Any, expire_seconds: int = 3600) -> bool:
        """Save data to Redis with expiration"""
        if not self._redis:
            return False
            
        try:
            serialized = (
                json.dumps(data) if isinstance(data, (dict, list)) 
                else str(data)
            )
            return bool(
                self._redis.setex(key, expire_seconds, serialized)
            )
        except Exception as e:
            print(f"⚠️ Redis save error: {e}")
            return False
            
    def get(self, key: str) -> Optional[Any]:
        """Get data from Redis"""
        if not self._redis:
            return None
            
        try:
            data = self._redis.get(key)
            if not data:
                return None
                
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        except Exception as e:
            print(f"⚠️ Redis get error: {e}")
            return None
            
    def delete(self, key: str) -> bool:
        """Delete data from Redis"""
        if not self._redis:
            return False
            
        try:
            return bool(self._redis.delete(key))
        except Exception as e:
            print(f"⚠️ Redis delete error: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check Redis connection status"""
        if not self._redis:
            return False
        try:
            return bool(self._redis.ping())
        except:
            return False