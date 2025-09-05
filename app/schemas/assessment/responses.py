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
        description="Question types used in the assessment (fixed: 5 MCQs + 2 Short Questions)"
    )
    
    text_content: str = Field(
        ..., 
        description="The original content used to generate the assessment (text content or curriculum details)"
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


class QuestionEvaluation(BaseModel):
    """Individual question evaluation"""
    
    question_number: int = Field(
        ...,
        description="Question number"
    )
    
    question: str = Field(
        ...,
        description="The question text"
    )
    
    student_answer: str = Field(
        ...,
        description="Student's answer to the question"
    )
    
    marks_obtained: float = Field(
        ...,
        description="Marks obtained for this question",
        ge=0
    )
    
    max_marks: float = Field(
        ...,
        description="Maximum marks for this question"
    )
    
    feedback: str = Field(
        ...,
        description="Specific feedback for this question"
    )
    
    is_correct: bool = Field(
        ...,
        description="Whether the answer is correct"
    )


class AssessmentEvalResponse(BaseModel):
    """Response schema for comprehensive assessment evaluation"""
    
    id: str = Field(
        ..., 
        description="Unique identifier for the evaluation"
    )
    
    assessment_data: str = Field(
        ..., 
        description="The original assessment data that was evaluated"
    )
    
    total_marks_obtained: float = Field(
        ...,
        description="Total marks obtained by the student",
        ge=0
    )
    
    total_marks: int = Field(
        ...,
        description="Total possible marks for the assessment"
    )
    
    percentage: float = Field(
        ...,
        description="Percentage score achieved",
        ge=0,
        le=100
    )
    
    grade: str = Field(
        ...,
        description="Overall letter grade based on performance",
        example="A+"
    )
    
    overall_feedback: str = Field(
        ...,
        description="Overall feedback on the student's performance"
    )
    
    question_evaluations: List[QuestionEvaluation] = Field(
        ...,
        description="Individual evaluation for each question"
    )
    
    strengths: List[str] = Field(
        ...,
        description="List of overall strengths identified"
    )
    
    areas_for_improvement: List[str] = Field(
        ...,
        description="List of areas where the student can improve"
    )
    
    suggestions: List[str] = Field(
        ...,
        description="Specific suggestions for improvement"
    )
    
    evaluation_criteria: str = Field(
        ...,
        description="Explanation of the evaluation criteria used"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the evaluation was completed"
    )
    
    status: str = Field(
        default="completed",
        description="Status of the evaluation"
    )
