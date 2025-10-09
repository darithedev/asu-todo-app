from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..models.task import Task, TaskResponse, TaskStatus, PriorityLevel, TaskCreate, TaskUpdate
from beanie import PydanticObjectId
from .auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks():
    """Get all tasks"""
    try:
        tasks = await Task.find_all().to_list()
        # Convert to response format manually
        return [TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            status=task.status,
            label_ids=[str(label_id) for label_id in task.label_ids],
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        ) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/user/{user_id}", response_model=List[TaskResponse])
async def get_user_tasks(user_id: str):
    """Get all tasks for a specific user"""
    try:
        tasks = await Task.find(Task.user_id == PydanticObjectId(user_id)).to_list()
        return [TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            status=task.status,
            label_ids=[str(label_id) for label_id in task.label_ids],
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        ) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user ID: {str(e)}")

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            status=task.status,
            label_ids=[str(label_id) for label_id in task.label_ids],
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )
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

# Authenticated Endpoints
@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new task for the current user"""
    try:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=current_user.id,
            priority=task_data.priority,
            deadline=task_data.deadline,
            status=task_data.status or TaskStatus.TODO,
            label_ids=[PydanticObjectId(x) for x in (task_data.label_ids or [])]
        )
        await task.insert()
        return TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            status=task.status,
            label_ids=[str(label_id) for label_id in task.label_ids],
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update fields on an existing task owned by the current user"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.deadline is not None:
            task.deadline = task_data.deadline
        if task_data.status is not None:
            task.status = task_data.status
            if task_data.status == TaskStatus.COMPLETED and task.completed_at is None:
                task.completed_at = task.deadline if task.deadline else task.created_at
        if task_data.label_ids is not None:
            task.label_ids = [PydanticObjectId(x) for x in task_data.label_ids]

        task.updated_at = task.updated_at  # keep existing updated_at or set explicitly elsewhere
        await task.save()

        return TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            status=task.status,
            label_ids=[str(label_id) for label_id in task.label_ids],
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a task owned by the current user"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")
        await task.delete()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")


@router.put("/{task_id}/labels", response_model=TaskResponse)
async def replace_task_labels(
    task_id: str,
    payload: dict,
    current_user: User = Depends(get_current_user)
):
    """Replace all labels on a task"""
    try:
        label_ids = payload.get("label_ids", [])
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        task.label_ids = [PydanticObjectId(x) for x in label_ids]
        await task.save()
        return TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            status=task.status,
            label_ids=[str(label_id) for label_id in task.label_ids],
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task labels: {str(e)}")


@router.post("/{task_id}/labels/{label_id}", response_model=TaskResponse)
async def add_task_label(
    task_id: str,
    label_id: str,
    current_user: User = Depends(get_current_user)
):
    """Add a single label to a task"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        pid = PydanticObjectId(label_id)
        if pid not in task.label_ids:
            task.label_ids.append(pid)
            await task.save()

        return TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            status=task.status,
            label_ids=[str(x) for x in task.label_ids],
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding label: {str(e)}")


@router.delete("/{task_id}/labels/{label_id}", response_model=TaskResponse)
async def remove_task_label(
    task_id: str,
    label_id: str,
    current_user: User = Depends(get_current_user)
):
    """Remove a single label from a task"""
    try:
        task = await Task.get(PydanticObjectId(task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        pid = PydanticObjectId(label_id)
        task.label_ids = [x for x in task.label_ids if x != pid]
        await task.save()

        return TaskResponse(
            id=str(task.id),
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            status=task.status,
            label_ids=[str(x) for x in task.label_ids],
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing label: {str(e)}")

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
