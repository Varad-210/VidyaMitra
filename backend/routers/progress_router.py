from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from services.auth import get_current_active_user
from services.progress_service import ProgressService
from models.user import User
from schemas.progress import ProgressCreate

router = APIRouter(prefix="/progress", tags=["progress"])
progress_service = ProgressService()

@router.get("/summary")
async def get_progress_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive progress summary for the current user."""
    try:
        summary = progress_service.get_user_progress_summary(current_user.id, db)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching progress summary: {str(e)}")

@router.get("/{user_id}")
async def get_user_progress(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user progress (must be own user or admin)."""
    try:
        # Verify user can only access their own progress
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Cannot access other user's progress")
        
        summary = progress_service.get_user_progress_summary(current_user.id, db)
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user progress: {str(e)}")

@router.get("/")
async def get_current_user_progress(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's progress."""
    try:
        summary = progress_service.get_user_progress_summary(current_user.id, db)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching progress: {str(e)}")

@router.get("/detailed")
async def get_detailed_progress(
    metric_type: Optional[str] = None,
    days_back: Optional[int] = 30,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed progress for specific metrics."""
    try:
        detailed_progress = progress_service.get_detailed_progress(
            current_user.id, metric_type, days_back, db
        )
        return detailed_progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching detailed progress: {str(e)}")

@router.get("/leaderboard")
async def get_leaderboard(
    metric_type: str = "quiz_score",
    limit: Optional[int] = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get leaderboard for a specific metric."""
    try:
        if metric_type not in ["resume_score", "quiz_score", "interview_score"]:
            raise HTTPException(status_code=400, detail="Invalid metric type. Use: resume_score, quiz_score, or interview_score")
        
        leaderboard = progress_service.get_leaderboard(metric_type, limit, db)
        return {
            "metric_type": metric_type,
            "leaderboard": leaderboard
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching leaderboard: {str(e)}")

@router.get("/achievements")
async def get_achievements(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user achievements."""
    try:
        achievements = progress_service._get_achievements(current_user.id, db)
        return {"achievements": achievements}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching achievements: {str(e)}")

@router.get("/{user_id}/timeline")
async def get_progress_timeline(
    user_id: int,
    metric_type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get progress timeline for a user."""
    try:
        # Verify user can only access their own progress
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Cannot access other user's progress")
        
        detailed = progress_service.get_detailed_progress(current_user.id, metric_type, 90, db)
        return {"timeline": detailed.get("timeline", [])}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching timeline: {str(e)}")

@router.get("/{user_id}/achievements")
async def get_user_achievements(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get achievements for a user."""
    try:
        # Verify user can only access their own progress
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Cannot access other user's progress")
        
        achievements = progress_service._get_achievements(current_user.id, db)
        return {"achievements": achievements}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching achievements: {str(e)}")

@router.get("/{user_id}/statistics")
async def get_user_statistics(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get statistics for a user."""
    try:
        # Verify user can only access their own progress
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Cannot access other user's progress")
        
        summary = progress_service.get_user_progress_summary(current_user.id, db)
        return {"statistics": summary.get("statistics", {})}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

@router.get("/recommendations")
async def get_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized recommendations based on progress."""
    try:
        # Get progress summary to extract recommendations
        summary = progress_service.get_user_progress_summary(current_user.id, db)
        return {
            "recommendations": summary.get("recommendations", []),
            "based_on": "Your recent performance and trends"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {str(e)}")

@router.post("/track")
async def track_progress(
    metric_type: str,
    metric_value: int,
    metadata: Optional[dict] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Manually track progress (for testing or external tracking)."""
    try:
        if metric_type not in ["resume_score", "quiz_score", "interview_score"]:
            raise HTTPException(status_code=400, detail="Invalid metric type. Use: resume_score, quiz_score, or interview_score")
        
        if metric_type == "resume_score":
            progress = progress_service.track_resume_score(current_user.id, metric_value, db)
        elif metric_type == "quiz_score":
            quiz_category = metadata.get("category") if metadata else None
            progress = progress_service.track_quiz_score(current_user.id, metric_value, db, quiz_category)
        elif metric_type == "interview_score":
            job_role = metadata.get("job_role") if metadata else None
            progress = progress_service.track_interview_score(current_user.id, metric_value, db, job_role)
        
        return {
            "message": "Progress tracked successfully",
            "progress_id": progress.id,
            "metric_type": progress.metric_type,
            "metric_value": progress.metric_value,
            "created_at": progress.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking progress: {str(e)}")
