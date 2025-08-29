# Deployment Guide

## Security Features Implemented

### 1. Environment-Based Configuration
- Development vs Production environment detection
- CORS restrictions based on environment
- Configurable allowed origins

### 2. Container Security
- Non-root user in Docker
- Minimal base image (python:3.11-slim)
- Health checks
- Proper file permissions

### 3. Production Best Practices
- Environment variable configuration
- CORS restrictions
- Rate limiting support
- Secure headers

## Deployment Options

### Option 1: Railway/Render/Heroku (Recommended)
These platforms will automatically detect and use the configuration files:
- `Procfile` - Specifies start command
- `nixpacks.toml` - Build configuration
- `runtime.txt` - Python version

### Option 2: Docker Deployment
```bash
# Build image
docker build -t ead-teachers-backend .

# Run container
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -e ENVIRONMENT=production \
  -e SECRET_KEY=your_secret \
  ead-teachers-backend
```

### Option 3: Manual Server Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY=your_key
export ENVIRONMENT=production
export SECRET_KEY=your_secret

# Run with gunicorn (production)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Environment Variables

### Required for Production
```bash
GOOGLE_API_KEY=your_actual_api_key
ENVIRONMENT=production
SECRET_KEY=strong_random_secret_key
ALLOWED_ORIGINS=https://yourdomain.com
```

### Optional
```bash
HOST=0.0.0.0
PORT=8000
RATE_LIMIT_PER_MINUTE=60
LOG_LEVEL=INFO
```

## Security Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Configure `ALLOWED_ORIGINS` with your domain
- [ ] Generate strong `SECRET_KEY`
- [ ] Use HTTPS in production
- [ ] Set up proper firewall rules
- [ ] Monitor logs for suspicious activity
- [ ] Regular security updates
- [ ] API key rotation

## Troubleshooting

### "No start command could be found"
- Ensure `Procfile` exists and is in root directory
- Check `nixpacks.toml` configuration
- Verify `requirements.txt` is present

### CORS errors
- Check `ALLOWED_ORIGINS` environment variable
- Ensure frontend domain is included
- Verify `ENVIRONMENT` is set correctly

### API key errors
- Verify `GOOGLE_API_KEY` is set correctly
- Check API key permissions and quotas
- Ensure key is valid and not expired 