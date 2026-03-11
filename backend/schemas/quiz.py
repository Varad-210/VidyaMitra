from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class QuizRequest(BaseModel):
    category: str
    num_questions: Optional[int] = 10
    difficulty: Optional[str] = "medium"

class QuizAnswerRequest(BaseModel):
    quiz_attempt_id: Optional[int] = None
    question_id: int
    answer: str

class QuizCreate(BaseModel):
    title: str
    category: str
    questions: List[Dict[str, Any]]
    difficulty: str = "medium"

class QuizResponse(BaseModel):
    id: int
    title: str
    category: str
    questions: List[Dict[str, Any]]
    difficulty: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuizAttemptCreate(BaseModel):
    quiz_id: int
    answers: List[Dict[str, Any]]

class QuizAttemptResponse(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    answers: List[Dict[str, Any]]
    score: Optional[int]
    total_questions: Optional[int]
    feedback: Optional[Dict[str, Any]]
    completed_at: datetime
    
    class Config:
        from_attributes = True
