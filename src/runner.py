import uvicorn


def run() -> None:
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000)
