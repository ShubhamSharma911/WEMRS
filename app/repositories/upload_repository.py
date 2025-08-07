# app/repositories/upload_repository.py

from sqlalchemy import text

class UploadRepository:
    def __init__(self, db):
        self.db = db

    def save_file_record(self, user_id: int, file_path: str, expense_type_id: int = 1, amount: float = 0.0, description: str = None):
        query = text("""
            INSERT INTO expense_receipts (
                user_id,
                expense_type_id,
                amount,
                receipt_file_path,
                description,
                uploaded_at,
                updated_at
            )
            VALUES (
                :user_id,
                :expense_type_id,
                :amount,
                :receipt_file_path,
                :description,
                NOW(),
                NOW()
            )
        """)
        self.db.execute(query, {
            "user_id": user_id,
            "expense_type_id": expense_type_id,
            "amount": amount,
            "receipt_file_path": file_path,
            "description": description
        })
        self.db.commit()
