from fastapi import APIRouter, status, Request
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services import user_service
from app.utils.required_role import require_roles, require_self_or_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@require_roles(["ADMIN"])
def create_user(user: UserCreate, request: Request, user_id_from_token: int):
    return user_service.create_user_service(user)

@router.get("/", response_model=list[UserResponse])
@require_roles(["ADMIN"])
def get_users(request: Request, user_id_from_token: int):
    return user_service.get_all_users_service()

@router.get("/{user_id}", response_model=UserResponse)
@require_roles(["EMPLOYEE", "ADMIN", "SUPERADMIN"])  # just to require login
def get_user(user_id: int, request: Request, user_id_from_token: int):
    return user_service.get_user_by_id_service(user_id)

@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_self_or_admin()
def update_user(user_id: int, update_data: UserUpdate, request: Request, user_id_from_token: int):
    user_service.update_user_service(user_id, update_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_roles(["SUPERADMIN"])
def delete_user(user_id: int, request: Request, user_id_from_token: int):
    user_service.delete_user_service(user_id)

@router.put("/{user_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
@require_roles(["SUPERADMIN"])  # Only Superadmin can restore
def restore_user(user_id: int, request: Request, user_id_from_token: int):
    user_service.restore_user_service(user_id)
