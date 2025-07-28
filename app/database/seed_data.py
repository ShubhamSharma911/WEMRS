# app/database/seed_data.py

from sqlalchemy import text
from app.database.connection import get_connection
from app.repositories import role_repository, emp_category_repository, user_repository
from app.security.hashing import get_password_hash
from app.utils.logger import get_logger

logger = get_logger("Seeder")

def seed_roles():
    roles = ["SUPERADMIN", "ADMIN", "EMPLOYEE"]
    for role in roles:
        if not role_repository.role_exists(role):
            role_repository.insert_role(role)

def seed_emp_categories():
    emp_categories = ["CLASS_1", "CLASS_2", "CLASS_3", "CLASS_4"]
    for cat in emp_categories:
        if not emp_category_repository.emp_category_exists(cat):
            emp_category_repository.insert_emp_category(cat)

def seed_expense_types():
    expense_types = ["TRAVEL", "FOOD", "LODGING", "MISC"]
    with get_connection() as conn:
        for expense in expense_types:
            existing = conn.execute(
                text("SELECT 1 FROM expense_types WHERE name = :name"),
                {"name": expense}
            ).fetchone()
            if not existing:
                conn.execute(
                    text("INSERT INTO expense_types (name) VALUES (:name)"),
                    {"name": expense}
                )
        conn.commit()

def seed_expense_statuses():
    statuses = ["PENDING", "APPROVED", "REJECTED"]
    with get_connection() as conn:
        for status in statuses:
            exists = conn.execute(
                text("SELECT 1 FROM expense_status WHERE name = :name"),
                {"name": status}
            ).fetchone()
            if not exists:
                conn.execute(
                    text("INSERT INTO expense_status (name) VALUES (:name)"),
                    {"name": status}
                )
        conn.commit()

def seed_users():
    defaults = [
        {
            "name": "Super Admin",
            "email": "shubham.sharma@sofmen.com",
            "role_name": "SUPERADMIN",
            "phone": "9691599915"
        },
        {
            "name": "Admin",
            "email": "ssharma.sofmen@gmail.com",
            "role_name": "ADMIN",
            "phone": "8962336802"
        },
        {
            "name": "test_user1",
            "email": "test_user1@gmail.com",
            "role_name": "EMPLOYEE",
            "phone": "9691599916"
        },
        {
            "name": "test_user2",
            "email": "test_user2@gmail.com",
            "role_name": "EMPLOYEE",
            "phone": "9691599917"
        },
        {
            "name": "test_user3",
            "email": "test_user3@gmail.com",
            "role_name": "EMPLOYEE",
            "phone": "9691599918"
        }
    ]

    hashed_password = get_password_hash("default")

    for user in defaults:
        with get_connection() as conn:
            role_id = conn.execute(
                text("SELECT id FROM roles WHERE name = :name"),
                {"name": user["role_name"]}
            ).scalar()
            emp_cat_id = conn.execute(
                text("SELECT id FROM emp_categories WHERE name = 'CLASS_1'")
            ).scalar()

        existing_user = user_repository.get_user_by_email(user["email"])
        if not existing_user:
            user_repository.insert_user(
                name=user["name"],
                email=user["email"],
                phone=user["phone"],
                hashed_password=hashed_password,
                role_id=role_id,
                emp_cat_id=emp_cat_id
            )

def run_seeders():
    try:
        seed_roles()
        seed_emp_categories()
        seed_expense_types()
        seed_expense_statuses()
        seed_users()
        logger.info("Seeding completed successfully.")
    except Exception as e:
        logger.error(f"Error while running seeders: {e}", exc_info=True)
