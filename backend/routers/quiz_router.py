from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from services.auth import get_current_active_user
from services.quiz_service import QuizService
from models.user import User
from models.quiz import Quiz, QuizAttempt
from schemas.quiz import QuizRequest, QuizAnswerRequest

router = APIRouter(prefix="/quiz", tags=["quiz"])
quiz_service = QuizService()

class QuizRequest(BaseModel):
    category: str
    num_questions: Optional[int] = 10
    difficulty: Optional[str] = "medium"

class QuizAnswerRequest(BaseModel):
    quiz_id: int
    answers: List[dict]

@router.get("/categories")
async def get_quiz_categories(
    current_user: User = Depends(get_current_active_user)
):
    """Get available quiz categories."""
    try:
        categories = quiz_service.get_quiz_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@router.post("/generate")
async def generate_quiz(
    request: QuizRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate a new quiz."""
    try:
        # Generate quiz data
        quiz_data = quiz_service.generate_quiz(
            request.category,
            request.num_questions,
            request.difficulty
        )
        
        # Create quiz record in database
        quiz = quiz_service.create_quiz_in_db({
            "title": f"{request.category.title()} Quiz",
            "category": request.category,
            "questions": quiz_data["questions"],
            "difficulty": request.difficulty
        }, db)
        
        return {
            "quiz_id": quiz.id,
            "title": quiz.title,
            "category": quiz.category,
            "difficulty": quiz.difficulty,
            "questions": quiz_data["questions"],
            "total_questions": quiz_data["total_questions"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

# Alternative endpoint for frontend compatibility
@router.post("/start")
async def start_quiz(
    request: QuizRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start a new quiz (alternative endpoint)."""
    return await generate_quiz(request, current_user, db)

@router.post("/submit", response_model=dict)
async def submit_quiz(
    request: QuizAnswerRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit quiz answers and get feedback."""
    try:
        # Verify quiz exists
        quiz = db.query(Quiz).filter(Quiz.id == request.quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        # Evaluate the quiz attempt
        evaluation_result = quiz_service.evaluate_quiz_attempt(
            request.quiz_id,
            request.answers,
            db
        )
        
        # Save the attempt
        attempt = quiz_service.save_quiz_attempt(
            current_user.id,
            request.quiz_id,
            request.answers,
            evaluation_result,
            db
        )
        
        return {
            "attempt_id": attempt.id,
            "quiz_id": request.quiz_id,
            "score": evaluation_result["score"],
            "correct_answers": evaluation_result["correct_answers"],
            "total_questions": evaluation_result["total_questions"],
            "percentage": evaluation_result["percentage"],
            "performance_feedback": evaluation_result["performance_feedback"],
            "detailed_feedback": evaluation_result["detailed_feedback"],
            "completed_at": attempt.completed_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting quiz: {str(e)}")

@router.get("/history")
async def get_quiz_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get quiz history for the current user."""
    try:
        attempts = quiz_service.get_user_quiz_history(current_user.id, db)
        
        history = []
        for attempt in attempts:
            history.append({
                "attempt_id": attempt.id,
                "quiz_id": attempt.quiz_id,
                "quiz_title": attempt.quiz.title if attempt.quiz else "Unknown Quiz",
                "quiz_category": attempt.quiz.category if attempt.quiz else "Unknown",
                "score": attempt.score,
                "total_questions": attempt.total_questions,
                "percentage": round((attempt.score / attempt.total_questions) * 100, 1) if attempt.total_questions > 0 else 0,
                "completed_at": attempt.completed_at
            })
        
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quiz history: {str(e)}")

# Alternative endpoint for frontend compatibility
@router.get("/")
async def get_quiz_list(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get quiz list (alias for history)."""
    return await get_quiz_history(current_user, db)

@router.post("/answer")
async def submit_quiz_answer_single(
    data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit a single quiz answer."""
    try:
        # This endpoint is for single answer submission
        # For now, redirect to submit endpoint with proper format
        return {"message": "Please use /quiz/submit endpoint for submitting answers"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/performance-stats")
async def get_performance_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get performance statistics for the current user."""
    try:
        stats = quiz_service.get_user_performance_stats(current_user.id, db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching performance stats: {str(e)}")

@router.get("/available")
async def get_available_quizzes(
    category: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get available quizzes."""
    try:
        query = db.query(Quiz)
        
        if category:
            query = query.filter(Quiz.category == category)
        
        quizzes = query.all()
        
        available_quizzes = []
        for quiz in quizzes:
            available_quizzes.append({
                "quiz_id": quiz.id,
                "title": quiz.title,
                "category": quiz.category,
                "difficulty": quiz.difficulty,
                "total_questions": len(quiz.questions) if quiz.questions else 0,
                "created_at": quiz.created_at
            })
        
        return {"quizzes": available_quizzes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching available quizzes: {str(e)}")

@router.get("/{quiz_id}")
async def get_quiz_details(
    quiz_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get quiz details (without answers)."""
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        # Remove correct answers from questions
        questions_for_user = []
        for question in quiz.questions:
            question_copy = question.copy()
            question_copy.pop("correct_answer", None)
            question_copy.pop("explanation", None)
            questions_for_user.append(question_copy)
        
        return {
            "quiz_id": quiz.id,
            "title": quiz.title,
            "category": quiz.category,
            "difficulty": quiz.difficulty,
            "questions": questions_for_user,
            "total_questions": len(questions_for_user)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quiz details: {str(e)}")
