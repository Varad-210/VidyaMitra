from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class InterviewStartRequest(BaseModel):
    job_role: str
    experience_level: Optional[str] = "beginner"
    skills: Optional[List[str]] = []
    num_questions: Optional[int] = 10

class InterviewAnswerRequest(BaseModel):
    interview_id: int
    question_id: Optional[int] = None
    question: str
    answer: str

class InterviewCreate(BaseModel):
    job_role: str

class InterviewResponse(BaseModel):
    id: int
    user_id: int
    job_role: str
    questions: Optional[List[str]]
    feedback: Optional[Dict[str, Any]]
    overall_score: Optional[int]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class InterviewAnswerCreate(BaseModel):
    interview_id: int
    question: str
    answer: str

class InterviewAnswerResponse(BaseModel):
    id: int
    interview_id: int
    question: str
    answer: str
    feedback: Optional[Dict[str, Any]]
    clarity_score: Optional[int]
    confidence_score: Optional[int]
    accuracy_score: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
