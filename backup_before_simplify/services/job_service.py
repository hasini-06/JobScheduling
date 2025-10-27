from repositories.job_repository import JobRepository
from schedulers.job_scheduler import JobScheduler

class JobService:
    """Service class that coordinates between repository and scheduler - Single Responsibility Principle"""
    
    def __init__(self, repository: JobRepository, scheduler: JobScheduler):
        self.repository = repository
        self.scheduler = scheduler
    
    def get_all_jobs(self):
        """Get all jobs"""
        return self.repository.get_all_jobs()
    
    def get_job_by_id(self, job_id: int):
        """Get job by ID"""
        return self.repository.get_job_by_id(job_id)
    
    def create_job(self, job_data: dict):
        """Create a new job"""
        return self.repository.create_job(job_data)
    
    def delete_job(self, job_id: int):
        """Delete a job"""
        return self.repository.delete_job(job_id)
    
    def schedule_job(self, job):
        """Schedule a job"""
        self.scheduler.schedule_job(job)
    
    def remove_scheduled_job(self, job_id: int):
        """Remove a job from scheduler"""
        self.scheduler.remove_job(job_id)
    
    def get_scheduled_jobs(self):
        """Get list of scheduled jobs"""
        return self.scheduler.get_scheduled_jobs()
    
    def clear_missed_jobs(self):
        """Clear any missed job executions"""
        self.scheduler.clear_missed_jobs()
