from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field
from pydantic.types import ObjectId


class Label(Document):
    """
    Label model for task categorization.
    Each label belongs to a user and can be assigned to multiple tasks.
    """
    
    # Required fields
    name: str = Field(..., min_length=1, max_length=50, description="Label name (e.g., 'Work', 'Personal', 'Urgent')")
    user_id: ObjectId = Field(..., description="ID of the user who created this label")
    
    # Optional fields
    color: Optional[str] = Field(None, max_length=7, description="Hex color code for UI display (e.g., '#FF5733')")
    description: Optional[str] = Field(None, max_length=200, description="Optional description of the label")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Label creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Settings:
        name = "labels"  # MongoDB collection name
        indexes = [
            [("user_id", 1), ("name", 1)],  # Compound index: unique label name per user
        ]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            ObjectId: str
        }
    
    def __str__(self) -> str:
        return f"Label(id={self.id}, name={self.name}, user_id={self.user_id})"
    
    def __repr__(self) -> str:
        return self.__str__()


class LabelCreate(BaseModel):
    """Schema for label creation"""
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, max_length=7)
    description: Optional[str] = Field(None, max_length=200)


class LabelUpdate(BaseModel):
    """Schema for label updates"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, max_length=7)
    description: Optional[str] = Field(None, max_length=200)


class LabelResponse(BaseModel):
    """Schema for label data in API responses"""
    id: str
    name: str
    color: Optional[str]
    description: Optional[str]
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LabelWithTaskCount(LabelResponse):
    """Schema for label with task count information"""
    task_count: int = Field(0, description="Number of tasks using this label")
    
    class Config:
        from_attributes = True
