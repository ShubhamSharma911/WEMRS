from app.repositories.user_repository import get_user_by_email_with_password
from app.security.hashing import verify_password
from app.utils.jwt_utils import create_access_token
from fastapi import HTTPException, status

def login_user(email: str, password: str):
    user = get_user_by_email_with_password(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token({
        "user_id": user["id"],
        "email": user["email"],
        "role": user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}
