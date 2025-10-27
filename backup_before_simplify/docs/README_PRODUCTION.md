# Job Scheduler API - Production Deployment

A production-ready job scheduling service built with FastAPI, Redis, and PostgreSQL.

## Features

- **Job Scheduling**: Create, manage, and execute scheduled jobs
- **Redis Caching**: High-performance caching for improved response times
- **PostgreSQL**: Robust database for production use
- **Docker Support**: Containerized deployment with Docker Compose
- **Health Monitoring**: Built-in health checks and metrics
- **Security**: CORS, trusted hosts, and security headers
- **Scalability**: Multi-worker support with Gunicorn

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Digantara_project
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your production values
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Check health**
   ```bash
   curl http://localhost/health
   ```

### Manual Deployment

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL and Redis**
   - Install PostgreSQL 15+
   - Install Redis 7+
   - Create database and user

3. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

4. **Run the application**
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8000
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_DB` | Database name | `jobscheduler` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_PASSWORD` | Redis password | - |
| `ENVIRONMENT` | Environment | `development` |
| `DEBUG` | Debug mode | `False` |
| `SECRET_KEY` | Secret key | - |
| `LOG_LEVEL` | Log level | `INFO` |

## API Endpoints

### Job Management
- `GET /jobs` - List all jobs
- `GET /job/{id}` - Get job by ID
- `POST /job` - Create new job
- `DELETE /job/{id}` - Delete job

### Monitoring
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Basic metrics

### Documentation
- `GET /docs` - Swagger UI (development only)
- `GET /redoc` - ReDoc (development only)

## Production Considerations

### Security
- Change default passwords
- Use strong secret keys
- Configure CORS origins
- Set up SSL/TLS certificates
- Use environment variables for secrets

### Performance
- Configure Redis for persistence
- Set up database connection pooling
- Use multiple workers
- Enable Redis clustering for high availability

### Monitoring
- Set up log aggregation
- Configure metrics collection
- Set up alerting
- Monitor resource usage

### Backup
- Regular database backups
- Redis persistence configuration
- Application state backup

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx)
- Multiple application instances
- Redis cluster
- Database read replicas

### Vertical Scaling
- Increase worker processes
- Optimize database queries
- Increase Redis memory
- Add more CPU/RAM

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check PostgreSQL is running
   - Verify connection credentials
   - Check network connectivity

2. **Redis Connection Issues**
   - Check Redis is running
   - Verify Redis password
   - Check Redis memory usage

3. **Job Execution Issues**
   - Check scheduler status
   - Verify job configurations
   - Check application logs

### Logs
- Application logs: `/app/logs/`
- Docker logs: `docker-compose logs`
- System logs: Check system journal

## Support

For issues and questions:
- Check application logs
- Verify environment configuration
- Test individual components
- Review documentation
