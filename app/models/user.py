from passlib.context import CryptContext
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, Boolean, DateTime

from database import Base

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    default="pbkdf2_sha256",
    deprecated="auto"
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    categories: Mapped[list["Category"]] = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        """Hash and store password"""
        # TODO: Password strength check
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return pwd_context.verify(password, self.password_hash)
