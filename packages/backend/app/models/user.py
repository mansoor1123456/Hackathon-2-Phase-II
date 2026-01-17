from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(nullable=False)
    password_hash: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=UserRole.user)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    todos: List["Todo"] = Relationship(back_populates="user")


class UserRead(SQLModel):
    id: uuid.UUID
    email: str
    name: str
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserCreate(SQLModel):
    email: str
    name: str
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UserLogin(SQLModel):
    email: str
    password: str


class UserPublic(SQLModel):
    id: uuid.UUID
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime