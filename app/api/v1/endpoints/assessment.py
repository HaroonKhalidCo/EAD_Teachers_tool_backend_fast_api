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
    """Generate an assessment with customizable number of MCQs and short questions based on content"""
    
    try:
        # Validate that at least one content source is provided
        if not request.text_content and not all([
            request.curriculum,
            request.grade,
            request.class_level,
            request.subject
        ]):
            raise HTTPException(
                status_code=400, 
                detail="Either provide detailed text_content OR all curriculum fields (curriculum, grade, class_level, subject)"
            )
        
        # Get agent when needed
        agent = get_assessment_agent()
        
        # Determine content source for the prompt
        if request.text_content:
            content_source = f"Text Content: {request.text_content}"
        else:
            content_source = f"""
            Curriculum: {request.curriculum}
            Grade: {request.grade}
            Class: {request.class_level}
            Subject: {request.subject}
            """
        
        # Create system prompt for the agent
        system_prompt = f"""
        Generate an educational assessment based on the following content:
        
        {content_source}
        
        Please create an assessment with the EXACT following structure:
        
        ========================================
        ASSESSMENT QUESTIONS
        ========================================
        
        MULTIPLE CHOICE QUESTIONS ({request.mcq_count} questions):
        ------------------------------------------------------
        
        {_generate_mcq_template(request.mcq_count)}
        
        SHORT ANSWER QUESTIONS ({request.short_question_count} questions):
        --------------------------------------------------------------
        
        {_generate_short_question_template(request.short_question_count)}
        
        ========================================
        ASSESSMENT GUIDELINES
        ========================================
        
        Instructions for Students:
        - Read each question carefully
        - For multiple choice questions, select the BEST answer
        - For short answer questions, provide detailed responses with examples
        - Time allocation: {_calculate_time_allocation(request.mcq_count, request.short_question_count)} minutes total
        
        Grading Criteria:
        - Multiple Choice: 2 points each (Total: {request.mcq_count * 2} points)
        - Short Answer: 5 points each (Total: {request.short_question_count * 5} points)
        - Total Assessment: {(request.mcq_count * 2) + (request.short_question_count * 5)} points
        
        Requirements:
        - Questions must be directly related to the provided content
        - Multiple choice questions should have 4 options (A, B, C, D)
        - Only one correct answer per multiple choice question
        - Short answer questions should require 2-3 sentences minimum
        - All questions should test understanding, application, and critical thinking
        - Difficulty should be appropriate for the content level
        - DO NOT include any answers or answer keys
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
            question_types=[f"{request.mcq_count} Multiple Choice Questions", f"{request.short_question_count} Short Answer Questions"],
            text_content=request.text_content or f"{request.curriculum} - {request.grade} - {request.class_level} - {request.subject}",
            generated_assessment=generated_content,
            created_at=datetime.utcnow(),
            status="completed"
        )
        
        return assessment
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating assessment: {str(e)}")

def _generate_mcq_template(count: int) -> str:
    """Generate MCQ template based on count"""
    template = ""
    for i in range(1, count + 1):
        template += f"""
        {i}. [Question {i}]
           A) [Option A]
           B) [Option B]
           C) [Option C]
           D) [Option D]
        """
    return template

def _generate_short_question_template(count: int) -> str:
    """Generate short question template based on count"""
    template = ""
    for i in range(1, count + 1):
        question_num = i + 5  # Start from 6 if we have 5 MCQs
        template += f"""
        {question_num}. [Question {question_num}]
           [Provide clear instructions for expected response length and format]
        """
    return template

def _calculate_time_allocation(mcq_count: int, short_count: int) -> int:
    """Calculate recommended time allocation"""
    mcq_time = mcq_count * 2  # 2 minutes per MCQ
    short_time = short_count * 5  # 5 minutes per short question
    return mcq_time + short_time


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
