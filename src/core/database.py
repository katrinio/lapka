import os
from pathlib import Path

from sqlalchemy import create_engine

ROOT = Path(__file__).parent.parent.parent
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///echo.db")
print(f"DATABASE_URL={DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

