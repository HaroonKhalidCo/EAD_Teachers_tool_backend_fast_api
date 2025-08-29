from pydantic import BaseModel, Field
from typing import Optional


class StudentAssistantRequest(BaseModel):
    """Request schema for student assistant queries"""
    
    curriculum: str = Field(
        ...,
        description="The curriculum context for the student's question",
        example="National Curriculum"
    )
    
    subject: str = Field(
        ...,
        description="The subject context for the student's question",
        example="Mathematics"
    )
    
    grade: str = Field(
        ...,
        description="The grade level context for the student's question",
        example="Grade 5"
    )
    
    question: str = Field(
        ...,
        description="The student's question or query for assistance",
        example="How do I solve this math problem?"
    )
    
    input_method: Optional[str] = Field(
        "text",
        description="Method of input - text or voice",
        example="text"
    )
