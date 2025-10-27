#  Job Scheduler API

A production-ready job scheduling service built with FastAPI, Redis, and PostgreSQL, following SOLID principles and clean architecture.

## Features

- **Job Scheduling**: Create, manage, and execute scheduled jobs
- **Redis Caching**: High-performance caching for improved response times
- **PostgreSQL**: Robust database for production use
- **Docker Support**: Containerized deployment with Docker Compose
- **Health Monitoring**: Built-in health checks and metrics
- **Security**: CORS, trusted hosts, and security headers
- **Scalability**: Multi-worker support with Gunicorn
- **SOLID Principles**: Clean, maintainable, and extensible code

## 🏗 Project Structure

```
Digantara_project/
├── app/                    # FastAPI application layer
├── services/              # Business logic layer
├── repositories/          # Data access layer
├── schedulers/            # Job scheduling layer
├── config/               # Configuration management
├── utils/                # Utility functions
├── tests/                # Test files
├── docs/                 # Documentation
└── app.py                # Main application entry point
```

## Quick Start

### Development Mode

1. **Install dependencies:**
   ```bash
   pip install -r requirements-simple.txt
   ```

2. **Run the application:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Production Mode

1. **Using Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **Access the API:**
   - API: http://localhost
   - Health Check: http://localhost/health

## -- API Endpoints

### Job Management
- `GET /jobs` - List all jobs
- `GET /job/{id}` - Get job by ID
- `POST /job` - Create new job
- `DELETE /job/{id}` - Delete job

### Monitoring
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Basic metrics

## 🛠 Configuration

Copy the environment template and configure:
```bash
cp config/env.example .env
```

Key environment variables:
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `REDIS_HOST` - Redis host
- `REDIS_PORT` - Redis port
- `ENVIRONMENT` - Environment (development/production)

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/jobs
```

## 📖 Documentation

- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Production Deployment](docs/README_PRODUCTION.md)

## 🏛 Architecture

This project follows **Clean Architecture** and **SOLID Principles**:

- **Single Responsibility**: Each class has one responsibility
- **Open/Closed**: Extensible without modification
- **Liskov Substitution**: Proper inheritance usage
- **Interface Segregation**: Focused interfaces
- **Dependency Inversion**: Depend on abstractions

## 🔧 Development

### Adding New Features

1. **API Endpoints**: Add to `app/api_endpoints.py`
2. **Business Logic**: Add to `services/`
3. **Data Operations**: Add to `repositories/`
4. **Scheduling**: Add to `schedulers/`
5. **Configuration**: Add to `config/`

### Code Quality

- **Linting**: `flake8`
- **Formatting**: `black`
- **Import Sorting**: `isort`

## 🚀 Deployment

### Docker
```bash
docker-compose up -d
```

### Manual
```bash
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📊 Monitoring

- **Health Check**: `/health`
- **Metrics**: `/metrics`
- **Logs**: Structured logging with configurable levels

## 🤝 Contributing

1. Follow SOLID principles
2. Write tests for new features
3. Update documentation
4. Use proper commit messages

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using FastAPI, Redis, and PostgreSQL**
