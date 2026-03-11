from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ProgressCreate(BaseModel):
    metric_type: str
    metric_value: int
    metric_data: Optional[Dict[str, Any]] = None

class ProgressResponse(BaseModel):
    id: int
    user_id: int
    metric_type: str
    metric_value: int
    metric_data: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True
