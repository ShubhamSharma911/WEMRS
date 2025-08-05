
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone, timedelta
from config import settings

def create_access_token(data: dict):
    to_encode = data.copy()

    # Normalize role if present
    if "role" in to_encode and isinstance(to_encode["role"], str):
        to_encode["role"] = to_encode["role"].upper()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_jwt_token(token: str):
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except ExpiredSignatureError:
        return None
    except JWTError:
        return None
