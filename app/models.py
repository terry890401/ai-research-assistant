from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default = lambda: datetime.now(timezone.utc))

class Research(Base):
    __tablename__ = "research"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(100), nullable=False)
    status = Column(String(20), default="pending")
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default = lambda: datetime.now(timezone.utc))