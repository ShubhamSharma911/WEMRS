from sqlalchemy import text
from app.database.connection import get_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Tables allowed for FK lookups
ALLOWED_FK_TABLES = {"roles", "emp_categories"}

# ----------------------------
# FK ID Fetch Helper
# ----------------------------
def get_fk_id(table: str, name: str):
    logger.debug(f"Fetching FK ID for {table} with name={name}")
    if table not in ALLOWED_FK_TABLES:
        logger.error(f"Invalid FK table: {table}")
        raise ValueError("Invalid table name for FK lookup")
    with get_connection() as conn:
        result = conn.execute(
            text(f"SELECT id FROM {table} WHERE name = :name"),
            {"name": name}
        ).fetchone()
        return result[0] if result else None

# ----------------------------
# Insert & CRUD for Users
# ----------------------------
def insert_user(name: str, email: str, phone: str, hashed_password: str, role_id: int, emp_cat_id: int):
    logger.info(f"Inserting user: {email}")
    with get_connection() as conn:
        result = conn.execute(
            text("""
                INSERT INTO users (name, email, phone, hashed_password, role_id, emp_category_id)
                VALUES (:name, :email, :phone, :hashed_password, :role_id, :emp_cat_id)
                RETURNING id
            """),
            {
                "name": name,
                "email": email,
                "phone": phone,
                "hashed_password": hashed_password,
                "role_id": role_id,
                "emp_cat_id": emp_cat_id
            }
        )
        conn.commit()
        user_id = result.fetchone()[0]
        logger.info(f"User inserted with ID: {user_id}")
        return user_id

def get_user_by_id(user_id: int):
    logger.debug(f"Fetching user by ID: {user_id}")
    with get_connection() as conn:
        result = conn.execute(text("""
            SELECT u.id, u.name, u.email, u.phone, r.name AS role, c.name AS emp_category
            FROM users u
            JOIN roles r ON u.role_id = r.id
            JOIN emp_categories c ON u.emp_category_id = c.id
            WHERE u.id = :user_id AND u.is_deleted = FALSE
        """), {"user_id": user_id}).fetchone()
        return dict(result._mapping) if result else None

def get_all_users():
    logger.debug("Fetching all users (excluding deleted)")
    with get_connection() as conn:
        result = conn.execute(text("""
            SELECT u.id, u.name, u.email, u.phone, r.name AS role, c.name AS emp_category
            FROM users u
            JOIN roles r ON u.role_id = r.id
            JOIN emp_categories c ON u.emp_category_id = c.id
            WHERE u.is_deleted = FALSE
        """)).fetchall()
        return [dict(row._mapping) for row in result]

def update_user(user_id: int, updates: dict):
    logger.info(f"Updating user {user_id} with fields: {list(updates.keys())}")
    set_clause = ", ".join([f"{key} = :{key}" for key in updates.keys()])
    updates["user_id"] = user_id
    with get_connection() as conn:
        conn.execute(text(f"UPDATE users SET {set_clause}, updated_at = NOW() WHERE id = :user_id"), updates)
        conn.commit()

def soft_delete_user(user_id: int):
    logger.warning(f"Soft deleting user: {user_id}")
    with get_connection() as conn:
        conn.execute(text("""
            UPDATE users SET is_deleted = TRUE, deleted_at = NOW() WHERE id = :user_id
        """), {"user_id": user_id})
        conn.commit()

def restore_user(user_id: int):
    logger.info(f"Restoring user: {user_id}")
    with get_connection() as conn:
        conn.execute(text("""
            UPDATE users SET is_deleted = FALSE, deleted_at = NULL WHERE id = :user_id
        """), {"user_id": user_id})
        conn.commit()

# ----------------------------
# Seeding Helpers for Roles & Emp Categories
# ----------------------------
def insert_role_if_not_exists(role_name: str):
    with get_connection() as conn:
        conn.execute(text("""
            INSERT INTO roles (name) VALUES (:name)
            ON CONFLICT (name) DO NOTHING
        """), {"name": role_name})
        conn.commit()

def insert_emp_category_if_not_exists(category_name: str):
    with get_connection() as conn:
        conn.execute(text("""
            INSERT INTO emp_categories (name) VALUES (:name)
            ON CONFLICT (name) DO NOTHING
        """), {"name": category_name})
        conn.commit()

def get_user_by_email(email: str):
    with get_connection() as conn:
        result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email})
        return result.fetchone()


def get_user_by_email_with_password(email: str):
    with get_connection() as conn:
        result = conn.execute(text("""
            SELECT u.id, u.email, u.hashed_password, r.name AS role
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.email = :email AND u.is_deleted = FALSE
        """), {"email": email}).fetchone()
        return dict(result._mapping) if result else None
