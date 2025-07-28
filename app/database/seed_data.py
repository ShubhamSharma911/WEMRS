# app/database/seed_data.py
from passlib.context import CryptContext
from sqlalchemy import text
from passlib.hash import bcrypt
from app.database.connection import get_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def seed_data():
    with get_connection() as conn:
        print("Seeding roles...")
        roles = ["EMPLOYEE", "ADMIN", "SUPERADMIN"]
        for role in roles:
            conn.execute(
                text("INSERT INTO roles (name) VALUES (:name) ON CONFLICT (name) DO NOTHING"),
                {"name": role}
            )

        print("Seeding employee categories...")
        categories = ["CLASS_1", "CLASS_2", "CLASS_3", "CLASS_4"]
        for cat in categories:
            conn.execute(
                text("INSERT INTO emp_categories (name) VALUES (:name) ON CONFLICT (name) DO NOTHING"),
                {"name": cat}
            )

        print("Seeding expense statuses...")
        statuses = ["PENDING", "APPROVED", "REJECTED", "REIMBURSED"]
        for status in statuses:
            conn.execute(
                text("INSERT INTO expense_statuses (name) VALUES (:name) ON CONFLICT (name) DO NOTHING"),
                {"name": status}
            )

        print("Seeding expense types...")
        expense_types = [
            {"name": "TRAVEL"},
            {"name": "FOOD"},
            {"name": "HOTEL"},
            {"name": "OTHER"}
        ]
        for et in expense_types:
            conn.execute(
                text("INSERT INTO expense_types (name) VALUES (:name) ON CONFLICT (name) DO NOTHING"),
                et
            )

        print("Seeding default users...")
        default_users = [
            {
                "name": "Default Employee",
                "email": "employee@example.com",
                "phone": "9999999991",
                "role": "EMPLOYEE",
                "category": "CLASS_1"
            },
            {
                "name": "Default Admin",
                "email": "admin@example.com",
                "phone": "9999999992",
                "role": "ADMIN",
                "category": "CLASS_2"
            },
            {
                "name": "Default SuperAdmin",
                "email": "superadmin@example.com",
                "phone": "9999999993",
                "role": "SUPERADMIN",
                "category": "CLASS_3"
            }
        ]

        for user in default_users:
            # Fetch role and category IDs
            role_result = conn.execute(
                text("SELECT id FROM roles WHERE name = :name"),
                {"name": user["role"]}
            ).fetchone()

            cat_result = conn.execute(
                text("SELECT id FROM emp_categories WHERE name = :name"),
                {"name": user["category"]}
            ).fetchone()

            if not role_result or not cat_result:
                print(f"Skipping user {user['email']} due to missing role/category.")
                continue

            hashed_pwd = bcrypt.hash("password@123")

            conn.execute(
                text("""
                    INSERT INTO users (name, email, phone, hashed_password, role_id, emp_category_id)
                    VALUES (:name, :email, :phone, :hashed_password, :role_id, :category_id)
                    ON CONFLICT (email) DO NOTHING
                """),
                {
                    "name": user["name"],
                    "email": user["email"],
                    "phone": user["phone"],
                    "hashed_password": hashed_pwd,
                    "role_id": role_result.id,
                    "category_id": cat_result.id
                }
            )
        conn.commit()
        print("Seed data committed.")
