from pydantic import BaseModel, Field
from typing import Optional


class LessonPlanRequest(BaseModel):
    """Request schema for generating a lesson plan based on the UI form"""
    
    syllabus_file: bytes = Field(
        ...,
        description="The content of the syllabus PDF file to upload"
    )
    
    number_of_classes: int = Field(
        1,
        description="The number of classes for which to generate lesson plans",
        ge=1
    )
    
    class_duration: str = Field(
        "45 minutes",
        description="The desired duration for each class",
        example="45 minutes"
    )
    
    teaching_style: str = Field(
        "Interactive",
        description="The preferred teaching style for the lesson plan",
        example="Interactive"
    )
    
    homework_level: str = Field(
        "Moderate",
        description="The desired level of homework for the lesson plan",
        example="Moderate"
    )
