from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, StringConstraints


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    first_name: Annotated[str, StringConstraints(min_length=1)]
    last_name: Annotated[str, StringConstraints(min_length=1)]

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        errors = []
        if len(password) < 8:
            errors.append("8 characters long")
        if not any(c.isupper() for c in password):
            errors.append("one uppercase letter")
        if not any(c.islower() for c in password):
            errors.append("one lowercase letter")
        if not any(c.isdigit() for c in password):
            errors.append("one number")

        if errors:
            raise ValueError(f"Password must have at least {', '.join(errors)}")
        
        return password
    
class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """Schema for returning user info."""
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
