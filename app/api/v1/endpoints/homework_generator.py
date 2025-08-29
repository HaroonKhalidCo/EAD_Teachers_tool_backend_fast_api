from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.schemas.homework_generator.requests import HomeworkGeneratorRequest
from app.schemas.homework_generator.responses import HomeworkGeneratorResponse, HomeworkGeneratorListResponse
from app.services.agent import homework_generator_agent

router = APIRouter()


@router.post("/generate", response_model=HomeworkGeneratorResponse)
async def generate_homework(request: HomeworkGeneratorRequest):
    """Generate homework based on curriculum, subject, grade, and topic"""
    
    try:
        # Create system prompt for the agent
        system_prompt = f"""
        Generate comprehensive homework assignments based on the following requirements:
        
        Curriculum: {request.curriculum}
        Subject: {request.subject}
        Grade: {request.grade}
        Topic: {request.topic}
        Difficulty Level: {request.difficulty_level}
        Additional Requirements: {request.additional_requirements or 'None specified'}
        
        Please create engaging homework that includes:
        1. Clear instructions and learning objectives
        2. Varied question types appropriate for {request.difficulty_level} level
        3. Practical applications and real-world connections
        4. Appropriate time allocation for {request.grade} students
        5. Answer key or solution guide for teachers
        6. Extension activities for advanced students
        7. Integration with {request.curriculum} standards
        
        Make the homework:
        - Age-appropriate and engaging for {request.grade} students
        - Challenging but achievable for {request.difficulty_level} level
        - Relevant to the {request.topic} in {request.subject}
        - Practical and meaningful for student learning
        
        Include a variety of question formats and ensure clear, student-friendly language.
        """
        
        # Generate homework using the agent
        response = homework_generator_agent.run(system_prompt)
        
        # Extract the content from the RunResponse object
        if hasattr(response, 'content'):
            generated_content = response.content
        elif hasattr(response, 'text'):
            generated_content = response.text
        else:
            generated_content = str(response)
        
        # Create response object
        homework = HomeworkGeneratorResponse(
            id=str(uuid.uuid4()),
            curriculum=request.curriculum,
            subject=request.subject,
            grade=request.grade,
            topic=request.topic,
            difficulty_level=request.difficulty_level,
            additional_requirements=request.additional_requirements,
            generated_homework=generated_content,
            created_at=datetime.utcnow(),
            status="completed"
        )
        
        return homework
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating homework: {str(e)}")


@router.get("/", response_model=HomeworkGeneratorListResponse)
async def list_homework_assignments():
    """List all generated homework assignments"""
    # This would typically query a database
    # For now, returning empty list
    return HomeworkGeneratorListResponse(
        homework_assignments=[],
        total_count=0
    )


@router.get("/{homework_id}", response_model=HomeworkGeneratorResponse)
async def get_homework(homework_id: str):
    """Get a specific homework assignment by ID"""
    # This would typically query a database
    # For now, returning 404
    raise HTTPException(status_code=404, detail="Homework assignment not found")
