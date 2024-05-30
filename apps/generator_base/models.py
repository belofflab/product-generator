from config.database import FastModel
from sqlalchemy import Column, ForeignKey, String, Boolean, Text, DateTime, BigInteger, Numeric, func


class UserCard(FastModel):
    __tablename__="user_cards"
    id = Column(BigInteger, primary_key = True)
    user_id = Column(ForeignKey("users.id"), nullable = False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    description_seo = Column(Text, nullable=True)
    size = Column(String(125), nullable=False)    
    is_visible= Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), index=True) 