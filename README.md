# Sports Management System

High-integrity system for managing sports championships with leagues, tournaments, and knockout stages.

## ⚠️ Experimental Project

This is an **experimental project** focused on **AI-driven development learning**. The primary goal is to explore best practices in:
- Domain-Driven Design (DDD)
- Test-Driven Development (TDD)
- Clean Architecture and Hexagonal Architecture
- AI-assisted coding with Claude
- Full-stack development from domain modeling to deployment

**Note:** While the codebase follows production-ready patterns, this project is primarily an educational resource for learning modern software development practices with AI assistance.

## 📋 Technology Stack

### Backend
- **Python 3.13+** with FastAPI 0.104.1
- **PostgreSQL** for data persistence
- **SQLModel/SQLAlchemy 2.0.23** for ORM
- **JWT** (python-jose) for authentication
- **pytest** for automated testing

### Frontend
- **React 20.0.0** with TypeScript
- **Vite** as build tool
- **Tailwind CSS 3.4.1** for styling
- **React Router 7.x** for navigation
- **Vitest** and **Testing Library** for testing

### DevOps
- **Docker** and **Docker Compose** for containerization
- Fully isolated environment with managed dependencies

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed, **OR**
- Python 3.13+ and Node.js 18+ installed locally
- PostgreSQL 15+ (if not using Docker)

### Option 1: With Docker (Recommended)

```bash
# Clone repository
git clone <repo-url>
cd sports-championship

# Start containers
docker-compose up -d

# Application ready at:
# Frontend:  http://localhost:5173
# Backend:   http://localhost:8000/docs
# PostgreSQL: localhost:5432
```

### Option 2: Locally

#### Backend

```bash
cd backend/

# Setup
poetry install
cp .env.example .env
python setup_db.py

# Development
uvicorn app.main:app --reload
```

Backend running on `http://localhost:8000`

#### Frontend

```bash
cd frontend/

# Setup
npm install
cp .env.example .env.local

# Development
npm run dev
```

Frontend running on `http://localhost:5173`

## 🧪 Testing

### Backend

```bash
cd backend/

# All tests
pytest

# Unit tests only
pytest tests/unit -v

# Integration tests only
pytest tests/integration -v

# With code coverage
pytest --cov=app --cov-report=html
```

### Frontend

```bash
cd frontend/

# Run tests
npm test

# With coverage
npm test -- --coverage
```

## 🔍 Quality Checks

### Backend

```bash
cd backend/

# Linting
ruff check .
ruff format .

# Type checking
mypy app

# Vulnerabilities
safety check
bandit -r app
```

### Frontend

```bash
cd frontend/

# Vulnerabilities
npm audit

# Try to fix automatically
npm audit fix
```

## 📦 Build & Deploy

### Backend

```bash
cd backend/

# Build Docker
docker build -t sports-backend .

# Run container
docker run -p 8000:8000 sports-backend
```

### Frontend

```bash
cd frontend/

# Build for production
npm run build

# Preview the build
npm run preview
```

## 🤝 Contributing

1. Create a branch: `git checkout -b feature/my-feature`
2. Commit with descriptive messages: `git commit -m "feat: add new feature"`
3. Write tests for new code (TDD first)
4. Open a Pull Request with clear description
5. Ensure CI/CD passes (tests, linting, type checking)

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for complete details.

The MIT License allows free use, modification, and distribution, including commercial use, without restrictions. You only need to maintain the copyright attribution.
