# Project Structure

This document describes the organized folder structure of the Job Scheduler API project.

## 📁 Folder Structure

```
Digantara_project/
├── app/                          # FastAPI application layer
│   ├── __init__.py
│   ├── api_endpoints.py         # API route handlers
│   ├── models.py                # SQLAlchemy models
│   ├── schema.py                # Pydantic schemas
│   └── monitoring.py            # Health checks and metrics
│
├── services/                     # Business logic layer
│   ├── __init__.py
│   └── job_service.py           # Job service orchestration
│
├── repositories/                 # Data access layer
│   ├── __init__.py
│   └── job_repository.py        # Job data operations
│
├── schedulers/                  # Job scheduling layer
│   ├── __init__.py
│   └── job_scheduler.py         # APScheduler integration
│
├── config/                      # Configuration management
│   ├── __init__.py
│   ├── config.py               # Application settings
│   ├── db_configuration.py     # Database configuration
│   ├── redis_config.py         # Redis configuration
│   └── env.example             # Environment variables template
│
├── utils/                       # Utility functions
│   ├── __init__.py
│   └── start.sh                # Production startup script
│
├── tests/                       # Test files
│   └── __init__.py
│
├── docs/                        # Documentation
│   ├── PROJECT_STRUCTURE.md    # This file
│   └── README_PRODUCTION.md    # Production deployment guide
│
├── app.py                       # Main application entry point
├── requirements.txt             # Production dependencies
├── requirements-simple.txt      # Simplified dependencies
├── requirements-dev.txt         # Development dependencies
├── Dockerfile                   # Container configuration
├── docker-compose.yml           # Multi-container setup
├── nginx.conf                   # Reverse proxy configuration
├── .dockerignore               # Docker ignore file
└── job.db                      # SQLite database (development)
```

## 🏗 Architecture Layers

### 1. **Application Layer** (`app/`)
- **Purpose**: FastAPI routes, models, and schemas
- **Responsibilities**: HTTP request/response handling, data validation
- **Files**: `api_endpoints.py`, `models.py`, `schema.py`, `monitoring.py`

### 2. **Service Layer** (`services/`)
- **Purpose**: Business logic orchestration
- **Responsibilities**: Coordinate between repositories and schedulers
- **Files**: `job_service.py`

### 3. **Repository Layer** (`repositories/`)
- **Purpose**: Data access and persistence
- **Responsibilities**: Database operations, caching
- **Files**: `job_repository.py`

### 4. **Scheduler Layer** (`schedulers/`)
- **Purpose**: Job scheduling and execution
- **Responsibilities**: APScheduler integration, job execution
- **Files**: `job_scheduler.py`

### 5. **Configuration Layer** (`config/`)
- **Purpose**: Application configuration management
- **Responsibilities**: Settings, database config, Redis config
- **Files**: `config.py`, `db_configuration.py`, `redis_config.py`

### 6. **Utilities Layer** (`utils/`)
- **Purpose**: Helper functions and scripts
- **Responsibilities**: Production scripts, utilities
- **Files**: `start.sh`

## 🔄 Data Flow

```
HTTP Request → API Endpoints → Service Layer → Repository/Scheduler → Database/Redis
     ↓              ↓              ↓              ↓
Response ← API Endpoints ← Service Layer ← Repository/Scheduler ← Database/Redis
```

## 📦 Package Dependencies

- **app** → **services**, **repositories**, **schedulers**
- **services** → **repositories**, **schedulers**
- **repositories** → **config** (Redis, DB)
- **schedulers** → **config** (DB)
- **config** → Environment variables

## 🎯 Benefits of This Structure

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Maintainability**: Easy to locate and modify specific functionality
3. **Testability**: Each layer can be tested independently
4. **Scalability**: Easy to add new features or modify existing ones
5. **SOLID Principles**: Follows Single Responsibility and Dependency Inversion
6. **Professional Structure**: Industry-standard organization

## 🚀 Running the Application

```bash
# Development
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Production
docker-compose up -d

# Testing
pytest tests/
```

## 📝 Adding New Features

1. **New API endpoints**: Add to `app/api_endpoints.py`
2. **New business logic**: Add to `services/`
3. **New data operations**: Add to `repositories/`
4. **New scheduling logic**: Add to `schedulers/`
5. **New configuration**: Add to `config/`
