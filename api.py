from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Job, get_db
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel
from redis_manager import redis_manager
from enum import Enum

class JobStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class JobCreate(BaseModel):
    name: str
    description: Optional[str] = None
    interval: str
    status: JobStatus = JobStatus.PENDING  # Default to pending

class JobUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    interval: Optional[str] = None
    status: Optional[JobStatus] = None

class JobResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    interval: str
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    status: JobStatus

    class Config:
        from_attributes = True

router = APIRouter()

@router.get("/jobs", response_model=List[JobResponse])
def get_jobs(status: Optional[JobStatus] = None, db: Session = Depends(get_db)):
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    return query.all()

@router.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = Job(
        name=job.name,
        description=job.description,
        interval=job.interval,
        next_run=datetime.now(),
        status=job.status
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# @router.patch("/jobs/{job_id}", response_model=JobResponse)
# def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
#     db_job = db.query(Job).filter(Job.id == job_id).first()
#     if db_job is None:
#         raise HTTPException(status_code=404, detail="Job not found")
    
#     # Update only provided fields
#     update_data = job_update.dict(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(db_job, field, value)
    
#     db.commit()
#     db.refresh(db_job)
#     return db_job

# @router.put("/jobs/{job_id}/status", response_model=JobResponse)
# def update_job_status(job_id: int, status: JobStatus, db: Session = Depends(get_db)):
#     db_job = db.query(Job).filter(Job.id == job_id).first()
#     if db_job is None:
#         raise HTTPException(status_code=404, detail="Job not found")
    
#     db_job.status = status
#     if status == JobStatus.ACTIVE:
#         db_job.next_run = datetime.now()  # Reset next run time when activating
    
#     db.commit()
#     db.refresh(db_job)
#     return db_job

@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}

@router.get("/jobs/{job_id}/status")
def get_job_status(job_id: int, db: Session = Depends(get_db)):
    """Get job status from both database and Redis cache"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    redis_status = redis_manager.get_job_status(job_id)
    return {
        "id": job_id,
        "db_status": job.status,
        "cache_status": redis_status
    }

@router.get("/redis/stats")
def get_redis_stats():
    """Get Redis server statistics"""
    return redis_manager.get_queue_info()