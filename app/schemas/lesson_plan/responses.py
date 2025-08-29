from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class LessonPlanResponse(BaseModel):
    """Response schema for lesson plan generation"""
    
    id: str = Field(
        ..., 
        description="Unique identifier for the generated lesson plan"
    )
    
    syllabus_filename: str = Field(
        ..., 
        description="Name or identifier of the syllabus content used"
    )
    
    number_of_classes: int = Field(
        ..., 
        description="Number of classes the lesson plan covers"
    )
    
    class_duration: str = Field(
        ..., 
        description="Duration of each class"
    )
    
    teaching_style: str = Field(
        ..., 
        description="Teaching style used in the lesson plan"
    )
    
    homework_level: str = Field(
        ..., 
        description="Level of homework assigned"
    )
    
    generated_plan: str = Field(
        ..., 
        description="The complete generated lesson plan content"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the plan was generated"
    )
    
    status: str = Field(
        default="completed",
        description="Status of the plan generation"
    )


class LessonPlanListResponse(BaseModel):
    """Response schema for listing multiple lesson plans"""
    
    plans: List[LessonPlanResponse] = Field(
        ..., 
        description="List of generated lesson plans"
    )
    
    total_count: int = Field(
        ..., 
        description="Total number of lesson plans"
    )
