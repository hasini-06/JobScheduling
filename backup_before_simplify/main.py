from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from config.db_configuration import Base, engine, SessionLocal
from services.job_service import JobService
from repositories.job_repository import JobRepository
from schedulers.job_scheduler import JobScheduler
from app.monitoring import router as monitoring_router
from config.config import settings
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

# Add monitoring routes
app.include_router(monitoring_router)

# Initialize components
job_scheduler = JobScheduler()
job_repository = JobRepository(SessionLocal())
job_service = JobService(job_repository, job_scheduler)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Reload jobs on startup
@app.on_event("startup")
async def load_jobs_on_startup():
    try:
        jobs = job_service.get_all_jobs()
        
        # Clear any missed job executions
        job_service.clear_missed_jobs()
        
        for job in jobs:
            job_service.schedule_job(job)
        
        logger.info(f"Loaded {len(jobs)} jobs on startup")
    except Exception as e:
        # Log full traceback to help debugging
        logger.exception("Error loading jobs on startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")

from app import api_endpoints
