from pydantic import BaseModel, Field
from typing import Optional


class TermPlanRequest(BaseModel):
    """Request schema for generating a term plan"""
    
    curriculum: str = Field(
        ..., 
        description="The curriculum to follow for the term plan",
        example="National Curriculum"
    )
    
    subject: str = Field(
        ..., 
        description="The subject for which the term plan is being generated",
        example="Mathematics"
    )
    
    grade: str = Field(
        ..., 
        description="The grade level for the term plan",
        example="Grade 5"
    )
    
    additional_notes: Optional[str] = Field(
        None,
        description="Optional additional notes or specific requirements for the term plan",
        example="Focus on project-based learning, include digital literacy...",
        max_length=1000
    )
