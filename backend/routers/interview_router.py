from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from services.auth import get_current_active_user
from ai_agents.interview_agent import InterviewAgent
from models.user import User
from models.interview import Interview, InterviewAnswer
from schemas.interview import InterviewStartRequest, InterviewAnswerRequest

router = APIRouter(prefix="/interview", tags=["interview"])
interview_agent = InterviewAgent()

@router.post("/start", response_model=dict)
async def start_interview(
    request: InterviewStartRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start a new mock interview session."""
    try:
        # Generate interview questions
        questions = interview_agent.generate_interview_questions(
            request.job_role, 
            request.num_questions
        )
        
        # Create interview record
        interview = Interview(
            user_id=current_user.id,
            job_role=request.job_role,
            questions=questions,
            status="started"
        )
        
        db.add(interview)
        db.commit()
        db.refresh(interview)
        
        return {
            "interview_id": interview.id,
            "job_role": request.job_role,
            "questions": questions,
            "status": "started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting interview: {str(e)}")

@router.post("/submit-answer", response_model=dict)
async def submit_answer(
    request: InterviewAnswerRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit an answer and get feedback."""
    try:
        # Verify interview exists and belongs to user
        interview = db.query(Interview).filter(
            Interview.id == request.interview_id,
            Interview.user_id == current_user.id
        ).first()
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        # Analyze the answer
        feedback = interview_agent.analyze_answer(
            request.question,
            request.answer,
            interview.job_role
        )
        
        # Create answer record
        interview_answer = InterviewAnswer(
            interview_id=request.interview_id,
            question=request.question,
            answer=request.answer,
            feedback=feedback,
            clarity_score=feedback["clarity"]["score"],
            confidence_score=feedback["confidence"]["score"],
            accuracy_score=feedback["accuracy"]["score"]
        )
        
        db.add(interview_answer)
        db.commit()
        db.refresh(interview_answer)
        
        return {
            "answer_id": interview_answer.id,
            "feedback": feedback,
            "scores": {
                "clarity": feedback["clarity"]["score"],
                "confidence": feedback["confidence"]["score"],
                "accuracy": feedback["accuracy"]["score"],
                "overall": feedback["overall"]["score"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting answer: {str(e)}")

# Alternative endpoint for frontend compatibility
@router.post("/answer")
async def submit_answer_alt(
    request: InterviewAnswerRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit an answer and get feedback (alternative endpoint accepting JSON body)."""
    return await submit_answer(request, current_user, db)

@router.get("/{interview_id}/status")
async def get_interview_status(
    interview_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get interview status and progress."""
    try:
        interview = db.query(Interview).filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id
        ).first()
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        # Get all answers for this interview
        answers = db.query(InterviewAnswer).filter(
            InterviewAnswer.interview_id == interview_id
        ).all()
        
        # Calculate progress
        total_questions = len(interview.questions) if interview.questions else 0
        answered_questions = len(answers)
        progress = (answered_questions / total_questions * 100) if total_questions > 0 else 0
        
        # Calculate average scores
        avg_scores = {}
        if answers:
            avg_scores["clarity"] = sum(a.clarity_score for a in answers if a.clarity_score) / len([a for a in answers if a.clarity_score])
            avg_scores["confidence"] = sum(a.confidence_score for a in answers if a.confidence_score) / len([a for a in answers if a.confidence_score])
            avg_scores["accuracy"] = sum(a.accuracy_score for a in answers if a.accuracy_score) / len([a for a in answers if a.accuracy_score])
            avg_scores["overall"] = (avg_scores["clarity"] + avg_scores["confidence"] + avg_scores["accuracy"]) / 3
        
        return {
            "interview_id": interview.id,
            "job_role": interview.job_role,
            "status": interview.status,
            "progress": round(progress, 1),
            "total_questions": total_questions,
            "answered_questions": answered_questions,
            "average_scores": {k: round(v, 1) for k, v in avg_scores.items()} if avg_scores else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting interview status: {str(e)}")

@router.get("/{interview_id}/feedback")
async def get_interview_feedback(
    interview_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get interview feedback (alias for status)."""
    return await get_interview_status(interview_id, current_user, db)

@router.post("/{interview_id}/complete")
async def complete_interview(
    interview_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Complete the interview and get final feedback."""
    try:
        interview = db.query(Interview).filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id
        ).first()
        
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
        
        # Get all answers
        answers = db.query(InterviewAnswer).filter(
            InterviewAnswer.interview_id == interview_id
        ).all()
        
        if not answers:
            raise HTTPException(status_code=400, detail="No answers found for this interview")
        
        # Calculate final scores
        total_clarity = sum(a.clarity_score for a in answers if a.clarity_score)
        total_confidence = sum(a.confidence_score for a in answers if a.confidence_score)
        total_accuracy = sum(a.accuracy_score for a in answers if a.accuracy_score)
        count = len(answers)
        
        final_scores = {
            "clarity": round(total_clarity / count, 1) if count > 0 else 0,
            "confidence": round(total_confidence / count, 1) if count > 0 else 0,
            "accuracy": round(total_accuracy / count, 1) if count > 0 else 0,
            "overall": round((total_clarity + total_confidence + total_accuracy) / (3 * count), 1) if count > 0 else 0
        }
        
        # Generate overall feedback
        overall_feedback = {
            "performance_assessment": interview_agent._get_overall_assessment(final_scores["overall"]),
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        # Identify strengths and areas for improvement
        if final_scores["clarity"] >= 70:
            overall_feedback["strengths"].append("Clear communication")
        else:
            overall_feedback["areas_for_improvement"].append("Communication clarity")
        
        if final_scores["confidence"] >= 70:
            overall_feedback["strengths"].append("Confident responses")
        else:
            overall_feedback["areas_for_improvement"].append("Response confidence")
        
        if final_scores["accuracy"] >= 70:
            overall_feedback["strengths"].append("Technical accuracy")
        else:
            overall_feedback["areas_for_improvement"].append("Technical knowledge")
        
        # Add recommendations
        overall_feedback["recommendations"] = [
            "Practice more mock interviews to improve performance",
            "Focus on areas where you scored below 70%",
            "Review technical concepts related to your target role",
            "Prepare specific examples from your experience"
        ]
        
        # Update interview status
        interview.status = "completed"
        interview.overall_score = int(final_scores["overall"])
        interview.feedback = overall_feedback
        
        db.commit()
        
        return {
            "interview_id": interview.id,
            "final_scores": final_scores,
            "overall_feedback": overall_feedback,
            "completed_at": interview.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error completing interview: {str(e)}")

@router.get("/", response_model=List[dict])
async def get_user_interviews(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all interviews for the current user."""
    try:
        interviews = db.query(Interview).filter(
            Interview.user_id == current_user.id
        ).order_by(Interview.created_at.desc()).all()
        
        result = []
        for interview in interviews:
            answers_count = db.query(InterviewAnswer).filter(
                InterviewAnswer.interview_id == interview.id
            ).count()
            
            result.append({
                "id": interview.id,
                "job_role": interview.job_role,
                "status": interview.status,
                "overall_score": interview.overall_score,
                "questions_count": len(interview.questions) if interview.questions else 0,
                "answers_count": answers_count,
                "created_at": interview.created_at
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching interviews: {str(e)}")
