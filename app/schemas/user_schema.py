#app/shemas/user_schema.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, EmailStr
from app.models.user_enum import UserRole, EmpCategory

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: UserRole
    emp_category: EmpCategory

    @field_validator("role", "emp_category", mode="before")
    def normalize_enum(cls, v):
        if isinstance(v, str):
            return v.upper()
        return v



class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    emp_category: Optional[EmpCategory] = None

class UserUpdateResponse(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    role_id: Optional[int]
    emp_category_id: Optional[int]
    updated_at: datetime


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    emp_category: EmpCategory
