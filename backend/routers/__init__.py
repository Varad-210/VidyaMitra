from .auth_router import router as auth_router
from .resume_router import router as resume_router
from .interview_router import router as interview_router
from .quiz_router import router as quiz_router
from .recommendation_router import router as recommendation_router
from .progress_router import router as progress_router

__all__ = [
    "auth_router",
    "resume_router", 
    "interview_router",
    "quiz_router",
    "recommendation_router",
    "progress_router"
]
