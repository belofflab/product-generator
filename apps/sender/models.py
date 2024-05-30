from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Text, func, Integer, Boolean
from config.database import FastModel
from uuid import uuid4


class Template(FastModel):
    __tablename__ = "s_templates"

    id = Column(Integer, primary_key=True)
    image = Column(String(255), nullable=True)
    text = Column(String(4096), nullable=True)
    is_visible = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    