from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.models import Job, get_db
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel
from src.cache.redis_manager import redis_manager
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


@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}


@router.get("/redis/stats")
def get_redis_stats():
    """Get Redis server statistics"""
    return redis_manager.get_queue_info()