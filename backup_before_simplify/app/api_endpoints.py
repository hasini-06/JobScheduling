from fastapi import Depends, HTTPException
from app.schema import JobSchema
from sqlalchemy.orm import Session
from datetime import datetime
from main import app, get_db, job_service

# Get all jobs
@app.get("/jobs", response_model=list[JobSchema])
def get_all_jobs():
    return job_service.get_all_jobs()

# Get job by ID
@app.get("/job/{id}", response_model=JobSchema)
def get_job_by_id(id: int):
    job = job_service.get_job_by_id(id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# Add new job
@app.post("/job", response_model=JobSchema)
def add_job(job: JobSchema):
    job_data = {
        "name": job.name,
        "description": job.description,
        "interval": job.interval,
        "last_run": datetime.now(),
        "next_run": job.next_run,
        "status": job.status
    }
    db_job = job_service.create_job(job_data)
    job_service.schedule_job(db_job)
    return db_job

# Delete a job
@app.delete("/job/{id}")
def delete_job(id: int):
    job = job_service.get_job_by_id(id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_service.delete_job(id)
    job_service.remove_scheduled_job(id)
    return {"detail": f"Job '{job.name}' deleted successfully"}

