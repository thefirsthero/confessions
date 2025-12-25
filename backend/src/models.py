from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConfessionCreate(BaseModel):
    """Model for creating a new confession"""
    confession: str
    location: str

class Confession(BaseModel):
    """Model for a confession with all fields"""
    id: int
    confession: str
    location: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
