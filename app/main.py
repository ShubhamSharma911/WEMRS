from fastapi import FastAPI, Request
from passlib.context import CryptContext
from sqlalchemy import text
from contextlib import asynccontextmanager
from app.controllers import user_controller, auth_controller
from app.utils.logger import get_logger
from app.database.connection import get_connection
from app.database.seed_data import seed_data
import time
import os
from app.controllers import cap_controller


logger = get_logger("API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # e.g., /app
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Running schema.sql at startup...")

        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, "r") as f:
                schema_sql = f.read()

            with get_connection() as conn:
                raw_conn = conn.connection  # psycopg2 connection
                with raw_conn.cursor() as cur:
                    cur.execute(schema_sql)
                raw_conn.commit()

            logger.info("Database schema reset and recreated.")
        else:
            logger.error(f"Schema file not found at: {SCHEMA_PATH}")

        # Call all seeders from the centralized run_seeders
        seed_data()

    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)

    yield


# FastAPI app
app = FastAPI(title="WEMRS - Workforce Expense Management", lifespan=lifespan)


# Middleware to log each HTTP request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(
        f"{request.method} {request.url.path} | Status: {response.status_code} | Time: {duration:.2f}ms"
    )
    return response


# Register routers
app.include_router(user_controller.router)
app.include_router(auth_controller.router)
app.include_router(cap_controller.router)