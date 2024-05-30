from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    BigInteger,
    Integer,
    Boolean,
    Unicode,
    Float,
    ForeignKey,
    LargeBinary,
    Numeric,
)
from decimal import Decimal
from config.database import FastModel
from uuid import uuid4
from sqlalchemy.orm import relationship


class APSchedulerJob(FastModel):
    __tablename__ = "apscheduler_jobs"
    __table_args__ = {"info": {"skip_autogenerate": True}}

    id = Column(Unicode(191), primary_key=True)
    next_run_time = Column(Float(25), index=True)
    job_state = Column(LargeBinary, nullable=False)


class User(FastModel):
    __tablename__ = "users"
    id: int = Column(BigInteger, primary_key=True)
    full_name: str = Column(String(1024), nullable=False, index=True)
    username: str = Column(String(255), nullable=True, index=True)
    balance: Decimal = Column(Numeric(12,2), nullable=False, default=0)
    
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