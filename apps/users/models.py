from decimal import Decimal
from sqlalchemy import (
    Column,
    String,
    DateTime,
    BigInteger,
    Boolean,
    ForeignKey,
    Numeric,
    func
)
from sqlalchemy.orm import relationship
from config.database import FastModel
from config.settings import PRICE_PER_CARD


class User(FastModel):
    __tablename__ = "users"
    id: int = Column(BigInteger, primary_key=True)
    full_name: str = Column(String(1024), nullable=False, index=True)
    username: str = Column(String(255), nullable=True, index=True)
    balance: Decimal = Column(Numeric(12,2), nullable=False, default=PRICE_PER_CARD)
    freezed_balance: Decimal = Column(Numeric(12,2), nullable=False, default=0)
    
    is_active = Column(Boolean, nullable=False, default=True)
    is_subscribed = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    date_joined = Column(
        DateTime, nullable=False, server_default=func.now(), index=True
    )
    last_join = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )

    transactions = relationship("Transaction", back_populates="user", lazy="joined")


class Transaction(FastModel):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    amount = Column(Numeric(12,2), nullable=False)

    is_paid = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )

    user = relationship("User", back_populates="transactions", lazy="joined")