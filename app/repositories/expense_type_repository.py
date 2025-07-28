from sqlalchemy import text
from app.database.connection import get_connection

def insert_expense_type(name: str):
    with get_connection() as conn:
        conn.execute(
            text("INSERT INTO expense_types (name) VALUES (:name)"),
            {"name": name}
        )
        conn.commit()

def expense_type_exists(name: str) -> bool:
    with get_connection() as conn:
        result = conn.execute(
            text("SELECT 1 FROM expense_types WHERE name = :name"),
            {"name": name}
        )
        return result.scalar() is not None
