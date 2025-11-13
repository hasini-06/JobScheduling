"""
Job scheduler using APScheduler
Handles scheduling and executing jobs at specified intervals
"""
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
import re
import logging
from src.models.models import SessionLocal, Job

logger = logging.getLogger(__name__)

class SimpleScheduler:
    def __init__(self):
        """Initialize the scheduler"""
        self.scheduler = BackgroundScheduler(
            timezone='Asia/Kolkata',  # Set default timezone
            job_defaults={
                'coalesce': True,  # Combine missed executions into a single one
                'max_instances': 1,  # Only one instance of each job can run at a time
                'misfire_grace_time': 60  # Allow jobs to be 60 seconds late
            }
        )
        self.scheduler.start()
        logger.info("Scheduler started successfully")
    
    def _parse_interval(self, interval: str) -> timedelta:
        """Convert interval string to timedelta"""
        interval = interval.lower().strip()
        try:
            # Match minute intervals (e.g., "5 minutes")
            if match := re.match(r"^(\d+)\s*(?:m|min|mins|minutes?)$", interval):
                return timedelta(minutes=int(match.group(1)))
                 
            # Match hour intervals (e.g., "2 hours")
            if match := re.match(r"^(\d+)\s*(?:h|hr|hrs|hours?)$", interval):
                return timedelta(hours=int(match.group(1)))
                
            # Handle daily/weekly
            if interval == "daily":
                return timedelta(days=1)
            if interval == "weekly":
                return timedelta(weeks=1)
                
            raise ValueError(f"Can't understand interval: {interval}")
        except Exception:
            # Default to 1 hour if interval format is invalid
            logger.warning(f"Invalid interval format: {interval}, defaulting to 1 hour")
            return timedelta(hours=1)
    
    def schedule_job(self, job_id: int, name: str, interval: str):
        """Schedule a reminder job"""
        try:
            delta = self._parse_interval(interval)
            seconds = int(delta.total_seconds())
            
            # For very frequent jobs (less than 1 minute), increase the interval
            if seconds < 60:
                logger.warning(f"Interval too short for {name}, setting to 1 minute minimum")
                seconds = 60
            
            job_exists = False
            try:
                job = self.scheduler.get_job(str(job_id))
                job_exists = bool(job)
            except:
                pass

            self.scheduler.add_job(
                func=self._run_job,
                trigger=IntervalTrigger(seconds=seconds),
                args=[job_id],
                id=str(job_id),
                replace_existing=True,
                misfire_grace_time=60  # Allow up to 60 seconds delay
            )
            
            # Log at debug level - jobs are loaded from DB on startup, not newly created
            if not job_exists:
                logger.debug(f"Scheduled job: {name} ({interval})")
            else:
                logger.debug(f"Rescheduled job: {name} ({interval})")
        except Exception as e:
            logger.error(f"Error scheduling job {name}: {e}")
    
    def _run_job(self, job_id: int):
        """Execute a scheduled job"""
        try:
            now = datetime.now()
            with SessionLocal() as db:
                job = db.query(Job).filter(Job.id == job_id).first()
                if job:
                    job.last_run = now
                    job.next_run = now + self._parse_interval(job.interval)
                    db.commit()
                    logger.info(f"Reminder: {job.name} at {now.strftime('%H:%M:%S')}")
                
        except Exception as e:
            logger.error(f"Job execution error: {str(e)}")
    
    def remove_job(self, job_id: int):
        """Stop a scheduled job"""
        try:
            self.scheduler.remove_job(str(job_id))
            logger.info(f"Removed job {job_id}")
        except Exception as e:
            logger.warning(f"Could not remove job {job_id}: {e}")
    
    def shutdown(self):
        """Shut down the scheduler gracefully"""
        self.scheduler.shutdown()