from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.api.v1.endpoints import (
    lesson_plan,
    term_plan,
    assessment,
    assessment_eval,
    student_assistant,
    teacher_assistant,
    homework_generator
)

# Get environment variables with defaults for deployment
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Create FastAPI app
app = FastAPI(
    title="EAD Teachers Tool Backend",
    description="AI-powered educational tools for teachers including lesson planning, assessment generation, and educational assistance",
    version="1.0.0"
)

# Add CORS middleware with production-ready configuration
if ENVIRONMENT == "production":
    # In production, restrict CORS to specific origins
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    if not allowed_origins or allowed_origins == [""]:
        allowed_origins = ["https://yourdomain.com"]  # Update with your actual domain
else:
    # In development, allow all origins
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    lesson_plan.router,
    prefix="/api/v1/lesson-plan",
    tags=["Lesson Plan"]
)

app.include_router(
    term_plan.router,
    prefix="/api/v1/term-plan",
    tags=["Term Plan"]
)

app.include_router(
    assessment.router,
    prefix="/api/v1/assessment",
    tags=["Assessment"]
)

app.include_router(
    assessment_eval.router,
    prefix="/api/v1/assessment-eval",
    tags=["Assessment Evaluation"]
)

app.include_router(
    student_assistant.router,
    prefix="/api/v1/student-assistant",
    tags=["Student Assistant"]
)

app.include_router(
    teacher_assistant.router,
    prefix="/api/v1/teacher-assistant",
    tags=["Teacher Assistant"]
)

app.include_router(
    homework_generator.router,
    prefix="/api/v1/homework-generator",
    tags=["Homework Generator"]
)

@app.get("/")
async def root():
    return {
        "message": "EAD Teachers Tool Backend API",
        "version": "1.0.0",
        "status": "running",
        "environment": ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
