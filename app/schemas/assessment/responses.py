from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class AssessmentResponse(BaseModel):
    """Response schema for assessment generation"""
    
    id: str = Field(
        ..., 
        description="Unique identifier for the generated assessment"
    )
    
    question_types: List[str] = Field(
        ..., 
        description="Question types used in the assessment"
    )
    
    text_content: str = Field(
        ..., 
        description="The original text content used to generate the assessment"
    )
    
    generated_assessment: str = Field(
        ..., 
        description="The complete generated assessment content"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the assessment was generated"
    )
    
    status: str = Field(
        default="completed",
        description="Status of the assessment generation"
    )


class AssessmentListResponse(BaseModel):
    """Response schema for listing multiple assessments"""
    
    assessments: List[AssessmentResponse] = Field(
        ..., 
        description="List of generated assessments"
    )
    
    total_count: int = Field(
        ..., 
        description="Total number of assessments"
    )
