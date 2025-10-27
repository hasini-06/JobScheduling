from sqlalchemy.orm import Session
from app.models import Job
from config.redis_config import redis_manager
import json

class JobRepository:
    """Repository class for job data operations with Redis caching - Single Responsibility Principle"""
    
    def __init__(self, db: Session):
        self.db = db
        self.redis = redis_manager
    
    def get_all_jobs(self):
        """Get all jobs with caching"""
        cache_key = "all_jobs"
        cached_data = self.redis.get_cache(cache_key)
        
        if cached_data:
            try:
                jobs_data = json.loads(cached_data)
                return [Job(**job_data) for job_data in jobs_data]
            except (json.JSONDecodeError, TypeError):
                pass
        
        jobs = self.db.query(Job).all()
        # Cache the results
        jobs_data = [self._job_to_dict(job) for job in jobs]
        self.redis.set_cache(cache_key, jobs_data, 300)  # 5 minutes cache
        
        return jobs
    
    def get_job_by_id(self, job_id: int):
        """Get job by ID with caching"""
        # Check cache first
        cached_job = self.redis.get_job_cache(job_id)
        if cached_job:
            return Job(**cached_job)
        
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if job:
            # Cache the job
            self.redis.set_job_cache(job_id, self._job_to_dict(job))
        
        return job
    
    def create_job(self, job_data: dict):
        """Create a new job"""
        db_job = Job(**job_data)
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        
        # Cache the new job
        self.redis.set_job_cache(db_job.id, self._job_to_dict(db_job))
        
        # Invalidate all jobs cache
        self.redis.delete_cache("all_jobs")
        
        return db_job
    
    def delete_job(self, job_id: int):
        """Delete a job"""
        job = self.get_job_by_id(job_id)
        if job:
            self.db.delete(job)
            self.db.commit()
            
            # Remove from cache
            self.redis.delete_cache(f"job:{job_id}")
            self.redis.delete_cache("all_jobs")
            
            return job
        return None
    
    def update_job(self, job_id: int, job_data: dict):
        """Update a job"""
        job = self.get_job_by_id(job_id)
        if job:
            for key, value in job_data.items():
                setattr(job, key, value)
            self.db.commit()
            self.db.refresh(job)
            
            # Update cache
            self.redis.set_job_cache(job_id, self._job_to_dict(job))
            self.redis.delete_cache("all_jobs")
            
            return job
        return None
    
    def _job_to_dict(self, job: Job) -> dict:
        """Convert Job object to dictionary for caching"""
        return {
            "id": job.id,
            "name": job.name,
            "description": job.description,
            "interval": job.interval,
            "last_run": job.last_run.isoformat() if job.last_run else None,
            "next_run": job.next_run.isoformat() if job.next_run else None,
            "status": job.status
        }
