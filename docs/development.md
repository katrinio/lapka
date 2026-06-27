## Development

### Install

```bash
poetry install
```

### Run

```bash
poetry run echo-run
```

Open the app at `http://127.0.0.1:8000`.
The app reads `.env` automatically through `pydantic-settings`.

The local database defaults to `echo.db` in the project root. Set `DATABASE_URL`
in the environment only when you need to override that behavior.

### Database

Apply migrations:

```bash
poetry run alembic upgrade head
```

Seed local data:

```bash
poetry run python scripts/seed_echo.py
```

Run this from the project root. If you are already inside `docs/`, the path is
`../scripts/seed_echo.py`.

If the database already has tables and you need to align Alembic with the current schema:

```bash
poetry run alembic stamp 4f1b2d9c7a11
```

### JS dependencies

```bash
npm install
```

### JS tests

```bash
npm run test:js        # run once
npm run test:js:watch  # watch mode
```

Tests live in `tests/js/`. They use [Vitest](https://vitest.dev/) with jsdom.

### Checks

```bash
# Python
poetry run pytest
poetry run ruff check src
poetry run mypy src
poetry run djlint src/templates --check

# JS
npm run test:js
npx stylelint "src/static/css/**/*.css"
npx eslint "src/static/js/**/*.js"
```
