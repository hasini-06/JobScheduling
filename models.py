from sqlalchemy import Column, Integer, String, DateTime
from db_configuration import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    interval = Column(String(50), nullable=False)
    last_run = Column(DateTime, nullable=True, default=None)
    next_run = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Job(id={self.id}, name='{self.name}', status='{self.status}')>"
