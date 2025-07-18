from pydantic import BaseModel
from app.models.user_enum import UserRole, EmpCategory

class UserCreate(BaseModel):
    name: str
    email: str
    password: str  # plain password input; will be hashed in service layer
    role: UserRole
    emp_category: EmpCategory

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None  # optional; if provided, will be hashed
    role: UserRole | None = None
    emp_category: EmpCategory | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    emp_category: EmpCategory
