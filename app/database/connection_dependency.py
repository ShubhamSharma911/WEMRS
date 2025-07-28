# app/database/connection_dependency.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, future=True)

# This creates a factory for sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to use in routes
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


