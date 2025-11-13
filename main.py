from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from src.models.models import Base, engine, SessionLocal, Job, get_db
from src.core.scheduler import SimpleScheduler as JobScheduler
from src.core.settings import settings
import time
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    # concise and readable format
    format='%(asctime)s %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)
# Reduce APScheduler verbosity (suppress INFO job-executed messages)
logging.getLogger('apscheduler').setLevel(logging.WARNING)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Scheduler API", 
    description="A production-ready job scheduling service",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)

# Initialize components
job_scheduler = JobScheduler()

# Make scheduler available to other modules
def get_scheduler():
    return job_scheduler

# Add API routes
from src.api.api import router as api_router, set_scheduler
set_scheduler(job_scheduler)
app.include_router(api_router, prefix="/api/v1")

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Load jobs on startup
@app.on_event("startup")
async def load_jobs_on_startup():
    try:
        db = SessionLocal()
        jobs = db.query(Job).all()
        for job in jobs:
            job_scheduler.schedule_job(job.id, job.name, job.interval)
        logger.info(f"Loaded and scheduled {len(jobs)} jobs from database")
        db.close()
    except Exception as e:
        logger.error(f"Startup error loading jobs: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    job_scheduler.shutdown()
