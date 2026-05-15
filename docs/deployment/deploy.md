"""
Deployment Guide
UrbanPulse Deployment Instructions
"""

# Deployment Guide

## Prerequisites

- Python 3.13+
- Node.js 22+
- Docker (optional)
- PostgreSQL or SQLite

## Development Setup

### Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run development server
python wsgi.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Production Deployment

### Using Gunicorn (Production WSGI Server)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### Using Docker

```bash
# Build Docker image
docker build -f docker/Dockerfile.backend -t urbanpulse-backend:latest .

# Run Docker container
docker run -p 5000:5000 urbanpulse-backend:latest
```

### Using Docker Compose

```bash
# Build and run all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f
```

## Environment Configuration

### Development (.env)
```
FLASK_ENV=development
FLASK_DEBUG=True
CACHE_ENABLED=True
```

### Production (.env)
```
FLASK_ENV=production
FLASK_DEBUG=False
CACHE_ENABLED=True
LOG_LEVEL=WARNING
```

## Database Migration (When Applicable)

```bash
# Create database tables
python manage.py db upgrade

# Create migration
python manage.py db migrate -m "Migration description"

# Apply migration
python manage.py db upgrade
```

## Frontend Build

```bash
cd frontend

# Build for production
npm run build

# Output directory
dist/
```

## Deployment Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Disable debug mode
- [ ] Set strong secret keys
- [ ] Configure CORS for production domain
- [ ] Setup logging to external service
- [ ] Configure monitoring/alerting
- [ ] Run security audit
- [ ] Setup database backups
- [ ] Configure SSL/TLS certificates
- [ ] Setup CI/CD pipeline

## Health Check

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2026-05-13T21:36:00",
  "version": "2.0.0"
}
```

## Monitoring

### Application Metrics
- CPU usage
- Memory usage
- Response time
- Error rate
- Request throughput

### Logging
- Application logs (Django/Flask)
- Access logs
- Error logs
- Performance logs

### Alerting
- High error rate
- High response time
- Low uptime
- High resource usage

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Run multiple Flask instances
- Share data via database

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Cache frequently accessed data

## Backup & Recovery

### Daily Backups
```bash
# Backup database
pg_dump -h localhost -U user dbname > backup.sql

# Backup data directory
tar -czf data_backup.tar.gz data/
```

### Restore from Backup
```bash
# Restore database
psql -h localhost -U user dbname < backup.sql

# Restore data directory
tar -xzf data_backup.tar.gz
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Permission Errors
```bash
# Fix file permissions
chmod 755 backend/
chmod 644 backend/*.py

# Fix directory permissions
chown -R appuser:appuser ./
```

### Database Connection Issues
- Check database is running
- Verify connection string in .env
- Check network connectivity
- Verify credentials

## Support

For issues or questions:
1. Check logs
2. Review deployment guide
3. Check GitHub issues
4. Contact maintainers
