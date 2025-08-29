from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TeacherAssistantResponse(BaseModel):
    """Response schema for teacher assistant queries"""
    
    id: str = Field(
        ..., 
        description="Unique identifier for the query response"
    )
    
    curriculum: str = Field(
        ..., 
        description="The curriculum context used"
    )
    
    subject: str = Field(
        ..., 
        description="The subject context used"
    )
    
    grade: str = Field(
        ..., 
        description="The grade level context used"
    )
    
    question: str = Field(
        ..., 
        description="The original question asked"
    )
    
    input_method: str = Field(
        ..., 
        description="Method of input used"
    )
    
    answer: str = Field(
        ..., 
        description="The AI-generated answer to the teacher's question"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the query was processed"
    )
    
    status: str = Field(
        default="completed",
        description="Status of the query processing"
    )


class TeacherAssistantListResponse(BaseModel):
    """Response schema for listing multiple teacher assistant queries"""
    
    queries: List[TeacherAssistantResponse] = Field(
        ..., 
        description="List of processed queries"
    )
    
    total_count: int = Field(
        ..., 
        description="Total number of queries"
    )
