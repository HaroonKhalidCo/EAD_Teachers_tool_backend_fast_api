from pydantic import BaseModel, Field
from typing import Optional


class HomeworkGeneratorRequest(BaseModel):
    """Request schema for homework generation"""
    
    curriculum: str = Field(
        ...,
        description="The curriculum context for homework generation",
        example="National Curriculum"
    )
    
    subject: str = Field(
        ...,
        description="The subject for homework generation",
        example="Mathematics"
    )
    
    grade: str = Field(
        ...,
        description="The grade level for homework generation",
        example="Grade 5"
    )
    
    topic: str = Field(
        ...,
        description="The specific topic for homework",
        example="Fractions and Decimals"
    )
    
    difficulty_level: Optional[str] = Field(
        "Medium",
        description="Difficulty level of the homework",
        example="Easy, Medium, Hard"
    )
    
    additional_requirements: Optional[str] = Field(
        None,
        description="Additional requirements or specific focus areas",
        example="Include word problems, focus on practical applications"
    )
