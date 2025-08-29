from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.schemas.assessment.requests import AssessmentRequest
from app.schemas.assessment.responses import AssessmentResponse, AssessmentListResponse
from app.services.agent import get_assessment_agent

router = APIRouter()


@router.post("/generate", response_model=AssessmentResponse)
async def generate_assessment(request: AssessmentRequest):
    """Generate an assessment based on question types and text content"""
    
    try:
        # Get agent when needed
        agent = get_assessment_agent()
        
        # Create system prompt for the agent
        question_types_str = ", ".join(request.question_types)
        system_prompt = f"""
        Generate a comprehensive educational assessment based on the following requirements:
        
        Question Types: {question_types_str}
        Text Content: {request.text_content}
        
        Please create a high-quality assessment that includes:
        1. Clear instructions for students
        2. Well-structured questions based on the selected types: {question_types_str}
        3. Appropriate difficulty level for the content
        4. Answer key or rubric for grading
        5. Learning objectives being assessed
        6. Time allocation recommendations
        
        For Multiple Choice Questions:
        - Include 4-5 options per question
        - Ensure only one correct answer
        - Make distractors plausible but clearly incorrect
        
        For Short Answer Questions:
        - Provide clear expectations for response length
        - Include sample answers or key points to look for
        
        Make the assessment engaging, fair, and aligned with educational best practices.
        """
        
        # Generate assessment using the agent
        response = agent.run(system_prompt)
        
        # Extract the content from the RunResponse object
        if hasattr(response, 'content'):
            generated_content = response.content
        elif hasattr(response, 'text'):
            generated_content = response.text
        else:
            generated_content = str(response)
        
        # Create response object
        assessment = AssessmentResponse(
            id=str(uuid.uuid4()),
            question_types=request.question_types,
            text_content=request.text_content,
            generated_assessment=generated_content,
            created_at=datetime.utcnow(),
            status="completed"
        )
        
        return assessment
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating assessment: {str(e)}")


@router.get("/", response_model=AssessmentListResponse)
async def list_assessments():
    """List all generated assessments"""
    # This would typically query a database
    # For now, returning empty list
    return AssessmentListResponse(
        assessments=[],
        total_count=0
    )


@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(assessment_id: str):
    """Get a specific assessment by ID"""
    # This would typically query a database
    # For now, returning 404
    raise HTTPException(status_code=404, detail="Assessment not found")
