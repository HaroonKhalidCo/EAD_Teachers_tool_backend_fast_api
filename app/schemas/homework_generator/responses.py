from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class HomeworkGeneratorResponse(BaseModel):
    """Response schema for homework generation"""
    
    id: str = Field(
        ..., 
        description="Unique identifier for the generated homework"
    )
    
    curriculum: str = Field(
        ..., 
        description="The curriculum context used"
    )
    
    subject: str = Field(
        ..., 
        description="The subject of the homework"
    )
    
    grade: str = Field(
        ..., 
        description="The grade level of the homework"
    )
    
    topic: str = Field(
        ..., 
        description="The specific topic of the homework"
    )
    
    difficulty_level: str = Field(
        ..., 
        description="Difficulty level of the homework"
    )
    
    additional_requirements: Optional[str] = Field(
        None,
        description="Additional requirements provided"
    )
    
    generated_homework: str = Field(
        ..., 
        description="The complete generated homework content"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the homework was generated"
    )
    
    status: str = Field(
        default="completed",
        description="Status of the homework generation"
    )


class HomeworkGeneratorListResponse(BaseModel):
    """Response schema for listing multiple homework assignments"""
    
    homework_assignments: List[HomeworkGeneratorResponse] = Field(
        ..., 
        description="List of generated homework assignments"
    )
    
    total_count: int = Field(
        ..., 
        description="Total number of homework assignments"
    )
