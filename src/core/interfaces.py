"""
Abstract base classes (interfaces) for our components
Following Interface Segregation Principle
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

class CacheInterface(ABC):
    """Interface for caching operations"""
    @abstractmethod
    def save(self, key: str, data: Any, expire_seconds: int) -> bool:
        """Save data to cache"""
        pass
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get data from cache"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete data from cache"""
        pass

class JobRepositoryInterface(ABC):
    """Interface for job storage operations"""
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all jobs"""
        pass
    
    @abstractmethod
    def get_by_id(self, job_id: int) -> Optional[Dict[str, Any]]:
        """Get job by ID"""
        pass
    
    @abstractmethod
    def create(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job"""
        pass
    
    @abstractmethod
    def update(self, job_id: int, job_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a job"""
        pass
    
    @abstractmethod
    def delete(self, job_id: int) -> bool:
        """Delete a job"""
        pass

class JobSchedulerInterface(ABC):
    """Interface for job scheduling operations"""
    @abstractmethod
    def schedule(self, job_id: int, name: str, interval: str) -> bool:
        """Schedule a job"""
        pass
    
    @abstractmethod
    def remove(self, job_id: int) -> bool:
        """Remove a scheduled job"""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown scheduler"""
        pass