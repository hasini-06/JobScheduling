"""
Job scheduler using APScheduler
Handles scheduling and executing jobs at specified intervals
"""
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import re
from models import SessionLocal, Job

class SimpleScheduler:
    def __init__(self):
        """Initialize the scheduler with some sane defaults"""
        self.scheduler = BackgroundScheduler(
            timezone='Asia/Kolkata',
            job_defaults={
                'coalesce': True,      # Combine missed jobs
                'max_instances': 1      # Only one instance at a time
            }
        )
        self.scheduler.start()
        print("✅ Scheduler started")
    
    def _parse_interval(self, interval: str) -> timedelta:
        """
        Convert interval string to timedelta
        Examples: "5 minutes", "1 hour", "daily"
        """
        interval = interval.lower().strip()
        
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
    
    def schedule_job(self, job_id: int, name: str, interval: str):
        """
        Schedule a job to run at specified intervals
        
        Args:
            job_id: Database ID of the job
            name: Display name of the job
            interval: How often to run (e.g., "5 minutes")
        """
        try:
            # Convert interval string to timedelta
            delta = self._parse_interval(interval)
            
            # Schedule the job
            self.scheduler.add_job(
                func=self._run_job,              # Function to run
                trigger=IntervalTrigger(         # Run at regular intervals
                    seconds=int(delta.total_seconds())
                ),
                args=[job_id],                   # Args for _run_job
                id=str(job_id),                  # Unique ID
                replace_existing=True,           # Replace if exists
                next_run_time=datetime.now() + timedelta(seconds=5)  # Start in 5 seconds
            )
            print(f"✅ Scheduled: {name} (every {interval})")
            
        except Exception as e:
            print(f"⚠️ Could not schedule job: {e}")
    
    def _run_job(self, job_id: int):
        """
        Execute a scheduled job
        Updates last_run time in database
        """
        try:
            # Get database session
            with SessionLocal() as db:
                # Find the job
                job = db.query(Job).filter(Job.id == job_id).first()
                if not job:
                    print(f"⚠️ Job {job_id} not found")
                    return
                    
                # Update last run time
                job.last_run = datetime.now()
                db.commit()
                
                print(f"✅ Ran job: {job.name}")
                
        except Exception as e:
            print(f"⚠️ Error running job {job_id}: {e}")
    
    def remove_job(self, job_id: int):
        """Stop a scheduled job"""
        try:
            self.scheduler.remove_job(str(job_id))
            print(f"✅ Removed job {job_id}")
        except Exception as e:
            print(f"⚠️ Could not remove job: {e}")
    
    def shutdown(self):
        """Shut down the scheduler gracefully"""
        self.scheduler.shutdown()