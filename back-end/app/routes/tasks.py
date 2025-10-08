from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..models.task import Task, TaskResponse, TaskStatus, PriorityLevel
from beanie import PydanticObjectId

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks():
    """Get all tasks"""
    tasks = await Task.find_all().to_list()
    return tasks

@router.get("/user/{user_id}", response_model=List[TaskResponse])
async def get_user_tasks(user_id: str):
    """Get all tasks for a specific user"""
    try:
        tasks = await Task.find(Task.user_id == PydanticObjectId(user_id)).to_list()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user ID: {str(e)}")

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid task ID: {str(e)}")

@router.get("/user/{user_id}/status/{status}", response_model=List[TaskResponse])
async def get_user_tasks_by_status(user_id: str, status: TaskStatus):
    """Get tasks for a specific user filtered by status"""
    try:
        tasks = await Task.find(
            Task.user_id == PydanticObjectId(user_id),
            Task.status == status
        ).to_list()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")

@router.get("/user/{user_id}/priority/{priority}", response_model=List[TaskResponse])
async def get_user_tasks_by_priority(user_id: str, priority: PriorityLevel):
    """Get tasks for a specific user filtered by priority"""
    try:
        tasks = await Task.find(
            Task.user_id == PydanticObjectId(user_id),
            Task.priority == priority
        ).to_list()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {str(e)}")
