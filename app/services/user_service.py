#app/services/user_service.py

from fastapi import HTTPException
from passlib.context import CryptContext
import logging
from app.repositories import user_repository
from app.models.user_enum import UserRole, EmpCategory
from app.models.users import User
from app.schemas.user_schema import UserUpdate, UserUpdateResponse
from app.utils.user_data_verify import validate_email, validate_phone

logger = logging.getLogger("app.services.user_service")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user_service(user_data) -> User:
    validate_email(user_data.email)
    validate_phone(user_data.phone)

    role_id = user_repository.get_fk_id("roles", user_data.role.value)
    emp_cat_id = user_repository.get_fk_id("emp_categories", user_data.emp_category.value)
    if not role_id or not emp_cat_id:
        raise HTTPException(status_code=400, detail="Invalid role or emp_category")

    email = user_repository.get_user_by_email(user_data.email)
    if email:
        raise HTTPException(status_code=400, detail="Email already registered")

    phone = user_repository.get_user_by_phone(user_data.phone)
    if phone:
        raise HTTPException(status_code=400, detail="Phone already registered")

    hashed_pw = hash_password(user_data.password)
    user_id = user_repository.insert_user(user_data.name, user_data.email, user_data.phone, hashed_pw, role_id, emp_cat_id)

    return User(user_id, user_data.name, user_data.email, user_data.role, user_data.emp_category)

def get_all_users_service() -> list[User]:
    users = user_repository.get_all_users()
    return [
        User(
            id=u["id"],
            name=u["name"],
            email=u["email"],
            role=UserRole(u["role"]),
            emp_category=EmpCategory(u["emp_category"])
        )
        for u in users
    ]

def get_user_by_id_service(user_id: int) -> User:
    data = user_repository.get_user_by_id(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return User(data["id"], data["name"], data["email"], UserRole(data["role"]), EmpCategory(data["emp_category"]))





def update_user_service(user_id: int, update_data: UserUpdate) -> UserUpdateResponse:
    logger.info(f"Attempting to update user_id={user_id}")
    # Check if user exists and is not deleted
    user = user_repository.get_user_by_id(user_id)
    if not user:
        logger.warning(f"User {user_id} not found or is deleted")
        raise HTTPException(status_code=404, detail="User not found or is deleted")

    updates = {}
    if update_data.name is not None:
        updates["name"] = update_data.name
    if update_data.email is not None:
        validate_email(update_data.email)
        updates["email"] = update_data.email
    if update_data.phone is not None:
        validate_phone(update_data.phone)
        updates["phone"] = update_data.phone
    if update_data.password is not None:
        updates["hashed_password"] = hash_password(update_data.password)
    if update_data.role is not None:
        updates["role_id"] = user_repository.get_fk_id("roles", update_data.role.value)
    if update_data.emp_category is not None:
        updates["emp_category_id"] = user_repository.get_fk_id("emp_categories", update_data.emp_category.value)

    if not updates:
        logger.warning(f"No valid fields provided to update for user_id={user_id}")
        raise HTTPException(status_code=400, detail="No valid fields to update")

    logger.debug(f"Update fields: {updates}")
    updated_user = user_repository.update_user(user_id, updates)
    if updated_user is None:
        logger.warning(f"Failed to update user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found or update failed")

    logger.info(f"User user_id={user_id} successfully updated")
    return UserUpdateResponse(**updated_user)

def delete_user_service(user_id: int) -> None:
    if not user_repository.get_user_by_id(user_id):
        raise HTTPException(status_code=404, detail="User not found or already deleted")
    user_repository.delete_user(user_id)

def restore_user_service(user_id: int) -> None:
    user = user_repository.get_user_by_id(user_id)
    if user:
        raise HTTPException(status_code=400, detail="User is already active")
    if not user_repository.user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    user_repository.restore_user(user_id)
