from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class User(Document):
    """
    User model for authentication and user management.
    Each user has a unique email and username for login.
    """
    
    # Required fields
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    hashed_password: str = Field(..., description="Hashed password for security")
    
    # Optional fields
    first_name: Optional[str] = Field(None, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=50, description="User's last name")
    phone_number: Optional[PhoneNumber] = Field(None, description="User's phone number")
    is_active: bool = Field(True, description="Whether the user account is active")
    is_verified: bool = Field(False, description="Whether the user's email is verified")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    
    class Settings:
        name = "users"  # MongoDB collection name
        indexes = [
            "email",  # Unique index on email
            "username",  # Unique index on username
        ]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"
    
    def __repr__(self) -> str:
        return self.__str__()


class UserCreate(BaseModel):
    """Schema for user registration/creation"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, description="Plain text password")
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[PhoneNumber] = None


class UserUpdate(BaseModel):
    """Schema for user profile updates"""
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[PhoneNumber] = None


class UserResponse(BaseModel):
    """Schema for user data in API responses (excludes sensitive fields)"""
    id: str
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True
