from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="items")


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    
    brand_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    website_url = Column(String, nullable=False)

    prediction_data = Column(JSON, nullable=True)
    image = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="posts")
    
