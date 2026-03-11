from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ResumeCreate(BaseModel):
    filename: str
    file_path: str
    extracted_text: Optional[str] = None

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_path: str
    extracted_text: Optional[str]
    analysis_result: Optional[Dict[str, Any]]
    score: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ResumeAnalysis(BaseModel):
    score: int
    strengths: List[str]
    missing_skills: List[str]
    improvement_suggestions: List[str]
    skill_gap_analysis: Optional[Dict[str, Any]] = None
