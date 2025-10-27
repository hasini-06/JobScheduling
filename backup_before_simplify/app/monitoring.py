from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db_configuration import SessionLocal
from config.redis_config import redis_manager
from config.config import settings
import time
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": settings.environment,
        "checks": {}
    }
    
    # Database health check
    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Redis health check
    try:
        if redis_manager.health_check():
            health_status["checks"]["redis"] = "healthy"
        else:
            health_status["checks"]["redis"] = "unhealthy"
            health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    return health_status

@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    return {
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/metrics")
async def metrics():
    """Basic metrics endpoint"""
    if not settings.enable_metrics:
        return {"error": "Metrics disabled"}
    
    return {
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time(),
        "environment": settings.environment,
        "version": "1.0.0"
    }
