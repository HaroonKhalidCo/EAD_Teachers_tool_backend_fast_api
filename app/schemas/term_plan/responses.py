from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TermPlanResponse(BaseModel):
    """Response schema for term plan generation"""
    
    id: str = Field(
        ..., 
        description="Unique identifier for the generated term plan"
    )
    
    curriculum: str = Field(
        ..., 
        description="The curriculum used for the term plan"
    )
    
    subject: str = Field(
        ..., 
        description="The subject of the term plan"
    )
    
    grade: str = Field(
        ..., 
        description="The grade level of the term plan"
    )
    
    additional_notes: Optional[str] = Field(
        None,
        description="Additional notes that were provided during generation"
    )
    
    generated_plan: str = Field(
        ..., 
        description="The complete generated term plan content"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the plan was generated"
    )
    
    status: str = Field(
        default="completed",
        description="Status of the plan generation"
    )


class TermPlanListResponse(BaseModel):
    """Response schema for listing multiple term plans"""
    
    plans: List[TermPlanResponse] = Field(
        ..., 
        description="List of generated term plans"
    )
    
    total_count: int = Field(
        ..., 
        description="Total number of term plans"
    )
