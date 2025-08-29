from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from app.schemas.term_plan.requests import TermPlanRequest
from app.schemas.term_plan.responses import TermPlanResponse, TermPlanListResponse
from app.services.agent import term_plan_agent

router = APIRouter()


@router.post("/generate", response_model=TermPlanResponse)
async def generate_term_plan(request: TermPlanRequest):
    """Generate a term plan based on curriculum, subject, and grade"""
    
    try:
        # Create system prompt for the agent
        system_prompt = f"""
        Generate a comprehensive term plan based on the following requirements:
        
        Curriculum: {request.curriculum}
        Subject: {request.subject}
        Grade: {request.grade}
        Additional Notes: {request.additional_notes or 'None provided'}
        
        Please create a detailed term plan that includes:
        1. Term overview and learning objectives
        2. Weekly breakdown of topics and concepts
        3. Assessment schedule and methods
        4. Teaching strategies and resources
        5. Student progress tracking methods
        6. Integration with {request.curriculum} standards
        7. Differentiation strategies for various learning levels
        
        Make the plan comprehensive, well-structured, and aligned with educational best practices for {request.grade} {request.subject}.
        """
        
        # Generate term plan using the agent
        response = term_plan_agent.run(system_prompt)
        
        # Extract the content from the RunResponse object
        if hasattr(response, 'content'):
            generated_content = response.content
        elif hasattr(response, 'text'):
            generated_content = response.text
        else:
            generated_content = str(response)
        
        # Create response object
        term_plan = TermPlanResponse(
            id=str(uuid.uuid4()),
            curriculum=request.curriculum,
            subject=request.subject,
            grade=request.grade,
            additional_notes=request.additional_notes,
            generated_plan=generated_content,
            created_at=datetime.utcnow(),
            status="completed"
        )
        
        return term_plan
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating term plan: {str(e)}")


@router.get("/", response_model=TermPlanListResponse)
async def list_term_plans():
    """List all generated term plans"""
    # This would typically query a database
    # For now, returning empty list
    return TermPlanListResponse(
        plans=[],
        total_count=0
    )


@router.get("/{plan_id}", response_model=TermPlanResponse)
async def get_term_plan(plan_id: str):
    """Get a specific term plan by ID"""
    # This would typically query a database
    # For now, returning 404
    raise HTTPException(status_code=404, detail="Term plan not found")
