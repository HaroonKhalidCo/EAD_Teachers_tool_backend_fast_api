import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import agno modules once
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools

def get_lesson_plan_agent():
    """Get lesson plan agent with lazy initialization"""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return Agent(
        model=Gemini(api_key=GOOGLE_API_KEY, id="gemini-2.5-flash"),
        description="You are an expert educational consultant specializing in lesson planning and curriculum development. You help teachers create engaging, standards-aligned lesson plans that incorporate best practices in pedagogy.",
        tools=[],
        show_tool_calls=True,
        markdown=True
    )

def get_term_plan_agent():
    """Get term plan agent with lazy initialization"""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return Agent(
        model=Gemini(api_key=GOOGLE_API_KEY, id="gemini-2.5-flash"),
        description="You are a curriculum specialist who creates comprehensive term plans that align with educational standards and learning objectives. You help teachers plan entire terms with proper pacing and assessment strategies.",
        tools=[DuckDuckGoTools()],
        show_tool_calls=True,
        markdown=True
    )

def get_assessment_agent():
    """Get assessment agent with lazy initialization"""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return Agent(
        model=Gemini(api_key=GOOGLE_API_KEY, id="gemini-2.5-flash"),
        description="You are an assessment expert who creates high-quality educational assessments including quizzes, tests, and projects. You ensure assessments are aligned with learning objectives and provide meaningful feedback opportunities.",
        tools=[],
        show_tool_calls=True,
        markdown=True
    )

def get_student_assistant_agent():
    """Get student assistant agent with lazy initialization"""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return Agent(
        model=Gemini(api_key=GOOGLE_API_KEY, id="gemini-2.5-flash"),
        description="You are a patient and knowledgeable tutor who helps students understand complex concepts, solve problems, and develop critical thinking skills. You adapt your explanations to the student's grade level and learning style.",
        tools=[DuckDuckGoTools()],
        show_tool_calls=True,
        markdown=True
    )

def get_teacher_assistant_agent():
    """Get teacher assistant agent with lazy initialization"""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return Agent(
        model=Gemini(api_key=GOOGLE_API_KEY, id="gemini-2.5-flash"),
        description="You are an experienced educational consultant who provides teachers with practical advice on lesson planning, teaching strategies, classroom management, and educational resources. You offer evidence-based recommendations.",
        tools=[DuckDuckGoTools()],
        show_tool_calls=True,
        markdown=True
    )

def get_homework_generator_agent():
    """Get homework generator agent with lazy initialization"""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return Agent(
        model=Gemini(api_key=GOOGLE_API_KEY, id="gemini-2.5-flash"),
        description="You are a homework specialist who creates engaging and appropriate homework assignments that reinforce classroom learning, promote independent thinking, and provide meaningful practice opportunities for students.",
        tools=[DuckDuckGoTools()],
        show_tool_calls=True,
        markdown=True
    ) 