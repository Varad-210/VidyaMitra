from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    questions = Column(JSON)
    difficulty = Column(String, default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    answers = Column(JSON)
    score = Column(Integer)
    total_questions = Column(Integer)
    feedback = Column(JSON)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
    quiz = relationship("Quiz", back_populates="attempts")
