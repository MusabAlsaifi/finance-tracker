from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from services.user import UserService
from services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Depedency to get UserService"""
    return UserService(db)

def get_auth_service(
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    """Dependency to get AuthService"""
    return AuthService(user_service)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Dependency to get the currently authenticated user from JWT token"""
    payload = auth_service.verify_token(token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = user_service.get_user_by_id(int(user_id))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return user
