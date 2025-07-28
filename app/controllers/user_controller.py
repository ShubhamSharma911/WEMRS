from fastapi import APIRouter, status, Request, Body
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services import user_service
from app.utils import logger
from app.utils.logger import get_logger
from app.utils.required_role import require_roles, require_self_or_admin
from app.utils.request_utils import get_current_user_id
from app.models.user_enum import UserRole, EmpCategory
import logging


router = APIRouter(prefix="/users", tags=["Users"])

logger = get_logger("user_controller")

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@require_roles(["ADMIN", "SUPERADMIN"])
def create_user(user: UserCreate, request: Request):
    current_user_id = get_current_user_id(request)
    return user_service.create_user_service(user)

@router.get("/", response_model=list[UserResponse])
@require_roles([UserRole.ADMIN,UserRole.SUPERADMIN,UserRole.EMPLOYEE])
def get_users(request: Request):
    return user_service.get_all_users_service()

@router.get("/{user_id}", response_model=UserResponse)
@require_roles(["EMPLOYEE", "ADMIN", "SUPERADMIN"])  # Just to require login
def get_user(user_id: int, request: Request):
    current_user_id = get_current_user_id(request)
    return user_service.get_user_by_id_service(user_id)


@router.post("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
@require_self_or_admin()
def update_user(
    user_id: int,
    request: Request,
    update_data: UserUpdate = Body(...)
):
    logger.info(f"POST /users/{user_id} called by user_id={getattr(request.state, 'current_user_id', 'unknown')}")
    user_service.update_user_service(user_id, update_data)
    logger.info(f"User {user_id} update completed")
    return user_service.get_user_by_id_service(user_id)




@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_roles(["SUPERADMIN"])
def delete_user(user_id: int, request: Request):
    user_service.delete_user_service(user_id)


@router.put("/{user_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
@require_roles(["SUPERADMIN"])  # Only Superadmin can restore
def restore_user(user_id: int, request: Request):
    user_service.restore_user_service(user_id)
