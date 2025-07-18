from sqlalchemy import text
from app.database.connection import get_connection

def role_exists(name: str):
    with get_connection() as conn:
        result = conn.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": name})
        return result.fetchone()

def insert_role(name: str):
    with get_connection() as conn:
        conn.execute(text("INSERT INTO roles (name) VALUES (:name)"), {"name": name})
        conn.commit()