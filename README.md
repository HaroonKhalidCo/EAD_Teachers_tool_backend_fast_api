# EAD Teachers Tool Backend

AI-powered educational tools for teachers including lesson planning, assessment generation, and educational assistance.

## Features

- **Lesson Plan Generator**: Create detailed lesson plans from syllabus uploads
- **Term Plan Generator**: Generate comprehensive term plans
- **Assessment Generator**: Create quizzes and tests with multiple question types
- **Student Assistant**: AI-powered tutoring and assistance for students
- **Teacher Assistant**: Professional guidance for teachers
- **Homework Generator**: Create engaging homework assignments

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Environment
ENVIRONMENT=development
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
- **Google Gemini 2.0 Flash**: Advanced AI model for content generation
- **Pydantic**: Data validation and settings management
- **DuckDuckGo Tools**: Web search capabilities for agents
