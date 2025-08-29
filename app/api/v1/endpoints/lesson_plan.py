from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import uuid
from datetime import datetime

from app.schemas.lesson_plan.requests import LessonPlanRequest
from app.schemas.lesson_plan.responses import LessonPlanResponse, LessonPlanListResponse
from app.services.agent import get_lesson_plan_agent

router = APIRouter()


@router.post("/generate", response_model=LessonPlanResponse)
async def generate_lesson_plan(
    syllabus_file: UploadFile = File(...),
    number_of_classes: int = 1,
    class_duration: str = "45 minutes",
    teaching_style: str = "Interactive",
    homework_level: str = "Moderate"
):
    """Generate a lesson plan based on uploaded syllabus and preferences"""
    
    try:
        # Validate file type
        if not syllabus_file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read file content
        syllabus_content = await syllabus_file.read()
        
        # Create system prompt for the agent
        system_prompt = f"""
        Generate a comprehensive lesson plan based on the following requirements:
        
        Syllabus: {syllabus_file.filename}
        Number of Classes: {number_of_classes}
        Class Duration: {class_duration}
        Teaching Style: {teaching_style}
        Homework Level: {homework_level}
        
        Please create a detailed lesson plan that includes:
        1. Learning objectives
        2. Lesson structure and activities
        3. Assessment methods
        4. Homework assignments (appropriate for {homework_level} level)
        5. Teaching strategies aligned with {teaching_style} style
        6. Timeline for {number_of_classes} classes of {class_duration} each
        
        Make the plan engaging, practical, and aligned with educational best practices.
        """
        
        # Get agent when needed
        agent = get_lesson_plan_agent()
        
        # Generate lesson plan using the agent
        response = agent.run(system_prompt)
        
        # Extract the content from the RunResponse object
        if hasattr(response, 'content'):
            generated_content = response.content
        elif hasattr(response, 'text'):
            generated_content = response.text
        else:
            generated_content = str(response)
        
        # Create response object
        lesson_plan = LessonPlanResponse(
            id=str(uuid.uuid4()),
            syllabus_filename=syllabus_file.filename,
            number_of_classes=number_of_classes,
            class_duration=class_duration,
            teaching_style=teaching_style,
            homework_level=homework_level,
            generated_plan=generated_content,
            created_at=datetime.utcnow(),
            status="completed"
        )
        
        return lesson_plan
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating lesson plan: {str(e)}")


@router.get("/", response_model=LessonPlanListResponse)
async def list_lesson_plans():
    """List all generated lesson plans"""
    # This would typically query a database
    # For now, returning empty list
    return LessonPlanListResponse(
        plans=[],
        total_count=0
    )


@router.get("/{plan_id}", response_model=LessonPlanResponse)
async def get_lesson_plan(plan_id: str):
    """Get a specific lesson plan by ID"""
    # This would typically query a database
    # For now, returning 404
    raise HTTPException(status_code=404, detail="Lesson plan not found")
