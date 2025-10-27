import redis
import os
from typing import Optional
import json
from datetime import datetime, timedelta

class RedisManager:
    """Redis manager for caching and session management"""
    
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                password=os.getenv('REDIS_PASSWORD', None),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            # Test connection
            self.redis_client.ping()
            self.redis_available = True
        except Exception as e:
            print(f"Redis not available, using fallback: {e}")
            self.redis_client = None
            self.redis_available = False
    
    def set_cache(self, key: str, value: any, expire_seconds: int = 300):
        """Set cache with expiration"""
        if not self.redis_available:
            return False
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            self.redis_client.setex(key, expire_seconds, value)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def get_cache(self, key: str) -> Optional[str]:
        """Get cache value"""
        if not self.redis_available:
            return None
        try:
            return self.redis_client.get(key)
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def delete_cache(self, key: str) -> bool:
        """Delete cache key"""
        if not self.redis_available:
            return False
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def set_job_cache(self, job_id: int, job_data: dict, expire_seconds: int = 300):
        """Cache job data"""
        key = f"job:{job_id}"
        return self.set_cache(key, job_data, expire_seconds)
    
    def get_job_cache(self, job_id: int) -> Optional[dict]:
        """Get cached job data"""
        key = f"job:{job_id}"
        data = self.get_cache(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return None
        return None
    
    def cache_job_execution(self, job_id: int, execution_time: datetime):
        """Cache job execution time"""
        key = f"job_execution:{job_id}"
        data = {
            "last_execution": execution_time.isoformat(),
            "execution_count": self.get_execution_count(job_id) + 1
        }
        return self.set_cache(key, data, 86400)  # 24 hours
    
    def get_execution_count(self, job_id: int) -> int:
        """Get job execution count"""
        key = f"job_execution:{job_id}"
        data = self.get_cache(key)
        if data:
            try:
                return json.loads(data).get("execution_count", 0)
            except json.JSONDecodeError:
                return 0
        return 0
    
    def set_session(self, session_id: str, data: dict, expire_seconds: int = 3600):
        """Set session data"""
        key = f"session:{session_id}"
        return self.set_cache(key, data, expire_seconds)
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data"""
        key = f"session:{session_id}"
        data = self.get_cache(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return None
        return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        key = f"session:{session_id}"
        return self.delete_cache(key)
    
    def health_check(self) -> bool:
        """Check Redis connection health"""
        if not self.redis_available:
            return False
        try:
            self.redis_client.ping()
            return True
        except Exception as e:
            print(f"Redis health check failed: {e}")
            return False

# Global Redis instance
redis_manager = RedisManager()
