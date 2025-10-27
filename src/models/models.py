"""
Database models for the job scheduler
Uses SQLAlchemy for database operations
"""
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create database engine - using SQLite for simplicity
DATABASE_URL = "sqlite:///./jobs.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(bind=engine)

# Create base class for models
Base = declarative_base()

class Job(Base):
    """
    Represents a scheduled job in the database
    
    Fields:
        id: Unique identifier for the job
        name: Display name of the job
        description: What the job does
        interval: How often to run (e.g., "5 minutes", "1 hour", "daily")
        last_run: When the job was last executed
        next_run: When the job should run next
        status: Current job status
    """
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    interval = Column(String(50), nullable=False)  # e.g., "5 minutes", "1 hour", "daily"
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=False)
    status = Column(String(50), default="active")  # active, paused, completed
    
    def to_dict(self):
        """Convert job to dictionary for caching/API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "interval": self.interval,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "status": self.status
        }
    
    def __repr__(self):
        return f"<Job(id={self.id}, name='{self.name}', status='{self.status}')>"

# Create all tables
Base.metadata.create_all(engine)

# Helper function to get database session
def get_db():
    """Get a new database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()