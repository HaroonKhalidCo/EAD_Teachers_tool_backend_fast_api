from pydantic import BaseModel, Field
from typing import Optional


class AssessmentRequest(BaseModel):
    """Request schema for generating an assessment with customizable number of MCQs and short questions"""
    
    # Curriculum-based content (optional)
    curriculum: Optional[str] = Field(
        None,
        description="The curriculum to base the assessment on (e.g., CBSE, ICSE, IB, etc.)",
        example="CBSE"
    )
    
    grade: Optional[str] = Field(
        None,
        description="The grade level for the assessment",
        example="Grade 10"
    )
    
    class_level: Optional[str] = Field(
        None,
        description="The class level for the assessment",
        example="Class X"
    )
    
    subject: Optional[str] = Field(
        None,
        description="The subject for the assessment",
        example="Mathematics"
    )
    
    # Text-based content (optional)
    text_content: Optional[str] = Field(
        None,
        description="Detailed text content to base the assessment on (alternative to curriculum-based)",
        min_length=10,
        example="Mathematics curriculum covering algebra fundamentals including linear equations, inequalities, and graphing. Students will learn to solve equations, graph linear functions, and apply algebraic concepts to real-world problems."
    )
    
    # Question counts
    mcq_count: int = Field(
        5,
        description="Number of multiple choice questions to generate",
        ge=1,
        le=20,
        example=5
    )
    
    short_question_count: int = Field(
        2,
        description="Number of short answer questions to generate",
        ge=1,
        le=10,
        example=2
    )
    
    # Validation to ensure at least one content source is provided
    class Config:
        @classmethod
        def validate_content_source(cls, values):
            if not values.get('text_content') and not all([
                values.get('curriculum'),
                values.get('grade'),
                values.get('class_level'),
                values.get('subject')
            ]):
                raise ValueError("Either provide detailed text_content OR all curriculum fields (curriculum, grade, class_level, subject)")
            return values
