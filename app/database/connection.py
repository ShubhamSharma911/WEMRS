#app/database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, future=True)

def get_connection() -> Connection:
    return engine.connect()
