# Personal Finance Dashboard

A full-stack personal finance project for securely tracking each user's
transactions. The backend currently provides registration, JWT login, and
user-owned transaction endpoints. The next product milestone is a React
dashboard that turns those transactions into useful spending summaries.

## Why this project exists

The app is intended to be useful for personal spending tracking while also
demonstrating a production-style workflow: database migrations, automated
tests, continuous integration, containers, deployment, infrastructure as
code, and observability.

## Current stack

- FastAPI REST API
- PostgreSQL and SQLAlchemy
- Alembic database migrations
- JWT Bearer authentication
- Pytest integration tests
- GitHub Actions continuous integration
- React and Vite frontend scaffold

## Run the backend locally

Create and activate a virtual environment, then install the development
dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Create a PostgreSQL database:

```bash
createdb finance_app_v2
```

Copy the environment template and replace the example secret:

```bash
cp .env.example .env
openssl rand -hex 32
```

Set `DATABASE_URL` for your local PostgreSQL user and paste the generated value
into `SECRET_KEY`. Never commit `.env`.

Apply the database schema and start the API:

```bash
python -m alembic upgrade head
python -m uvicorn backend.main:app --reload
```

Open <http://127.0.0.1:8000/docs>. Register, log in, copy the returned access
token, select **Authorize**, and paste the token. Swagger adds the `Bearer`
prefix to authenticated requests.

## Run the tests

```bash
python -m pytest
```

The tests use an isolated in-memory database. They verify login, rejection of
unauthenticated requests, and the central ownership rule: one user cannot
list, read, or delete another user's transactions.

## Continuous integration

`.github/workflows/backend-ci.yml` starts PostgreSQL, applies every Alembic
migration to a clean database, and runs the backend tests for each pull
request and each push to `main`.

## Roadmap

1. Build the transaction dashboard and authentication screens in React.
2. Add Dockerfiles and Docker Compose for reproducible local development.
3. Deploy the application and PostgreSQL database.
4. Define cloud resources with Terraform.
5. Add structured logs, health monitoring, and a basic alert.
6. Integrate a financial-data provider after the manual transaction workflow
   is reliable.
