from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    debug: bool = True
    log_level: str = "INFO"
    cors_origins: List[str] = ["*"]
    allowed_hosts: List[str] = ["*"]
    redis_url: str = "redis://localhost:6379/0"
    redis_password: str = "defaultpassword"  # Change this in production
    redis_db: int = 0

settings = Settings()