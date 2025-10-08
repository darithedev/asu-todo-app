from fastapi import APIRouter, HTTPException
from typing import List
from ..models.user import User, UserResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    """Get all users"""
    users = await User.find_all().to_list()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a specific user by ID"""
    try:
        user = await User.get(PydanticObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user ID: {str(e)}")

@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(username: str):
    """Get a user by username"""
    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
