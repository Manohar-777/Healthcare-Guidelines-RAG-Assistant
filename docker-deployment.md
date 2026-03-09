# 🐳 Docker Deployment Guide

## Quick Start

### 1. Prerequisites

- Docker Desktop installed (https://www.docker.com/products/docker-desktop)
- Docker Compose installed (included with Docker Desktop)
- Groq API key (https://console.groq.com/keys)

### 2. Setup Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Groq API key
# LLM_PROVIDER=groq
# GROQ_API_KEY=your_actual_key_here
```

### 3. Build and Run
#### Run API + UI 
```bash
# Build image
docker-compose build

# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**Access:**
- Streamlit UI: http://localhost:8501
- API Docs: http://localhost:9070/docs

### 4. Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Detailed Commands

### Build Images
```bash
# Build API image
docker build -t healthcare-rag-api .

# Build UI image
docker build -f Dockerfile.streamlit -t healthcare-rag-ui .

# Or build with docker-compose
docker-compose build
```

### Run Containers
```bash
# Run in foreground (see logs)
docker-compose up

# Run in background (detached)
docker-compose up -d

# Run specific service only
docker-compose up api
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f ui

# Last 100 lines
docker-compose logs --tail=100 api
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart api
```

### Rebuild After Code Changes
```bash
# Rebuild and restart
docker-compose up -d --build

# Force rebuild
docker-compose build --no-cache
docker-compose up -d
```

---

## Container Management

### Execute Commands in Container
```bash
# Access container shell
docker exec -it healthcare-rag-api bash

# Run evaluation inside container
docker exec healthcare-rag-api python evaluation/eval_comprehensive.py

# Rebuild index inside container
docker exec healthcare-rag-api python scripts/pipeline.py
```

### Copy Files To/From Container
```bash
# Copy file from container
docker cp healthcare-rag-api:/app/evaluation/reports/evaluation_results.json ./

# Copy file to container
docker cp new_queries.csv healthcare-rag-api:/app/evaluation/
```

---

## Troubleshooting

### Issue: Container Won't Start
```bash
# Check logs
docker-compose logs api

# Common causes:
# 1. Port already in use
# 2. Missing .env file
# 3. Invalid API key
```

**Solution:**
```bash
# Check port usage
netstat -ano | findstr :9070  # Windows
lsof -i :9070                 # macOS/Linux

# Verify .env file
cat .env

# Restart with fresh build
docker-compose down
docker-compose up --build
```

### Issue: API Key Not Working

**Symptom:**
```
ValueError: GROQ_API_KEY missing
```

**Solution:**
```bash
# 1. Check .env file exists
ls .env

# 2. Verify content (no quotes!)
cat .env
# Should be: GROQ_API_KEY=gsk_xxxxx

# 3. Rebuild with correct env
docker-compose down
docker-compose up --build
```

### Issue: Cannot Access API

**Symptom:** http://localhost:9070/docs not loading

**Solution:**
```bash
# 1. Check container is running
docker-compose ps

# 2. Check container logs
docker-compose logs api

# 3. Verify port mapping
docker ps

# 4. Test from inside container
docker exec healthcare-rag-api curl http://localhost:9070/
```

### Issue: Slow Build Times

**Solution:**
```bash
# Use build cache
docker-compose build

# Or use BuildKit (faster)
DOCKER_BUILDKIT=1 docker build -t healthcare-rag-api .
```

---


## Performance Optimization

### Multi-Stage Build (Reduce Image Size)
```dockerfile
# Dockerfile.optimized
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "9070"]
```

### Caching Strategies
```yaml
services:
  api:
    volumes:
      # Cache models to avoid re-downloading
      - model-cache:/root/.cache/huggingface
      # Cache pip packages
      - pip-cache:/root/.cache/pip

volumes:
  model-cache:
  pip-cache:
```

---

## Monitoring

### Health Checks
```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' healthcare-rag-api

# Auto health check with docker-compose
docker-compose ps
```

### Resource Usage
```bash
# Monitor resource usage
docker stats healthcare-rag-api

# Or all containers
docker stats
```

---

## Backup and Restore

### Backup Index
```bash
# Backup index from container
docker cp healthcare-rag-api:/app/index ./backup_index_$(date +%Y%m%d)
```

### Restore Index
```bash
# Restore index to container
docker cp ./backup_index_20260203 healthcare-rag-api:/app/index
docker-compose restart api
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start all services |
| `docker-compose down` | Stop all services |
| `docker-compose logs -f api` | View API logs |
| `docker-compose restart api` | Restart API |
| `docker-compose build --no-cache` | Rebuild from scratch |
| `docker exec -it healthcare-rag-api bash` | Access container shell |
| `docker-compose ps` | Check status |
| `docker stats` | Monitor resources |

---

## Support

For Docker-specific issues:
- Docker Documentation: https://docs.docker.com/
- Docker Compose Reference: https://docs.docker.com/compose/

For application issues:
- See `RUNBOOK.md`
- See `TROUBLESHOOTING.md`