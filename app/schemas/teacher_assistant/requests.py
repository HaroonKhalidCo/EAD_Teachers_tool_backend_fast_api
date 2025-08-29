from pydantic import BaseModel, Field
from typing import Optional


class TeacherAssistantRequest(BaseModel):
    """Request schema for teacher assistant queries based on the UI form"""
    
    curriculum: str = Field(
        ...,
        description="The curriculum context for the question",
        example="National Curriculum"
    )
    
    subject: str = Field(
        ...,
        description="The subject context for the question",
        example="Mathematics"
    )
    
    grade: str = Field(
        ...,
        description="The grade level context for the question",
        example="Grade 5"
    )
    
    question: str = Field(
        ...,
        description="The teacher's question or query for assistance",
        example="Suggest a fun activity to teach fractions..."
    )
    
    input_method: Optional[str] = Field(
        "text",
        description="Method of input - text or voice",
        example="text"
    )
