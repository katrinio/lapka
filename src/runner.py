import os

import uvicorn


def run() -> None:
    os.environ["DATABASE_URL"] = "sqlite:///echo.db"
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000)
