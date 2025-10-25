from fastapi import FastAPI
from db_configuration import Base, engine, SessionLocal
from models import Job
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import re

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
scheduler = BackgroundScheduler()

scheduler.start()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_interval(interval: str) -> timedelta:
    interval = interval.lower()
    if match := re.match(r"^\s*(\d+)\s*(?:m|min|mins|minutes)\s*$", interval):
        return timedelta(minutes=int(match.group(1)))
    elif match := re.match(r"^(\d+)\s*(?:h|hr|hrs|hour|hours)$", interval):
        return timedelta(hours=int(match.group(1)))
    # elif match := re.match(r"(\d+)\s*s", interval):
    #     return timedelta(seconds=int(match.group(1)))
    elif interval == "daily":
        return timedelta(days=1)
    elif interval == "weekly":
        return timedelta(weeks=1) 
    else:
        raise ValueError(f"Invalid interval: {interval}")

# Job execution
def execute_job(job_id: int):
     
     with SessionLocal() as db:
         job = db.query(Job).filter(Job.id == job_id).first()
         if not job: 
            print(f" Job {job_id} not found.") 
            return 
         job.last_run = datetime.now() 
         db.commit() 
         print(f" Reminder: '{job.name}' ran at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Schedule job using interval trigger 
def schedule_job(db_job: Job):
    try:
        delta = parse_interval(db_job.interval)
    except ValueError as e:
        print(f" Invalid interval for job '{db_job.name}': {e}")
        return

    start_time = db_job.next_run if db_job.next_run > datetime.now() else datetime.now() + timedelta(seconds=1)

    scheduler.add_job(
        func=execute_job,
        trigger=IntervalTrigger(seconds=int(delta.total_seconds())),
        args=[db_job.id],
        id=str(db_job.id),
        replace_existing=True,
        next_run_time=start_time,
        misfire_grace_time=30
    )
    print(f" '{db_job.name}' scheduled every {db_job.interval}, first run at {start_time}")

# Reload jobs on startup
@app.on_event("startup")
def load_jobs_on_startup():
    with SessionLocal() as db:
        jobs = db.query(Job).all()
        for job in jobs:
            schedule_job(job)

import api_endpoints
