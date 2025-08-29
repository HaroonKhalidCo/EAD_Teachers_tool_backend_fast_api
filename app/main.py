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
    student_assistant,
    teacher_assistant,
    homework_generator
)

# Create FastAPI app
app = FastAPI(
    title="EAD Teachers Tool Backend",
    description="AI-powered educational tools for teachers including lesson planning, assessment generation, and educational assistance",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
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
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
