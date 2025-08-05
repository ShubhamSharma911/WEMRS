#app/utils/auth_dependency.py

from fastapi import Request, HTTPException, status, Depends
from app.utils.jwt_utils import decode_jwt_token
from app.utils.logger import get_logger

logger = get_logger("required_role")

def require_roles_dependency(allowed_roles: list[str]):
    def _role_checker(request: Request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            logger.warning("Missing or malformed Authorization header")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

        jwt_token = token[7:]  # remove "Bearer "
        try:
            payload = decode_jwt_token(jwt_token)
            role = payload.get("role")
            user_id = payload.get("user_id")

            if role is None or user_id is None:
                logger.error("Token payload missing required fields")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            if role not in allowed_roles:
                logger.warning(f"Access denied for role '{role}'. Allowed: {allowed_roles}")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

            request.state.current_user_id = user_id
            request.state.current_user_role = role

            logger.info(f"Access granted for user {user_id} with role {role}")
        except Exception as e:
            logger.error(f"Token decoding failed: {str(e)}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token decoding failed")

    return _role_checker