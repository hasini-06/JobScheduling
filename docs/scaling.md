# Scaling Guide

This document provides guidance on scaling the Job Scheduling application using Docker, Redis, and API scaling techniques.

## Docker Scaling

### Docker Compose Scaling
```bash
# Scale specific services
docker-compose up --scale app=3

# Scale with resource limits
docker-compose up --scale app=3 -d
```

### Docker Swarm
```bash
# Initialize Docker Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml jobscheduler

# Scale services
docker service scale jobscheduler_app=3

# Check service status
docker service ls
```

### Container Resource Limits
```yaml
# In docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Redis Scaling

### Redis Cluster Setup
```bash
# Start Redis cluster
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 --cluster-replicas 1

# Check cluster status
redis-cli -c -p 7000 cluster info
```

### Redis Configuration
```conf
# Redis configuration for high availability
maxmemory 2gb
maxmemory-policy allkeys-lru
appendonly yes
```

### Redis Sentinel
```bash
# Start Redis Sentinel
redis-server /path/to/sentinel.conf --sentinel

# Monitor Sentinel status
redis-cli -p 26379 info sentinel
```

## API Scaling

### Load Balancing
Using Nginx as a load balancer:

```nginx
# nginx.conf
upstream backend {
    server app1:8000;
    server app2:8000;
    server app3:8000;
    keepalive 32;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Application Configuration
```python
# uvicorn configuration for performance
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --loop uvloop --http httptools
```

### Database Connection Pooling
```python
# SQLAlchemy connection pooling
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)
```

## Monitoring and Health Checks

### Docker Health Checks
```yaml
# In docker-compose.yml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Prometheus Metrics
```python
# Add Prometheus metrics endpoints
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize metrics in FastAPI app
Instrumentator().instrument(app).expose(app)
```

## Best Practices

1. **Horizontal Scaling**
   - Use container orchestration (Docker Swarm/Kubernetes)
   - Implement stateless application design
   - Use distributed caching (Redis)

2. **Vertical Scaling**
   - Optimize application code
   - Configure proper resource limits
   - Use connection pooling

3. **Caching Strategy**
   - Implement Redis caching for frequently accessed data
   - Use appropriate cache invalidation strategies
   - Configure proper TTL for cached items

4. **High Availability**
   - Deploy across multiple availability zones
   - Use Redis Sentinel/Cluster for cache HA
   - Implement proper failover mechanisms

5. **Performance Monitoring**
   - Set up Prometheus/Grafana for metrics
   - Monitor application and infrastructure health
   - Implement proper logging and tracing