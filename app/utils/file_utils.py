#app.utils.file_utils.py

import os
from fastapi import UploadFile

UPLOAD_DIR = "uploaded_receipts"

async def save_upload_file(file: UploadFile, filename: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    full_path = os.path.join(UPLOAD_DIR, filename)

    with open(full_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return full_path
