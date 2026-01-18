# MovieFlix CMS API — Deployment, Structure, and Usage Guide

This document complements the root `readme.md` (unchanged per your request) and focuses on installation, deployment, folder structure, and how to use the service.

## Folder Structure

```
movie-restapi/
├─ app/
│  ├─ api/
│  │  └─ routes/               # FastAPI routers (auth, users, movies, likes, health)
│  ├─ core/                    # App settings and security helpers
│  ├─ db/
│  │  ├─ models/               # SQLAlchemy ORM models
│  │  ├─ session.py            # Async engine + session dependency
│  │  └─ seed.py               # Optional seed script
│  ├─ middleware/              # JWT and structured logging middleware
│  ├─ schemas/                 # Pydantic request/response models
│  └─ main.py                  # FastAPI entrypoint
├─ docs/
│  ├─ README.md                # This file
│  └─ API_SPEC.md              # Endpoints summary
├─ tests/                      # Unit/integration tests
├─ .github/workflows/ci.yml    # CI pipeline (tests + Trivy scan)
├─ Dockerfile                  # Container image definition
├─ docker-compose.yml          # Local container orchestration
├─ requirements.txt            # Python dependencies
├─ pyproject.toml              # Tools config (ruff/black/pytest)
├─ .env.example                # Example environment variables
└─ readme.md                   # Original README (unchanged)
```

## Prerequisites
- Python 3.12+ (for local runs without Docker)
- Docker (optional but recommended)
- Git

## Configuration
Copy the example env and adjust if needed:

```powershell
Copy-Item .env.example .env
```

Environment variables:
- `DATABASE_URL` (default: `sqlite+aiosqlite:///./movieflix.db`)
- `JWT_SECRET` (change in production)
- `JWT_ALGORITHM` (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `60`)

## Install & Run (Local Python)

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Optional seed:

```powershell
python app/db/seed.py
```

## Docker (Single Container)

```powershell
docker build -t movieflix-api:dev .
docker run -p 8000:8000 --env-file .env.example movieflix-api:dev
```

## Docker Compose (Recommended)

```powershell
docker compose up --build
```

This publishes the API on `http://localhost:8000`.

## Healthcheck & Authentication
- Health: GET `http://localhost:8000/health`
- Signup: POST `http://localhost:8000/auth/signup` (JSON body per `UserCreate`)
- Login: POST `http://localhost:8000/auth/login?email=...&password=...` → returns JWT
- Protected routes require header: `Authorization: Bearer <token>`

See [docs/API_SPEC.md](docs/API_SPEC.md) for route details.

## Logging
Structured logging middleware emits entries with:
- `timestamp`: UTC ISO string
- `path`: request path
- `HttpMethodInvoked`: HTTP verb
- `logrequiredFieldsfromPayload`: parsed JSON body (if available)

## Security
- JWT middleware exempts `/auth/login`, `/auth/signup`, `/health`.
- For other routes, clients must include a valid bearer token.

## Testing
Run tests locally:

```powershell
pytest
```

CI runs automatically via GitHub Actions:
- Installs dependencies
- Runs `pip-audit` (advisory-only)
- Executes `pytest`
- Builds Docker image and scans it with Trivy

## Database & ORM
- Async SQLAlchemy engine with SQLite (aiosqlite driver)
- Models: `User`, `Movie`, `MoviesLiked` (field names match the original README)
- Tables are auto-created at startup for local/dev. Use Alembic for production migrations (not included by default).

## Common Workflows

- Create user and login:
  1. POST `/auth/signup` with `firstname`, `lastname`, `email`, `password`, `phonenumber`, `isPremiumUser`
  2. POST `/auth/login` with query params `email`, `password` → save `access_token`

- Create a movie:
  1. POST `/movies/` with body per `MovieCreate`
  2. Include header `Authorization: Bearer <token>`

- Like a movie:
  1. POST `/likes/` with `{ userid, movieid }` and bearer token
  2. GET `/likes/user/{userid}` to list likes (requires bearer token)

## Production Notes
- Change `JWT_SECRET` to a strong value.
- Consider Postgres/MySQL for production. Update `DATABASE_URL` accordingly.
- Replace auto-creation on startup with Alembic migrations.
- Configure observability (e.g., JSON logging to stdout, Application Insights).
- Harden Dockerfile (pin versions, use multi-stage builds).

## Troubleshooting
- If `pip install` is slow, use Docker to avoid local setup.
- Authorization errors → check bearer token header and token expiry.
- SQLite concurrency issues → consider a dedicated DB in production.
