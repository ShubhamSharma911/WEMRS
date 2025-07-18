from sqlalchemy import text
from app.db.connection import get_connection
from app.models.enums import UserRole, EmpCategory

def seed_roles_and_categories():
    with get_connection() as conn:
        for role in UserRole.list():
            conn.execute(
                text("INSERT INTO roles (name) VALUES (:name) ON CONFLICT DO NOTHING"),
                {"name": role}
            )

        for category in EmpCategory.list():
            conn.execute(
                text("INSERT INTO emp_categories (name) VALUES (:name) ON CONFLICT DO NOTHING"),
                {"name": category}
            )

        conn.commit()
        print("✅ Roles and Emp Categories seeded.")

if __name__ == "__main__":
    seed_roles_and_categories()
