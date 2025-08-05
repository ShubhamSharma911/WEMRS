#app/services/receipt_service.py
import os
from fastapi import UploadFile,File
from sqlalchemy.orm import Session


async def handle_receipt_upload(
        db: Session,
        user_id: int,
        expense_type_id: int,
        amount: float,
        description: str,
        file: UploadFile = File(...)

):
        try:
            # Create folder if not exists
            os.makedirs("./receipts", exist_ok=True)

            #Unique filename 

