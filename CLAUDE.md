# Sports Management System — Development Guide

## Overview
High-integrity system for managing sports championships (leagues, tournaments, knockout stages).

**Stack:**
- **Backend:** Python 3.13+, FastAPI 0.104.1, PostgreSQL, SQLModel/SQLAlchemy 2.0.23
- **Frontend:** React 20.0.0, TypeScript, Vite, Tailwind CSS 3.4.1, React Router 7.x
- **DevOps:** Docker, Docker Compose (local), PostgreSQL container

## Architecture and Design

### Backend (Hexagonal Architecture)
The system core is isolated from IO and frameworks.
- **Domain:** Pure entities (`User`, `Championship`, `Team`, `Player`, `Match`). No external dependencies.
- **Application:** Use Cases and **Ports** (ABC Interfaces) for abstraction.
- **Adapters:** 
  - **Repositories:** SQLModel/SQLAlchemy for persistence
  - **Controllers:** FastAPI routers with Pydantic schemas
  - **Auth:** JWT with python-jose, password hashing with pwdlib

### Frontend (Clean Architecture + Atomic Design)
- **Domain:** TypeScript types, interfaces, and validations.
- **Services:** Centralized API client in `services/api.js`, native fetch with JWT interception.
- **UI/Components:** Reusable atomic components (Button, FormInput, Card, Table, Modal, Header).
- **State Management:** React Context for authentication, localStorage for JWT tokens.
- **Routing:** React Router with ProtectedRoute for access control.

## 🛠️ Mandatory Principles

1. **DDD (Domain-Driven Design):** Consistent ubiquitous language. Entities manage state, not tables. Use case = pure domain.
2. **TDD (Test-Driven Development):** **Red-Green-Refactor** cycle. 
   - **Prohibited:** Production code without corresponding test.
   - **Back:** `pytest` (pytest-asyncio for async), fixtures for DB, mocks for Auth.
   - **Front:** `Vitest` + `Testing Library`, behavior tests (user interactions).
3. **Clean Code:** SRP, semantic names, strong TypeScript types, zero obvious comments.
4. **Layer Isolation:** Domain doesn't access DB directly, Pydantic schemas isolate DTO from Entity, API client isolated in `services/`.
5. **Exact Versioning:** Locked dependencies in `poetry.lock` and `package-lock.json`, no `~` or `^` in production.

## Folder Structure

```text
/
├── backend/
│   ├── app/
│   │   ├── domain/           # Entities and Rules (User, Championship, Team, Player, Match)
│   │   ├── application/      # Use Cases and Ports (ABC interfaces)
│   │   ├── adapters/
│   │   │   ├── repositories/ # SQLModel/SQLAlchemy repositories
│   │   │   ├── routers/      # FastAPI routers (auth, championships, matches, players)
│   │   │   └── schemas.py    # Pydantic DTOs (Create, Update, Public, Full)
│   │   ├── auth.py           # JWT, password hashing (pwdlib), oauth2_scheme
│   │   ├── dependencies.py   # Dependency Injection (SessionDep, CurrentUserDep)
│   │   ├── models.py         # SQLModel tables (deprecated, use domain/)
│   │   └── main.py           # FastAPI app, CORS, health check
│   ├── tests/
│   │   ├── unit/             # unit tests (domain logic)
│   │   └── integration/      # end-to-end API tests
│   ├── database.py           # create_engine, get_session, SessionDep
│   ├── setup_db.py           # Seed script (5 users, 3 championships)
│   ├── .env.example          # DATABASE_URL, SECRET_KEY, ALGORITHM, etc
│   ├── Dockerfile            # Docker image for backend (Python 3.13)
│   ├── docker-compose.yml    # Orchestration for backend + postgres
│   ├── requirements.txt      # poetry install (execute poetry.lock)
│   └── pyproject.toml        # Poetry config, exact versions
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Atomic: Button, FormInput, Card, Table, Modal, Header
│   │   ├── pages/            # LoginPage, ChampionshipsPage, RankingPage, MatchesPage
│   │   ├── context/          # AuthContext.jsx, useAuth hook, ProtectedRoute
│   │   ├── services/         # api.js (authAPI, championshipAPI, playerAPI, matchAPI, rankingAPI)
│   │   ├── hooks/            # useChampionships, useMatches, useRanking (React Query or custom)
│   │   ├── styles/           # tailwind.config.js, index.css (@tailwind imports)
│   │   ├── assets/           # images, SVG icons
│   │   ├── App.jsx           # Router setup, AuthProvider wrapper
│   │   └── main.jsx          # React entry point
│   ├── tests/                # Vitest + Testing Library
│   ├── .env.example          # VITE_API_URL=http://localhost:8000/api
│   ├── Dockerfile            # Docker image for frontend (Node 18)
│   ├── docker-compose.yml    # Frontend orchestration
│   ├── package.json          # React 20.0.0, Vite, Tailwind 3.4.1
│   ├── vite.config.js        # Vite config, port 5173
│   └── tailwind.config.js    # Tailwind customization
│
├── .github/
│   └── workflows/            # CI/CD (linting, tests, deploy)
│
├── docker-compose.yml        # Complete orchestration (app + external dependencies: postgres, redis, etc)
├── .dockerignore             # Files ignored in Docker builds
│
└── docs/                     # ADRs, diagrams, domain glossary
```

## Domain Glossary (Ubiquitous Language)

- **Championship:** Competition (league, tournament, etc). Status: draft → active → completed
- **Team:** Team within a Championship (context only, players participate directly)
- **Player:** Entity that participates in a Championship, with rating (Elo)
- **Match:** Meeting between 2 Players with result (draw, a_wins, b_wins) and rating update
- **Rating:** Elo metric (default 1500), updated after each Match
- **User:** Registered person (unique email, role: admin/player/organizer)
- **DTO (Schema):** API contract (UserCreate, ChampionshipPublic, etc)
- **Entity:** Domain object isolated from DB (contains no SQLAlchemy code)
- **Repository:** Abstraction (Port) for persistence, implemented with SQLModel

## Development Workflow (Red-Green-Refactor)

1. **Contract:** Define Pydantic schema (request/response) in `adapters/schemas.py`
2. **Red Test:** Write failing test (assert response.status_code == 201, assert user.id is not None)
3. **Green Implementation:** Code domain logic + repository until test passes
4. **Refactoring:** Extract methods, improve names, maintain coverage

## Documentation Standards

**Every new entity or business rule MUST update CLAUDE.md immediately. No exceptions.**

### When to Update CLAUDE.md

1. **New Domain Entity:** Add to Domain Glossary with description and status transitions (if applicable)
   - Format: `**EntityName:** Brief description. Status/Relationships.`
2. **New Business Rule:** Document in the relevant architecture section (Backend/Frontend)
3. **New API Route:** Update folder structure comment in Backend section if adding new router
4. **New Dependency:** Update Tech Stack section with version
5. **New Layer/Pattern:** Add to Mandatory Principles or Architecture sections

### Update Checklist
- [ ] Entity added to Domain Glossary
- [ ] Relationships and constraints clearly documented
- [ ] Status transitions specified (if applicable)
- [ ] Architecture impact noted
- [ ] Commit message includes "docs: update CLAUDE.md"

**Owner:** Every developer updating domain logic is responsible for keeping documentation synchronized.

## Running the Application

### Backend

```bash
# Setup
cd backend/
poetry install                          # Install dependencies
cp .env.example .env                    # Create .env (edit DATABASE_URL)
python setup_db.py                      # Create tables and seed data

# Development
unicorn app.main:app --reload          # Runs on http://localhost:8000

# Testing
pytest                                  # All tests
pytest tests/unit -v                    # Unit tests only
pytest tests/integration -v             # Integration tests only
pytest --cov=app --cov-report=html     # With coverage

# Linting
ruff check .                            # Lint
ruff format .                           # Autoformat
mypy app                                # Type checking
safety check                            # Dependency vulnerabilities
bandit -r app                           # Static security analysis
```

### Frontend

```bash
# Setup
cd frontend/
npm install                             # Install dependencies (Node 18+)
cp .env.example .env.local              # VITE_API_URL configured

# Development
npm run dev                             # Vite dev server (http://localhost:5173)

# Testing
npm test                                # Vitest
npm test -- --coverage                 # With coverage
npm audit                               # Check vulnerabilities
npm audit fix                           # Try to fix automatically

# Build
npm run build                           # Build for production
```

### Both Simultaneously

```bash
# Terminal 1
cd backend/ && uvicorn app.main:app --reload

# Terminal 2
cd frontend/ && npm run dev

# Open http://localhost:5173 (frontend calls http://localhost:8000/api)
```

### With Docker (Recommended for Development)

**External Dependencies with Docker Compose:**

The `docker-compose.yml` manages all external dependencies (PostgreSQL) and the application:

1. **Run application + dependencies (recommended):**
```bash
docker-compose up -d                    # Brings up backend + frontend + postgres
```

2. **Run external dependencies only (without application):**
```bash
docker-compose up -d postgres           # PostgreSQL only
# Then run backend/frontend locally
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

3. **Add more external dependencies:**
Extend the `docker-compose.yml` with Redis, ElasticSearch, etc as needed.

**Common Commands:**
```bash
# Real-time logs
docker-compose logs -f                  # View all
docker-compose logs -f backend          # Backend only
docker-compose logs -f frontend         # Frontend only
docker-compose logs -f postgres         # DB only

# Execute commands inside containers
docker-compose exec backend pytest      # Backend tests
docker-compose exec backend python setup_db.py  # Initial seed
docker-compose exec frontend npm test   # Frontend tests

# Stop containers
docker-compose down                     # Stop all
docker-compose down -v                  # Stop and remove volumes (clean DB)

# Access
Backend:  http://localhost:8000/docs
Frontend: http://localhost:5173
Postgres: localhost:5432 (user: sports_user, pass: sports_pass)
```