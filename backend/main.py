from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import os

# Import database components
from database import engine, Base, test_connection
from routers import (
    auth_router, resume_router, interview_router, 
    quiz_router, recommendation_router, progress_router
)

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    print("🔄 Creating database tables...")
    from sqlalchemy.orm import declarative_base
    Base.registry.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    
    # Test database connection
    test_connection()
    
    yield
    
    # Cleanup if needed
    print("🔄 Application shutdown...")

# Initialize FastAPI app
app = FastAPI(
    title="VidyaMitra API",
    description="AI-driven career assistant platform backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Configure CORS
origins = [
    "http://localhost:8080",  # Frontend running on port 8080
    "http://localhost:3000",  # React dev server
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:8080", # Localhost alternative
    "http://127.0.0.1:3000", # Localhost alternative
    "http://127.0.0.1:5173", # Localhost alternative
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(quiz_router)
app.include_router(recommendation_router)
app.include_router(progress_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to VidyaMitra API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "VidyaMitra API",
        "version": "1.0.0",
        "database": "connected" if test_connection() else "disconnected"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "detail": str(exc) if os.getenv("DEBUG", "False").lower() == "true" else None
        }
    )

# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "message": "The requested resource was not found."
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
