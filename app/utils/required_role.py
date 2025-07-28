from fastapi import Request, HTTPException, status
from functools import wraps
import inspect
from app.utils.jwt_utils import decode_jwt_token
from app.utils.logger import get_logger

logger = get_logger("required_role")

def require_roles(allowed_roles: list[str]):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                request = _extract_request(args, kwargs)
                _verify_token_and_roles(request, allowed_roles)
                return await func(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                request = _extract_request(args, kwargs)
                _verify_token_and_roles(request, allowed_roles)
                return func(*args, **kwargs)
            return sync_wrapper
    return decorator


def require_self_or_admin():
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                request = _extract_request(args, kwargs)
                logger.info("require_self_or_admin: checking permissions")

                user_data = _verify_token_and_roles(request, allowed_roles=["ADMIN", "SUPERADMIN", "EMPLOYEE"])
                print("user_data", user_data)
                target_user_id = int(kwargs.get("user_id"))
                print("target_user_id", target_user_id)

                logger.debug(f"Authenticated user_id={user_data['user_id']} with role={user_data['role']}, target_user_id={target_user_id}")

                if user_data["user_id"] != target_user_id and user_data["role"].upper() not in ["ADMIN", "SUPERADMIN"]:
                    logger.warning(f"Permission denied. Authenticated user_id={user_data['user_id']} tried updating user_id={target_user_id}")
                    raise HTTPException(status_code=403, detail="You can only update your own profile")

                logger.info(f"Permission granted to user_id={user_data['user_id']} for updating user_id={target_user_id}")
                return await func(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                request = _extract_request(args, kwargs)
                user_data = _verify_token_and_roles(request, allowed_roles=["ADMIN", "SUPERADMIN", "EMPLOYEE"])
                target_user_id = int(kwargs.get("user_id"))

                logger.debug(f"Authenticated user_id={user_data['user_id']} with role={user_data['role']}, target_user_id={target_user_id}")

                if user_data["user_id"] != target_user_id and user_data["role"].upper() not in ["ADMIN", "SUPERADMIN"]:
                    logger.warning(f"Permission denied. Authenticated user_id={user_data['user_id']} tried updating user_id={target_user_id}")
                    raise HTTPException(status_code=403, detail="You can only update your own profile")

                logger.info(f"Permission granted to user_id={user_data['user_id']} for updating user_id={target_user_id}")
                return func(*args, **kwargs)
            return sync_wrapper
    return decorator



def _extract_request(args, kwargs) -> Request:
    request = kwargs.get("request")
    if not request:
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
    if not request:
        raise HTTPException(status_code=400, detail="Request object not found")
    return request


def _verify_token_and_roles(request: Request, allowed_roles: list[str]):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth.split(" ")[1]
    user_data = decode_jwt_token(token)

    request.state.current_user_id = user_data["user_id"]  # Save user ID for logging or DB ops

    if allowed_roles and user_data["role"].upper() not in [r.upper() for r in allowed_roles]:
        raise HTTPException(status_code=403, detail="Access denied for your role")

    return user_data
