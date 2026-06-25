## Setup

```bash
poetry install
poetry run alembic upgrade head
poetry run uvicorn src.app:app --reload
```

If tables were already created before running migrations:

```bash
poetry run alembic stamp 4f1b2d9c7a11
```
