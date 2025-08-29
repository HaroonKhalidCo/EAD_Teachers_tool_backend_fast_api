# EAD Teachers Tool Backend

AI-powered educational tools for teachers including lesson planning, assessment generation, and educational assistance.

## Features

- **Lesson Plan Generator**: Create detailed lesson plans from syllabus uploads
- **Term Plan Generator**: Generate comprehensive term plans
- **Assessment Generator**: Create quizzes and tests with multiple question types
- **Student Assistant**: AI-powered tutoring and assistance for students
- **Teacher Assistant**: Professional guidance for teachers
- **Homework Generator**: Create engaging homework assignments

## Security Features

- **Environment-based Configuration**: Automatic security hardening in production
- **CORS Protection**: Configurable cross-origin resource sharing
- **Container Security**: Non-root user, minimal base image, health checks
- **Rate Limiting**: Built-in protection against abuse
- **Secure Headers**: Production-ready security middleware

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Run the setup script to create a `.env` file:

```bash
python setup_env.py
```

Or manually create a `.env` file in the root directory:

```env
# API Keys
GOOGLE_API_KEY=your_google_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# Security Configuration
SECRET_KEY=your_secret_key_here_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration (for production)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

### 3. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### 4. Run the Application

```bash
# Development
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Deployment

### Quick Deploy (Railway/Render/Heroku)
The project includes all necessary configuration files for automatic deployment:
- `Procfile` - Start command
- `nixpacks.toml` - Build configuration  
- `runtime.txt` - Python version
- `Dockerfile` - Container configuration

### Docker Deployment
```bash
# Build and run
docker build -t ead-teachers-backend .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key ead-teachers-backend
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## API Endpoints

- `POST /api/v1/lesson-plan/generate` - Generate lesson plan
- `POST /api/v1/term-plan/generate` - Generate term plan
- `POST /api/v1/assessment/generate` - Generate assessment
- `POST /api/v1/student-assistant/ask` - Get student assistance
- `POST /api/v1/teacher-assistant/ask` - Get teacher assistance
- `POST /api/v1/homework-generator/generate` - Generate homework

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

- **FastAPI**: Modern web framework for building APIs
- **Agno**: AI agent framework for intelligent responses
- **Google Gemini 2.5 Flash**: Advanced AI model for content generation
- **Pydantic**: Data validation and settings management
- **DuckDuckGo Tools**: Web search capabilities for agents

## Security Best Practices

- Set `ENVIRONMENT=production` in production deployments
- Configure `ALLOWED_ORIGINS` with your actual domain
- Generate a strong `SECRET_KEY` for production
- Use HTTPS in production environments
- Regularly rotate API keys
- Monitor logs for suspicious activity
