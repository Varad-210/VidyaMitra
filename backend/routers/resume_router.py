from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.auth import get_current_active_user
from services.resume_service import ResumeService
from models.user import User
from models.resume import Resume
from schemas.resume import ResumeResponse, ResumeAnalysis

router = APIRouter(prefix="/resume", tags=["resume"])
resume_service = ResumeService()

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload and analyze a resume."""
    try:
        resume = await resume_service.process_resume(file, current_user.id, db)
        return resume
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@router.get("/", response_model=List[ResumeResponse])
async def get_resumes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all resumes for the current user."""
    resumes = resume_service.get_user_resumes(current_user.id, db)
    return resumes

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific resume by ID."""
    resume = resume_service.get_resume_by_id(resume_id, current_user.id, db)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.get("/{resume_id}/analysis", response_model=ResumeAnalysis)
async def get_resume_analysis(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed analysis of a resume."""
    resume = resume_service.get_resume_by_id(resume_id, current_user.id, db)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not resume.analysis_result:
        raise HTTPException(status_code=400, detail="Resume analysis not available")
    
    return ResumeAnalysis(**resume.analysis_result)
