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
│   ├── .env.example          # POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, SECRET_KEY, ALGORITHM, etc
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

### Implemented Entities

- **User:** Registered person in the system. Participant or administrator of championships.
  - Fields: id (UUID), email (unique, indexed), full_name, hashed_password, is_active, created_at, updated_at
  - Relationships: Can participate as Player in multiple Championships; can manage championships as organizer
  - Constraints: Email unique, password hashed with pwdlib before storage
  - Auth: JWT token via AuthService (python-jose), password verified with AuthService.verify_password()
  - Storage: SQLModel User table, accessed via UserRepository (IUserRepository port)
  - API: POST /api/auth/register (create), GET /api/auth/me (read authenticated)
  - Status: ✅ Implemented (Phase 1), 🔄 Endpoints: register done, login/refresh TBD

### Concepts

- **DTO (Schema):** API contract (UserCreate, ChampionshipPublic, etc). Pydantic for validation + serialization
- **Entity:** Domain object isolated from DB (contains no SQLAlchemy code). Pure Python classes
- **Repository:** Abstraction (Port, ABC interface) for persistence, implemented with SQLModel adapter
- **Port:** Interface (ABC) defining contract, e.g., IUserRepository, IAuthService. No implementation details

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

**All commands must be executed with Docker Compose. No local setup required.**

### Startup

```bash
# Start all services (backend + frontend + postgres)
docker compose up -d

# Verify all services are running
docker compose ps

# Seed database with initial data
docker compose exec backend python setup_db.py
```

### Development

```bash
# View real-time logs (all services)
docker compose logs -f

# View logs for specific service
docker compose logs -f backend          # Backend logs
docker compose logs -f frontend         # Frontend logs
docker compose logs -f postgres         # Database logs
```

### Testing

```bash
# Run all backend tests
docker compose exec backend make test-backend

# Run backend tests with coverage
docker compose exec backend make test-backend-coverage

# Run backend unit tests only
docker compose exec backend pytest tests/unit -v

# Run backend integration tests only
docker compose exec backend pytest tests/integration -v

# Run frontend tests
docker compose exec frontend npm test

# Run frontend tests with coverage
docker compose exec frontend npm test -- --coverage
```

### Code Quality

```bash
# Backend linting, formatting and security
docker compose exec backend make lint-backend             # Lint
docker compose exec backend make lint-backend-security    # Security

# Frontend vulnerability audit
docker compose exec frontend npm audit            # Check vulnerabilities
docker compose exec frontend npm audit fix        # Try to fix automatically
```

### Database

```bash
# Access PostgreSQL CLI
docker compose exec postgres psql -U sports_user -d sports_db

# Seed data (populate with test data)
docker compose exec backend python setup_db.py

# Reset database (remove all data)
docker compose down -v                  # Stop services and remove volumes
docker compose up -d                    # Start fresh
docker compose exec backend python setup_db.py
```

### Maintenance

```bash
# Stop all services
docker compose down

# Stop and remove all volumes (clean slate)
docker compose down -v

# Rebuild images (if Dockerfile changes)
docker compose up -d --build

# View full service status
docker compose ps

# Execute arbitrary commands in containers
docker compose exec backend <command>
docker compose exec frontend <command>
```

### Access

```
Frontend:  http://localhost:5173
Backend:   http://localhost:8000/docs
Postgres:  localhost:5432 (user: sports_user, password: sports_pass, db: sports_db)
```
