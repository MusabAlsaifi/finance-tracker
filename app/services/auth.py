from enum import Enum
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from config import settings
from models.user import User
from services.user import UserService


class TokenType(str, Enum):
    """JWT token types used in authentication"""
    ACCESS = "access"
    REFRESH = "refresh"

    def ttl_minutes(self):
        """Get time-to-live for the token type"""
        if self is TokenType.ACCESS:
            return settings.ACCESS_TOKEN_EXPIRE_MINUTES
        if self is TokenType.REFRESH:
            return settings.REFRESH_TOKEN_EXPIRE_MINUTES

class AuthService:
    """Authentication service"""
    def __init__(
        self, 
        db: Session,
        user_service: UserService,
        secret_key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM,
    ):
        self.db = db
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.user_service = user_service

    def create_access_token(self, user_id: int) -> str:
        """Create short-lived JWT access token for authenticated users"""
        payload = self._create_payload(user_id, TokenType.ACCESS)
        return jwt.encode(payload, self.secret_key, self.algorithm)
    
    def create_refresh_token(self, user_id: int) -> str:
        """Create long-lived JWT refresh token for token renewal"""
        payload = self._create_payload(user_id, TokenType.REFRESH)
        return jwt.encode(payload, self.secret_key, self.algorithm)
    
    def verify_token(self, token: str) -> dict:
        """Verify and decode the token"""
        try:
            payload = jwt.decode(token, self.secret_key, [self.algorithm])
            if not payload.get("sub"):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
    def authenticate_user(self, email: str, password: str) -> User | None:
        """Authenticate the user with the email and password"""
        user = self.user_service.get_user_by_email(email)
        if not user or not user.is_active or not user.verify_password(password):
            return None
        return user

    def _create_payload(self, user_id: int, token_type: TokenType) -> dict:
        """Create JWT payload"""
        current_time = datetime.utcnow()
        expire = current_time + timedelta(minutes=token_type.ttl_minutes)
        return {
            "sub": str(user_id),
            "exp": expire,
            "iat": current_time,
            "type": token_type
        }
        
        