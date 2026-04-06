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

1.  **DDD (Domain-Driven Design):**
    -   **Rich Domain:** Entities (e.g., `Championship`, `Match`) must encapsulate business logic and state transitions, not just hold data.
    -   **Value Objects:** Use for descriptive attributes (e.g., `Email`, `Score`) that don't have an identity but have validation logic.
    -   **Aggregates:** Group related entities that must be treated as a single unit for data changes (e.g., a `Match` and its `Events`).
    -   **Ubiquitous Language:** Use the same terminology in code (classes, variables), documentation, and communication.
2.  **TDD (Test-Driven Development):**
    -   **Red:** Start with a failing test that defines the expected behavior of a new feature or fix.
    -   **Green:** Write the minimum code required to make the test pass.
    -   **Refactor:** Clean up the code while ensuring tests remain green.
    -   **Mocking:** Use mocks for external dependencies (database, external APIs) in unit tests. Integration tests should use a real test database.
3.  **Clean Code:**
    -   **Meaningful Names:** Variables, functions, and classes must reveal intent (e.g., `calculate_group_standings` vs `calc_std`).
    -   **Small Functions:** Functions should do one thing and do it well (SRP). Use a maximum of 20-30 lines as a guideline.
    -   **DRY (Don't Repeat Yourself):** Abstract common logic to prevent duplication.
    -   **YAGNI (You Ain't Gonna Need It):** Don't implement features or abstractions until they are actually needed.
4.  **Hexagonal Architecture (Ports & Adapters):**
    -   **Core (Domain):** The heart of the app, containing business rules, independent of any framework or database.
    -   **Application (Use Cases):** Orchestrates the flow of data to and from the domain.
    -   **Ports (Interfaces):** Abstract definitions of what the application needs (e.g., `IUserRepository`).
    -   **Adapters (Infrastructure):** Concrete implementations of ports (e.g., `SQLAlchemyUserRepository`, `FastAPIControllers`).
    -   **Dependency Rule:** Dependencies always point inwards toward the Domain. The Domain never knows about the Database or API.
5.  **SOLID Principles:**
    -   **S - Single Responsibility:** A class should have one, and only one, reason to change (e.g., one service per use case).
    -   **O - Open/Closed:** Entities should be open for extension (e.g., new championship types) but closed for modification.
    -   **L - Liskov Substitution:** Subtypes must be substitutable for their base types (e.g., any `Repository` implementation must work the same).
    -   **I - Interface Segregation:** Prefer many small, specific interfaces over one large, general-purpose one.
    -   **D - Dependency Inversion:** Depend on abstractions (Ports), not on concrete implementations (Adapters). Use FastAPI's `Depends` for this.
6.  **Backend Fundamentals (Strict Standards):**
    -   **Async Consistency:** Use `async/await` for all I/O operations (database, API calls). Avoid blocking calls in the main event loop.
    -   **Global Error Handling:** Implement custom domain exceptions and catch them in FastAPI global handlers to maintain consistent error response structures.
    -   **Database Transactions:** Ensure that units of work involving multiple writes are wrapped in transactions. Use the `SessionDep` dependency for managed life-cycles.
    -   **Schema Strictness:** Never return database models directly from the API. Always use Pydantic `Public` schemas to filter sensitive data and define the contract.
    -   **Dependency Injection:** Leverage FastAPI's `Depends` for all cross-cutting concerns (Auth, DB Sessions, Service registration) to facilitate testing and decoupling.
7.  **Exact Versioning:** Dependencies must be locked with exact versions in `poetry.lock` and `package-lock.json`, without the use of `~` or `^` in production environments.

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

1.  **Contract:** Define Pydantic schema (request/response) in `adapters/schemas.py`
2.  **Red Test:** Write failing test (assert response.status_code == 201, assert user.id is not None)
3.  **Green Implementation:** Code domain logic + repository until test passes
4.  **Refactoring:** Extract methods, improve names, maintain coverage

## Documentation Standards

**Every new entity or business rule MUST update CLAUDE.md immediately. No exceptions.**

### When to Update CLAUDE.md

1.  **New Domain Entity:** Add to Domain Glossary with description and status transitions (if applicable)
    -   Format: `**EntityName:** Brief description. Status/Relationships.`
2.  **New Business Rule:** Document in the relevant architecture section (Backend/Frontend)
3.  **New API Route:** Update folder structure comment in Backend section if adding new router
4.  **New Dependency:** Update Tech Stack section with version
5.  **New Layer/Pattern:** Add to Mandatory Principles or Architecture sections

### Update Checklist
- [ ] Entity added to Domain Glossary
- [ ] Relationships and constraints clearly documented
- [ ] Status transitions specified (if applicable)
- [ ] Architecture impact noted
- [ ] Commit message includes "docs: update CLAUDE.md"

**Owner:** Every developer updating domain logic is responsible for keeping documentation synchronized.

### Startup

```bash
# Start all services (backend + frontend + postgres)
docker compose up -d --build

# Verify all services are running
docker compose ps

# Seed database with initial data
python setup_db.py
```

### Testing

```bash
# Run all backend tests
make test-backend

# Run backend tests with coverage
make test-backend-coverage

# Run backend unit tests only
pytest tests/unit -v

# Run backend integration tests only
pytest tests/integration -v

# Run frontend tests
docker compose exec frontend npm test

# Run frontend tests with coverage
docker compose exec frontend npm test -- --coverage
```

### Code Quality

```bash
# Backend linting, formatting and security
make lint-backend             # Lint
make lint-backend-security    # Security

# Frontend vulnerability audit
docker compose exec frontend npm audit            # Check vulnerabilities
docker compose exec frontend npm audit fix        # Try to fix automatically
```

### Database

```bash
# Access PostgreSQL CLI
docker compose exec postgres psql -U sports_user -d sports_db

# Seed data (populate with test data)
python setup_db.py

# Reset database (remove all data)
docker compose down -v                  # Stop services and remove volumes
docker compose up -d                    # Start fresh
python setup_db.py
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
