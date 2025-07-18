import re
from fastapi import HTTPException

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PHONE_REGEX = r'^\+?\d{10,15}$'

def validate_email(email: str):
    """Validate email format."""
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

def validate_phone(phone: str):
    """Validate phone number format."""
    if not re.match(PHONE_REGEX, phone):
        raise HTTPException(status_code=400, detail="Invalid phone number format")
