from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Numeric, ForeignKey, Enum, DateTime, Date

from database import Base


class TransactionType(Enum):
    EXPENSE = "expense"
    INCOME = "income"
    
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)

    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    description: Mapped[str | None] = mapped_column(String)

    transaction_type: Mapped[TransactionType] = mapped_column(TransactionType, nullable=False)
    transaction_date: Mapped[Date] = mapped_column(Date, nullable=False)

    created_at: Mapped[Date] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Date] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped["Category"] = relationship("Category", back_populates="transactions")
    