from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.schemas.teacher_assistant.requests import TeacherAssistantRequest
from app.schemas.teacher_assistant.responses import TeacherAssistantResponse, TeacherAssistantListResponse
from app.services.agent import get_teacher_assistant_agent

router = APIRouter()


@router.post("/ask", response_model=TeacherAssistantResponse)
async def ask_teacher_assistant(request: TeacherAssistantRequest):
    """Get assistance from the teacher assistant"""
    
    try:
        # Create system prompt for the agent
        system_prompt = f"""
        You are helping a teacher with the following context:
        
        Curriculum: {request.curriculum}
        Subject: {request.subject}
        Grade: {request.grade}
        Teacher's Question: {request.question}
        Input Method: {request.input_method}
        
        Please provide professional, practical advice that:
        1. Addresses the teacher's specific question or concern
        2. Offers evidence-based teaching strategies and best practices
        3. Suggests practical classroom activities and resources
        4. Considers the {request.grade} level and {request.subject} context
        5. Aligns with {request.curriculum} standards and requirements
        6. Provides actionable recommendations and next steps
        7. References relevant educational research when appropriate
        
        Remember you are speaking to a professional educator, so be thorough, practical, and supportive.
        """
        
        # Get response from the teacher assistant agent
        agent = get_teacher_assistant_agent()
        response = agent.run(system_prompt)
        
        # Extract the content from the RunResponse object
        if hasattr(response, 'content'):
            generated_content = response.content
        elif hasattr(response, 'text'):
            generated_content = response.text
        else:
            generated_content = str(response)
        
        # Create response object
        teacher_response = TeacherAssistantResponse(
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
        
        return teacher_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting teacher assistance: {str(e)}")


@router.get("/", response_model=TeacherAssistantListResponse)
async def list_teacher_queries():
    """List all teacher assistant queries"""
    # This would typically query a database
    # For now, returning empty list
    return TeacherAssistantListResponse(
        queries=[],
        total_count=0
    )


@router.get("/{query_id}", response_model=TeacherAssistantResponse)
async def get_teacher_query(query_id: str):
    """Get a specific teacher query by ID"""
    # This would typically query a database
    # For now, returning 404
    raise HTTPException(status_code=404, detail="Teacher query not found")
