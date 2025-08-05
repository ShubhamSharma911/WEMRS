
from sqlalchemy import text
from app.database.connection import get_connection
from app.models.user_enum import UserRole, EmpCategory
from app.utils.logger import get_logger

logger = get_logger("Initializer")

def seed_default_data():
    with get_connection() as conn:
        # Insert roles if not exists
        for role in UserRole:
            conn.execute(text("""
                INSERT INTO roles (name)
                VALUES (:name)
                ON CONFLICT (name) DO NOTHING
            """), {"name": role.value})

        # Insert employee categories if not exists
        for category in EmpCategory:
            conn.execute(text("""
                INSERT INTO emp_categories (name)
                VALUES (:name)
                ON CONFLICT (name) DO NOTHING
            """), {"name": category.value})

        conn.commit()
        logger.info("Default roles and emp_categories seeded successfully.")
