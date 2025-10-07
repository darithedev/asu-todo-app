from datetime import datetime
from typing import List, Optional
from enum import Enum
from beanie import Document
from pydantic import BaseModel, Field
from pydantic.types import ObjectId


class PriorityLevel(str, Enum):
    """Priority levels for tasks"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TaskStatus(str, Enum):
    """Task status options"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(Document):
    """
    Task model for the todo application.
    Each task belongs to a user and can have multiple labels.
    """
    
    # Required fields
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    user_id: ObjectId = Field(..., description="ID of the user who owns this task")
    priority: PriorityLevel = Field(..., description="Task priority level")
    deadline: datetime = Field(..., description="Task deadline (date and time)")
    
    # Optional fields
    description: Optional[str] = Field(None, max_length=1000, description="Detailed task description")
    status: TaskStatus = Field(TaskStatus.TODO, description="Current task status")
    label_ids: List[ObjectId] = Field(default_factory=list, description="List of label IDs assigned to this task")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Task creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Task completion timestamp")
    
    class Settings:
        name = "tasks"  # MongoDB collection name
        indexes = [
            "user_id",  # Index for user's tasks
            "status",   # Index for filtering by status
            "priority", # Index for filtering by priority
            "deadline", # Index for sorting by deadline
            [("user_id", 1), ("status", 1)],  # Compound index for user's tasks by status
            [("user_id", 1), ("deadline", 1)],  # Compound index for user's tasks by deadline
        ]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            ObjectId: str
        }
    
    def __str__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, status={self.status}, priority={self.priority})"
    
    def __repr__(self) -> str:
        return self.__str__()


class TaskCreate(BaseModel):
    """Schema for task creation"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: PriorityLevel
    deadline: datetime
    label_ids: List[str] = Field(default_factory=list, description="List of label IDs as strings")


class TaskUpdate(BaseModel):
    """Schema for task updates"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[PriorityLevel] = None
    deadline: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    label_ids: Optional[List[str]] = Field(None, description="List of label IDs as strings")


class TaskResponse(BaseModel):
    """Schema for task data in API responses"""
    id: str
    title: str
    description: Optional[str]
    priority: PriorityLevel
    deadline: datetime
    status: TaskStatus
    label_ids: List[str]
    user_id: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TaskWithLabels(TaskResponse):
    """Schema for task with label details"""
    labels: List[dict] = Field(default_factory=list, description="Full label objects")
    
    class Config:
        from_attributes = True


class TaskFilter(BaseModel):
    """Schema for filtering tasks"""
    status: Optional[TaskStatus] = None
    priority: Optional[PriorityLevel] = None
    label_ids: Optional[List[str]] = None
    deadline_from: Optional[datetime] = None
    deadline_to: Optional[datetime] = None
    search: Optional[str] = Field(None, description="Search in title and description")


class TaskStats(BaseModel):
    """Schema for task statistics"""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    tasks_by_priority: dict
    tasks_by_status: dict
