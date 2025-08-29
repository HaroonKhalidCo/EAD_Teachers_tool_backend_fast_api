from pydantic import BaseModel, Field
from typing import List


class AssessmentRequest(BaseModel):
    """Request schema for generating an assessment based on the UI form"""
    
    question_types: List[str] = Field(
        ...,
        description="List of selected question types for the assessment",
        example=["Multiple Choice Questions", "Short Answer Questions"]
    )
    
    text_content: str = Field(
        ...,
        description="The text content to base the assessment on",
        example="Enter the text content here..."
    )
