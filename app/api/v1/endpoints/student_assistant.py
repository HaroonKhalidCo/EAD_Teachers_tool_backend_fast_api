from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.schemas.student_assistant.requests import StudentAssistantRequest
from app.schemas.student_assistant.responses import StudentAssistantResponse, StudentAssistantListResponse
from app.services.agent import student_assistant_agent

router = APIRouter()


@router.post("/ask", response_model=StudentAssistantResponse)
async def ask_student_assistant(request: StudentAssistantRequest):
    """Get assistance from the student assistant"""
    
    try:
        # Create system prompt for the agent
        system_prompt = f"""
        You are helping a student with the following context:
        
        Curriculum: {request.curriculum}
        Subject: {request.subject}
        Grade: {request.grade}
        Student's Question: {request.question}
        Input Method: {request.input_method}
        
        Please provide a helpful, age-appropriate response that:
        1. Addresses the student's question clearly and patiently
        2. Uses language and examples appropriate for {request.grade} level
        3. Encourages critical thinking and problem-solving
        4. Provides step-by-step explanations when helpful
        5. Suggests additional resources or practice opportunities
        6. Maintains an encouraging and supportive tone
        
        Remember you are speaking to a student, so be patient, clear, and motivating.
        """
        
        # Get response from the student assistant agent
        response = student_assistant_agent.run(system_prompt)
        
        # Extract the content from the RunResponse object
        if hasattr(response, 'content'):
            generated_content = response.content
        elif hasattr(response, 'text'):
            generated_content = response.text
        else:
            generated_content = str(response)
        
        # Create response object
        student_response = StudentAssistantResponse(
            id=str(uuid.uuid4()),
            curriculum=request.curriculum,
            subject=request.subject,
            grade=request.grade,
            question=request.question,
            input_method=request.input_method,
            answer=generated_content,
            created_at=datetime.utcnow(),
            status="completed"
        )
        
        return student_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting student assistance: {str(e)}")


@router.get("/", response_model=StudentAssistantListResponse)
async def list_student_queries():
    """List all student assistant queries"""
    # This would typically query a database
    # For now, returning empty list
    return StudentAssistantListResponse(
        queries=[],
        total_count=0
    )


@router.get("/{query_id}", response_model=StudentAssistantResponse)
async def get_student_query(query_id: str):
    """Get a specific student query by ID"""
    # This would typically query a database
    # For now, returning 404
    raise HTTPException(status_code=404, detail="Student query not found")
