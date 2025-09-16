from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


class UserService:
    """User Service"""
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user account"""
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        user.set_password(user_data.password)

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
        
    def update_user(self, user_id: int, user_data: dict) -> User:
        """Update user profile"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        allow_fields = ["first_name", "last_name"]
        for field in allow_fields:
            if field in update_data:
                setattr(user, field, user_data[field])

        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

    def deactivate_user(self, user_id: int) -> User:
        """Deactivate user account (soft delete)"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, details="User not found")
        
        user.is_active = False
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to deactivate user: {str(e)}")

    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve the user by the email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve the user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    # TODO: Schedule permanent user deletion
    # TODO: Change password
    # TODO: Get user profile
    # TODO: search users
    