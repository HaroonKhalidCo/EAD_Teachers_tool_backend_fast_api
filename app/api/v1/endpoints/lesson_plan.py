from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.schemas.lesson_plan.requests import LessonPlanRequest
from app.schemas.lesson_plan.responses import LessonPlanResponse, LessonPlanListResponse
from app.services.agent import get_lesson_plan_agent

router = APIRouter()


@router.post("/generate", response_model=LessonPlanResponse)
async def generate_lesson_plan(
    request: LessonPlanRequest
):
    """Generate a detailed lesson plan based on syllabus content and preferences"""
    
    try:
        # Create comprehensive system prompt for the agent
        system_prompt = f"""
        Generate a comprehensive and detailed lesson plan based on the following requirements:
        
        Syllabus Content: {request.syllabus_content}
        Number of Classes: {request.number_of_classes}
        Class Duration: {request.class_duration}
        Teaching Style: {request.teaching_style}
        Homework Level: {request.homework_level}
        
        Please create a detailed, structured lesson plan that includes:
        
        1. LEARNING OBJECTIVES
           - Clear, measurable learning outcomes
           - Specific skills and knowledge students will acquire
           - Alignment with educational standards
        
        2. LESSON STRUCTURE AND ACTIVITIES
           - Detailed breakdown for each class session
           - Engaging activities and exercises
           - Time allocation for each activity
           - Student engagement strategies
        
        3. TEACHING STRATEGIES
           - Methods aligned with {request.teaching_style} teaching style
           - Differentiation strategies for diverse learners
           - Classroom management techniques
           - Use of technology and resources
        
        4. ASSESSMENT METHODS
           - Formative assessment strategies
           - Summative assessment options
           - Student progress monitoring
           - Feedback mechanisms
        
        5. HOMEWORK ASSIGNMENTS
           - Level-appropriate assignments for {request.homework_level} level
           - Clear instructions and expectations
           - Connection to classroom learning
           - Estimated completion time
        
        6. TIMELINE AND PACING
           - Detailed schedule for {request.number_of_classes} classes
           - Each class duration: {request.class_duration}
           - Pacing recommendations
           - Flexibility considerations
        
        7. RESOURCES AND MATERIALS
           - Required materials and equipment
           - Digital resources and tools
           - Supplementary reading materials
           - Safety considerations if applicable
        
        8. EVALUATION AND REFLECTION
           - Success criteria for the lesson
           - Reflection questions for teachers
           - Student self-assessment opportunities
           - Areas for improvement and adaptation
        
        Make the plan:
        - Practical and implementable in real classroom settings
        - Engaging and student-centered
        - Aligned with educational best practices
        - Detailed enough for teachers to follow without additional planning
        - Flexible enough to adapt to different student needs
        
        Format the response in a clear, structured manner that teachers can easily read and implement.
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
            syllabus_filename="Curriculum-based syllabus",
            number_of_classes=request.number_of_classes,
            class_duration=request.class_duration,
            teaching_style=request.teaching_style,
            homework_level=request.homework_level,
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
