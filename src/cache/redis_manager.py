"""
Simple Redis manager for job scheduling
"""
from redis import Redis
import logging
import json
from datetime import datetime
from src.core.settings import settings

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self):
        self.redis = Redis(
            host="localhost",  # Simplified for local development
            port=6379,
            db=0,
            decode_responses=True
        )
        
    def cache_job_status(self, job_id: int, status: str):
        """Cache job status in Redis"""
        try:
            key = f"job:{job_id}:status"
            self.redis.set(key, status)
            # Also store the timestamp
            self.redis.set(f"job:{job_id}:last_updated", datetime.now().isoformat())
            logger.info(f"Cached status for job {job_id}: {status}")
        except Exception as e:
            logger.error(f"Error caching job status: {str(e)}")

    def get_job_status(self, job_id: int) -> dict:
        """Get job status from Redis cache"""
        try:
            status = self.redis.get(f"job:{job_id}:status")
            last_updated = self.redis.get(f"job:{job_id}:last_updated")
            return {
                "status": status if status else "unknown",
                "last_updated": last_updated
            }
        except Exception as e:
            logger.error(f"Error getting job status: {str(e)}")
            return {"status": "unknown", "last_updated": None}

    def get_queue_info(self):
        """Get basic Redis stats"""
        try:
            info = self.redis.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "uptime_in_days": info.get("uptime_in_days", 0)
            }
        except Exception as e:
            logger.error(f"Error getting Redis info: {str(e)}")
            return {}

# Global Redis manager instance
redis_manager = RedisManager()