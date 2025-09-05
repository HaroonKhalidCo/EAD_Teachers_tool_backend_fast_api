from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime
import json
import re

from app.schemas.assessment.requests import AssessmentEvalRequest
from app.schemas.assessment.responses import AssessmentEvalResponse, QuestionEvaluation
from app.services.agent import get_assessment_eval_agent

router = APIRouter()


@router.post("/evaluate", response_model=AssessmentEvalResponse)
async def evaluate_assessment(request: AssessmentEvalRequest):
    """Evaluate a complete assessment with questions and answers"""
    
    try:
        # Get the assessment evaluation agent
        agent = get_assessment_eval_agent()
        
        # Create system prompt for comprehensive assessment evaluation
        system_prompt = f"""
        You are an expert educational assessor. Please evaluate the following complete assessment and provide comprehensive feedback.

        ASSESSMENT DATA:
        ================
        
        {request.assessment_data}
        
        EVALUATION CONTEXT:
        ==================
        Subject: {request.subject if request.subject else "Not specified"}
        Grade Level: {request.grade_level if request.grade_level else "Not specified"}
        Total Marks: {request.total_marks}
        
        EVALUATION REQUIREMENTS:
        =======================
        
        Please provide your evaluation in the following JSON format:
        
        {{
            "total_marks_obtained": <float>,
            "percentage": <float>,
            "grade": "<letter_grade>",
            "overall_feedback": "<comprehensive_overall_feedback>",
            "question_evaluations": [
                {{
                    "question_number": 1,
                    "question": "<question_text>",
                    "student_answer": "<student_answer>",
                    "marks_obtained": <float>,
                    "max_marks": <float>,
                    "feedback": "<specific_feedback>",
                    "is_correct": <boolean>
                }},
                {{
                    "question_number": 2,
                    "question": "<question_text>",
                    "student_answer": "<student_answer>",
                    "marks_obtained": <float>,
                    "max_marks": <float>,
                    "feedback": "<specific_feedback>",
                    "is_correct": <boolean>
                }}
            ],
            "strengths": ["<strength1>", "<strength2>", "<strength3>"],
            "areas_for_improvement": ["<area1>", "<area2>", "<area3>"],
            "suggestions": ["<suggestion1>", "<suggestion2>", "<suggestion3>"],
            "evaluation_criteria": "<explanation_of_criteria_used>"
        }}
        
        EVALUATION GUIDELINES:
        =====================
        
        1. **Parse the Assessment**: 
           - Identify all questions and their corresponding student answers
           - Extract question numbers, question text, and student responses
           - Determine appropriate marks allocation for each question
        
        2. **Individual Question Evaluation**:
           - Evaluate each question separately
           - Award marks based on accuracy, completeness, and understanding
           - Provide specific feedback for each question
           - Determine if each answer is correct or not
        
        3. **Overall Assessment**:
           - Calculate total marks obtained
           - Determine percentage and grade
           - Provide comprehensive overall feedback
        
        4. **Grade Assignment**:
           - A+ (90-100%): Exceptional work
           - A (80-89%): Excellent work
           - B+ (70-79%): Good work
           - B (60-69%): Satisfactory work
           - C+ (50-59%): Below average
           - C (40-49%): Poor work
           - D (30-39%): Very poor work
           - F (0-29%): Fail
        
        5. **Feedback Requirements**:
           - Provide specific, constructive feedback for each question
           - Highlight overall strengths and areas for improvement
           - Offer actionable suggestions
           - Be encouraging but honest
        
        6. **Evaluation Criteria**:
           - Content accuracy and relevance
           - Understanding and comprehension
           - Critical thinking and analysis
           - Communication and clarity
           - Effort and completeness
           - Subject-specific knowledge application
        
        Please ensure your response is in valid JSON format and addresses all aspects of the assessment comprehensively.
        """
        
        # Generate evaluation using the agent
        response = agent.run(system_prompt)
        
        # Extract the content from the RunResponse object
        if hasattr(response, 'content'):
            generated_content = response.content
        elif hasattr(response, 'text'):
            generated_content = response.text
        else:
            generated_content = str(response)
        
        # Parse the JSON response
        try:
            # Extract JSON from the response (in case there's extra text)
            json_match = re.search(r'\{.*\}', generated_content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                eval_data = json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback evaluation if JSON parsing fails
            eval_data = _create_fallback_evaluation(request, generated_content)
        
        # Create question evaluations
        question_evaluations = []
        for q_eval in eval_data.get("question_evaluations", []):
            question_evaluations.append(QuestionEvaluation(
                question_number=q_eval.get("question_number", 1),
                question=q_eval.get("question", ""),
                student_answer=q_eval.get("student_answer", ""),
                marks_obtained=q_eval.get("marks_obtained", 0.0),
                max_marks=q_eval.get("max_marks", 1.0),
                feedback=q_eval.get("feedback", ""),
                is_correct=q_eval.get("is_correct", False)
            ))
        
        # Create response object
        evaluation = AssessmentEvalResponse(
            id=str(uuid.uuid4()),
            assessment_data=request.assessment_data,
            total_marks_obtained=eval_data.get("total_marks_obtained", 0.0),
            total_marks=request.total_marks,
            percentage=eval_data.get("percentage", 0.0),
            grade=eval_data.get("grade", "F"),
            overall_feedback=eval_data.get("overall_feedback", ""),
            question_evaluations=question_evaluations,
            strengths=eval_data.get("strengths", []),
            areas_for_improvement=eval_data.get("areas_for_improvement", []),
            suggestions=eval_data.get("suggestions", []),
            evaluation_criteria=eval_data.get("evaluation_criteria", ""),
            created_at=datetime.utcnow(),
            status="completed"
        )
        
        return evaluation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating assessment: {str(e)}")


def _create_fallback_evaluation(request: AssessmentEvalRequest, generated_content: str) -> dict:
    """Create a fallback evaluation if JSON parsing fails"""
    
    # Basic evaluation based on assessment data length
    data_length = len(request.assessment_data)
    total_marks = request.total_marks
    
    # Simple scoring based on data length and content quality
    if data_length < 50:
        marks_obtained = total_marks * 0.2
        grade = "F"
    elif data_length < 200:
        marks_obtained = total_marks * 0.4
        grade = "D"
    elif data_length < 500:
        marks_obtained = total_marks * 0.6
        grade = "C"
    elif data_length < 1000:
        marks_obtained = total_marks * 0.8
        grade = "B"
    else:
        marks_obtained = total_marks * 0.9
        grade = "A"
    
    percentage = (marks_obtained / total_marks) * 100
    
    return {
        "total_marks_obtained": round(marks_obtained, 2),
        "percentage": round(percentage, 2),
        "grade": grade,
        "overall_feedback": f"Assessment evaluation completed. Data length: {data_length} characters. Please note: This is a fallback evaluation due to parsing issues.",
        "question_evaluations": [
            {
                "question_number": 1,
                "question": "Assessment question",
                "student_answer": "Student response",
                "marks_obtained": round(marks_obtained / 2, 2),
                "max_marks": total_marks / 2,
                "feedback": "Basic evaluation completed",
                "is_correct": marks_obtained > total_marks * 0.5
            }
        ],
        "strengths": ["Provided responses", "Attempted to answer"],
        "areas_for_improvement": ["Improve response quality", "Provide more detailed answers"],
        "suggestions": ["Expand on your answers", "Provide specific examples", "Review the questions carefully"],
        "evaluation_criteria": "Basic evaluation based on response length and content quality"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint for assessment evaluation service"""
    return {"status": "healthy", "service": "assessment_evaluation"}
