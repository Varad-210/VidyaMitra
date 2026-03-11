from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from services.auth import get_current_active_user
from ai_agents.skill_mapper import SkillMapper
from ai_agents.recommendation_agent import RecommendationAgent
from models.user import User
from models.resume import Resume

router = APIRouter(prefix="/recommendations", tags=["recommendations"])
skill_mapper = SkillMapper()
recommendation_agent = RecommendationAgent()

class SkillGapRequest(BaseModel):
    user_skills: List[str]
    target_role: str

class RoadmapRequest(BaseModel):
    user_skills: List[str]
    target_role: str
    experience_level: Optional[str] = "beginner"

@router.post("/skill-gap")
async def analyze_skill_gap(
    request: SkillGapRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Analyze skill gaps for a target role."""
    try:
        analysis = skill_mapper.analyze_skill_gap(request.user_skills, request.target_role)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing skill gap: {str(e)}")

@router.post("/roadmap")
async def generate_roadmap(
    request: RoadmapRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Generate a personalized career roadmap."""
    try:
        roadmap = recommendation_agent.generate_career_roadmap(
            request.user_skills, 
            request.target_role, 
            request.experience_level
        )
        return roadmap
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

@router.get("/market-trends")
async def get_market_trends(
    current_user: User = Depends(get_current_active_user)
):
    """Get current market trends and in-demand skills."""
    try:
        trends = skill_mapper.get_market_trends()
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market trends: {str(e)}")

@router.get("/resume-based-roadmap")
async def get_resume_based_roadmap(
    resume_id: int,
    target_role: Optional[str] = "software_engineer",
    experience_level: Optional[str] = "beginner",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate roadmap based on resume analysis."""
    try:
        # Get resume
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        ).first()
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        if not resume.analysis_result or not resume.analysis_result.get("skill_gap_analysis"):
            raise HTTPException(status_code=400, detail="Resume analysis not available")
        
        # Extract skills from resume analysis
        skill_analysis = resume.analysis_result["skill_gap_analysis"]
        user_skills = (
            skill_analysis.get("technical_skills", []) + 
            skill_analysis.get("soft_skills", [])
        )
        
        # Generate roadmap
        roadmap = recommendation_agent.generate_career_roadmap(
            user_skills, 
            target_role, 
            experience_level
        )
        
        return roadmap
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")
