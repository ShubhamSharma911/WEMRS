#app/repositories/emp_category_repository.py


from sqlalchemy import text
from app.database.connection import get_connection

def emp_category_exists(name: str):
    with get_connection() as conn:
        result = conn.execute(text("SELECT id FROM emp_categories WHERE name = :name"), {"name": name})
        return result.fetchone()

def insert_emp_category(name: str):
    with get_connection() as conn:
        conn.execute(text("INSERT INTO emp_categories (name) VALUES (:name)"), {"name": name})
        conn.commit()
