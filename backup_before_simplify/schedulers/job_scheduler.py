from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import re
import logging

logger = logging.getLogger(__name__)

class JobScheduler:
    """Scheduler class - Single Responsibility Principle"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler(
            timezone='Asia/Kolkata',  # Set your timezone
            job_defaults={
                'coalesce': True,  # Combine missed jobs into one
                'max_instances': 1,  # Only one instance of each job
                'misfire_grace_time': 60  # Grace period for missed jobs
            }
        )
        self.scheduler.start()
    
    def parse_interval(self, interval: str) -> timedelta:
        """Parse interval string to timedelta"""
        interval = interval.lower()
        if match := re.match(r"^\s*(\d+)\s*(?:m|min|mins|minutes)\s*$", interval):
            return timedelta(minutes=int(match.group(1)))
        elif match := re.match(r"^(\d+)\s*(?:h|hr|hrs|hour|hours)$", interval):
            return timedelta(hours=int(match.group(1)))
        elif interval == "daily":
            return timedelta(days=1)
        elif interval == "weekly":
            return timedelta(weeks=1) 
        else:
            raise ValueError(f"Invalid interval: {interval}")
    
    def schedule_job(self, job):
        """Schedule a job"""
        try:
            delta = self.parse_interval(job.interval)
        except ValueError as e:
            logger.warning(f"Invalid interval for job '{getattr(job, 'name', 'unknown')}': {e}")
            return

        # Ensure next_run is a datetime when the job comes from cache (it may be an ISO string)
        next_run = getattr(job, 'next_run', None)
        try:
            if isinstance(next_run, str):
                # parse ISO formatted datetime string
                next_run = datetime.fromisoformat(next_run)
        except Exception:
            # fallback to None and schedule immediately
            next_run = None

        start_time = next_run if (isinstance(next_run, datetime) and next_run > datetime.now()) else datetime.now() + timedelta(seconds=1)

        try:
            self.scheduler.add_job(
                func=self._execute_job,
                trigger=IntervalTrigger(seconds=int(delta.total_seconds())),
                args=[job.id],
                id=str(job.id),
                replace_existing=True,
                next_run_time=start_time,
                misfire_grace_time=60,  # Increased grace time
                coalesce=True,  # Combine missed executions
                max_instances=1  # Prevent multiple instances
            )
            logger.info(f"'{getattr(job, 'name', str(job.id))}' scheduled every {getattr(job, 'interval', 'unknown')}, first run at {start_time}")
        except Exception as e:
            # Catch scheduling exceptions so one bad job doesn't stop others
            logger.error(f"Failed to schedule job {getattr(job, 'id', 'unknown')}: {e}")
    
    def remove_job(self, job_id: int):
        """Remove a job from scheduler"""
        try:
            self.scheduler.remove_job(str(job_id))
            logger.info(f"Job {job_id} removed from scheduler")
        except Exception as e:
            logger.error(f"Failed to remove job {job_id}: {e}")
    
    def get_scheduled_jobs(self):
        """Get list of scheduled jobs"""
        return self.scheduler.get_jobs()
    
    def clear_missed_jobs(self):
        """Clear any missed job executions"""
        jobs = self.get_scheduled_jobs()
        for job in jobs:
            if hasattr(job, 'next_run_time') and job.next_run_time < datetime.now():
                # Reschedule missed jobs
                job.next_run_time = datetime.now() + timedelta(seconds=1)
    
    def _execute_job(self, job_id: int):
        """Execute a job"""
        from config.db_configuration import SessionLocal
        from app.models import Job
        
        try:
            with SessionLocal() as db:
                job = db.query(Job).filter(Job.id == job_id).first()
                if not job:
                    logger.warning(f"Job {job_id} not found.")
                    return
                job.last_run = datetime.now()
                db.commit()
                logger.info(f"Reminder: '{job.name}' ran at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            logger.exception(f"Error executing job {job_id}")
