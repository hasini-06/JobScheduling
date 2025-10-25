from fastapi import Depends, HTTPException
from schema import JobSchema
from sqlalchemy.orm import Session
from models import Job
from datetime import datetime
from app import app,get_db,schedule_job,scheduler

# Get all jobs
@app.get("/jobs", response_model=list[JobSchema])
def get_all_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

# Get job by ID
@app.get("/job/{id}", response_model=JobSchema)
def get_job_by_id(id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# Add new job
@app.post("/job", response_model=JobSchema)
def add_job(job: JobSchema, db: Session = Depends(get_db)):
    db_job = Job(
        name=job.name,
        description=job.description,
        interval=job.interval,
        last_run=datetime.now(),
        next_run=job.next_run,
        status=job.status
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    schedule_job(db_job)
    return db_job

# Delete a job
@app.delete("/job/{id}")
def delete_job(id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    try:
        scheduler.remove_job(str(id))
        print(f" Job '{job.name}' deleted from scheduler and database")
    except Exception as e:
        print(f" Job '{job.name}' deleted from DB, but scheduler removal failed: {e}")
    
    return {"detail": f" Job '{job.name}' deleted successfully"}

