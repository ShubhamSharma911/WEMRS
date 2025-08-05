#app/controllers/auth_controller.py

from fastapi import APIRouter
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    return auth_service.login_user(request.email, request.password)
