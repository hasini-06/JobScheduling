"""
Simple Redis helper for caching job data.
This module provides basic Redis operations with error handling.
"""
import redis
import json
from typing import Optional, Dict, Any

class RedisHelper:
    def __init__(self, host='localhost', port=6379, password=None):
        """Initialize Redis connection with simple error handling"""
        try:
            self.redis = redis.Redis(
                host=host,
                port=port,
                password=password,
                decode_responses=True  # Automatically decode responses to strings
            )
            # Test connection
            self.redis.ping()
            print("✅ Connected to Redis successfully")
        except Exception as e:
            print(f"⚠️ Redis connection failed: {e}")
            self.redis = None
    
    def save_job(self, job_id: int, job_data: Dict[str, Any], expire_seconds: int = 3600) -> bool:
        """
        Save job data to Redis cache
        Args:
            job_id: The ID of the job
            job_data: Dictionary containing job information
            expire_seconds: How long to keep in cache (default 1 hour)
        """
        if not self.redis:
            return False
            
        try:
            # Convert job data to JSON string
            key = f"job:{job_id}"
            self.redis.setex(key, expire_seconds, json.dumps(job_data))
            return True
        except Exception as e:
            print(f"⚠️ Could not save job to Redis: {e}")
            return False
    
    def get_job(self, job_id: int) -> Optional[Dict[str, Any]]:
        """
        Get job data from Redis cache
        Args:
            job_id: The ID of the job to retrieve
        Returns:
            Dictionary with job data if found, None if not found
        """
        if not self.redis:
            return None
            
        try:
            key = f"job:{job_id}"
            data = self.redis.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"⚠️ Could not get job from Redis: {e}")
            return None
    
    def delete_job(self, job_id: int) -> bool:
        """
        Delete job data from Redis cache
        Args:
            job_id: The ID of the job to delete
        """
        if not self.redis:
            return False
            
        try:
            key = f"job:{job_id}"
            return bool(self.redis.delete(key))
        except Exception as e:
            print(f"⚠️ Could not delete job from Redis: {e}")
            return False
    
    def save_all_jobs(self, jobs_data: Dict[int, Dict], expire_seconds: int = 3600) -> bool:
        """
        Save multiple jobs to Redis in one go
        Args:
            jobs_data: Dictionary mapping job IDs to job data
            expire_seconds: How long to keep in cache (default 1 hour)
        """
        if not self.redis:
            return False
            
        try:
            # Use pipeline for better performance with multiple operations
            with self.redis.pipeline() as pipe:
                for job_id, job_data in jobs_data.items():
                    key = f"job:{job_id}"
                    pipe.setex(key, expire_seconds, json.dumps(job_data))
                pipe.execute()
            return True
        except Exception as e:
            print(f"⚠️ Could not save jobs to Redis: {e}")
            return False
            
    def is_connected(self) -> bool:
        """Check if Redis is connected and responding"""
        if not self.redis:
            return False
        try:
            return bool(self.redis.ping())
        except:
            return False