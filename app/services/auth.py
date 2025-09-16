from enum import Enum
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.config import settings
from app.models.user import User

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
        secret_key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM,
    ):
        self.db = db
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, user_id: int) -> str:
        """Create short-lived JWT access token for authenticated users"""
        payload = self._create_payload(user_id, TokenType.ACCESS)
        return jwt.encode(payload, self.secret_key, self.algorithm)
    
    def create_refresh_token(self, user_id: int) -> str:
        """Create long-lived JWT refresh token for token renewal"""
        payload = self._create_payload(user_id, TokenType.REFRESH)
        return jwt.encode(payload, self.secret_key, self.algorithm)
    
    def verify_token(self, token: str) -> str:
        """Verify and decode the token"""
        try:
            payload = jwt.decode(token, self.secret_key, [self.algorithm])
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
            return user_id
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate the user with the email and password"""
        user = self.get_user_by_email(email)
        if not user or not user.is_active or not user.verify_password(password):
            return None
        return user

    def get_user_by_email(self, email: str) -> User:
        """Retrieve the user by the email"""
        return self.db.query(User).filter(User.email == email).first()

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
        
        