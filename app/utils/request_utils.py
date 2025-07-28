from fastapi import Request, HTTPException

def get_current_user_id(request: Request) -> int:
    """
    Retrieve the current authenticated user's ID from the request state.
    Raises HTTP 401 if the user_id is not found.
    """
    user_id = getattr(request.state, "current_user_id", None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found in request state")
    return user_id
