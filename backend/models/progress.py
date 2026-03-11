from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    metric_type = Column(String, nullable=False)  # resume_score, quiz_score, interview_score
    metric_value = Column(Integer, nullable=False)
    metric_data = Column(JSON)  # Renamed from 'metadata' to avoid SQLAlchemy 2.0 conflict
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
