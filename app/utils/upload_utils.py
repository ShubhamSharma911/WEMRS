import os
from datetime import datetime
from uuid import uuid4


def generate_upload_path(extension: str, base_dir: str = "uploads") -> str:
    """
    Generate a unique file path like: uploads/2025/08/05/20250805110018_uuid.jpeg
    """

    unique_id = uuid4().hex
    timestamp = datetime.now()
    date_path =  timestamp.strftime("%Y/%m/%d")
    filename = f"{timestamp.strftime('%Y%m%d%H%M%S')}_{unique_id}.{extension}"
    full_path = os.path.join(base_dir, date_path)

    os.makedirs(full_dir, exist_ok=True)
    return os.path.join(full_path, filename)