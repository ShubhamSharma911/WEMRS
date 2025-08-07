# app/services/upload_services.py

import os
import uuid
from datetime import datetime
from fastapi import UploadFile
from app.utils.file_utils import save_upload_file
from app.repositories.upload_repository import UploadRepository

class UploadService:
    def __init__(self, db):
        self.db = db
        self.upload_repository = UploadRepository(db)

    async def handle_upload(self, file: UploadFile, user_id: int, description: str = None) -> str:
        # Generate unique filename with extension
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}_{int(datetime.utcnow().timestamp())}{file_extension}"

        # Save file to disk, get relative path
        file_path = await save_upload_file(file, unique_filename)

        # Save metadata in DB (with default dummy values for now)
        self.upload_repository.save_file_record(
            user_id=user_id,
            file_path=file_path,         # e.g., "uploaded_receipts/abc123.jpg"
            expense_type_id=1,           # temporary default, update after OCR
            amount=0.0,                  # temporary default, update after OCR
            description=description
        )

        return unique_filename
