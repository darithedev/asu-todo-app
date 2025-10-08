from fastapi import APIRouter, HTTPException
from typing import List
from ..models.user import User, UserResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/test")
async def test_users():
    """Test endpoint to debug"""
    try:
        # Test basic import
        from ..models.user import User
        return {"message": "User model imported successfully"}
    except Exception as e:
        return {"error": f"Import error: {str(e)}"}

@router.get("/test-db")
async def test_database():
    """Test database connection"""
    try:
        from ..models.user import User
        # Try a simple count query
        count = await User.count()
        return {"message": f"Database connection successful, found {count} users"}
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}

@router.get("/raw")
async def get_users_raw():
    """Get users without response model"""
    try:
        users = await User.find_all().to_list()
        # Convert to dict manually
        return [user.dict() for user in users]
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}

@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    """Get all users"""
    try:
        users = await User.find_all().to_list()
        # Convert to response format manually
        return [UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        ) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a specific user by ID"""
    try:
        user = await User.get(PydanticObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user ID: {str(e)}")

@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(username: str):
    """Get a user by username"""
    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login
    )
