from fastapi import FastAPI, Request
from sqlalchemy import text
from contextlib import asynccontextmanager
from app.controllers import user_controller, auth_controller
from app.utils.logger import get_logger
from app.database.connection import get_connection
from app.repositories import role_repository, emp_category_repository, user_repository
from app.security.hashing import get_password_hash
import time
import os

logger = get_logger("API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # 1. Drop and create tables from schema.sql
        logger.info("Running schema.sql at startup...")
        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, "r") as f:
                schema_sql = f.read()
            with get_connection() as conn:
                conn.execute(text(schema_sql))
                conn.commit()
            logger.info("Database schema reset and recreated.")
        else:
            logger.error(f"Schema file not found at: {SCHEMA_PATH}")

        # 2. Seed Roles
        roles = ["Superadmin", "Admin", "User"]
        for role in roles:
            if not role_repository.role_exists(role):
                role_repository.insert_role(role)

        # 3. Seed Employee Categories
        emp_categories = ["Class-1", "Class-2", "Class-3", "Class-4"]
        for cat in emp_categories:
            if not emp_category_repository.emp_category_exists(cat):
                emp_category_repository.insert_emp_category(cat)

        # 4. Seed Default Users
        defaults = [
            {"name": "Super Admin", "email": "shubham.sharma@sofmen.com", "role_name": "Superadmin", "phone": "9999999999"},
            {"name": "Admin", "email": "ssharma.sofmen@gmail.com", "role_name": "Admin", "phone": "8888888888"}
        ]

        hashed_password = get_password_hash("default")

        for user in defaults:
            # Get role_id for user
            with get_connection() as conn:
                role_id = conn.execute(
                    text("SELECT id FROM roles WHERE name = :name"),
                    {"name": user["role_name"]}
                ).scalar()

            # Check if user already exists
            existing_user = user_repository.get_user_by_email(user["email"])
            if not existing_user:
                user_repository.insert_user(
                    name=user["name"],
                    email=user["email"],
                    phone=user["phone"],
                    hashed_password=hashed_password,
                    role_id=role_id,
                    emp_cat_id=1  # Default to Class-1
                )

        logger.info("Default roles, categories, and users seeded successfully.")
    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)

    yield
    # Optional shutdown logic here

# FastAPI app
app = FastAPI(title="WEMRS - Workforce Expense Management", lifespan=lifespan)

# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} | Status: {response.status_code} | Time: {duration:.2f}ms")
    return response

# Register routers
app.include_router(user_controller.router)
app.include_router(auth_controller.router)
