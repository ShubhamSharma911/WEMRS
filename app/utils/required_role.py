from fastapi import Request, HTTPException, status
from functools import wraps
import inspect
from app.utils.jwt_utils import decode_jwt_token

def require_roles(allowed_roles: list[str]):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                request: Request = _extract_request(args, kwargs)
                user_data = _verify_token(request, allowed_roles)
                kwargs["user_id_from_token"] = user_data["user_id"]
                return await func(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                request: Request = _extract_request(args, kwargs)
                user_data = _verify_token(request, allowed_roles)
                kwargs["user_id_from_token"] = user_data["user_id"]
                return func(*args, **kwargs)
            return sync_wrapper
    return decorator


def require_self_or_admin():
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                request: Request = _extract_request(args, kwargs)
                user_data = _verify_token(request, allowed_roles=["ADMIN", "SUPERADMIN", "EMPLOYEE"])
                user_id_from_token = user_data["user_id"]
                target_user_id = kwargs.get("user_id")
                if user_id_from_token != target_user_id and user_data["role"] not in ["ADMIN", "SUPERADMIN"]:
                    raise HTTPException(status_code=403, detail="You can only update your own profile")
                kwargs["user_id_from_token"] = user_id_from_token
                return await func(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                request: Request = _extract_request(args, kwargs)
                user_data = _verify_token(request, allowed_roles=["ADMIN", "SUPERADMIN", "EMPLOYEE"])
                user_id_from_token = user_data["user_id"]
                target_user_id = kwargs.get("user_id")
                if user_id_from_token != target_user_id and user_data["role"] not in ["ADMIN", "SUPERADMIN"]:
                    raise HTTPException(status_code=403, detail="You can only update your own profile")
                kwargs["user_id_from_token"] = user_id_from_token
                return func(*args, **kwargs)
            return sync_wrapper
    return decorator

def _extract_request(args, kwargs):
    request: Request = kwargs.get("request")
    if not request:
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
    if not request:
        raise HTTPException(status_code=400, detail="Request object not found")
    return request

def _verify_token(request: Request, allowed_roles: list[str]):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth.split(" ")[1]
    user_data = decode_jwt_token(token)
    if allowed_roles and user_data["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="Access denied for your role")
    return user_data
