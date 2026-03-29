.PHONY: help setup setup-backend setup-frontend dev dev-backend dev-frontend test test-backend test-frontend lint lint-backend lint-frontend build build-backend build-frontend docker-up docker-down docker-logs clean db-seed

# Colors for help output
BLUE := \033[0;34m
GREEN := \033[0;32m
NC := \033[0m # No Color

help: ## Exibe esta mensagem de ajuda
	@echo "$(BLUE)Sports Championship - Makefile Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================
# SETUP TARGETS
# ============================================

setup: setup-backend setup-frontend ## Setup completo (Backend + Frontend)
	@echo "$(BLUE)✓ Setup completo finalizado$(NC)"

setup-backend: ## Setup do Backend (Poetry install + .env)
	@echo "$(BLUE)Instalando dependências do Backend...$(NC)"
	poetry install
	@echo "$(BLUE)Criando arquivo .env...$(NC)"
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; echo "arquivo .env criado em backend/"; fi
	@echo "$(GREEN)✓ Backend setup concluído$(NC)"

setup-frontend: ## Setup do Frontend (npm install + .env)
	@echo "$(BLUE)Instalando dependências do Frontend...$(NC)"
	npm install
	@echo "$(BLUE)Criando arquivo .env.local...$(NC)"
	@if [ ! -f frontend/.env.local ]; then cp frontend/.env.example frontend/.env.local; echo "arquivo .env.local criado em frontend/"; fi
	@echo "$(GREEN)✓ Frontend setup concluído$(NC)"

db-seed: ## Cria tabelas e popula banco de dados com dados seed
	@echo "$(BLUE)Criando banco de dados e inserindo dados seed...$(NC)"
	python setup_db.py
	@echo "$(GREEN)✓ Banco de dados inicializado$(NC)"

# ============================================
# DESENVOLVIMENTO (EXECUÇÃO)
# ============================================

dev: ## Executa Backend e Frontend simultaneamente (em paralelo)
	@echo "$(BLUE)Iniciando Backend e Frontend...$(NC)"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "Docs API: http://localhost:8000/docs"
	@echo ""
	@(uvicorn app.main:app --reload) & \
	(npm run dev) & \
	wait

dev-backend: ## Executa Backend (uvicorn com reload)
	@echo "$(BLUE)Iniciando Backend em http://localhost:8000$(NC)"
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Executa Frontend (Vite dev server)
	@echo "$(BLUE)Iniciando Frontend em http://localhost:5173$(NC)"
	npm run dev

# ============================================
# TESTES
# ============================================

test: test-backend test-frontend ## Executa todos os testes (Backend + Frontend)

test-backend: ## Testes do Backend (pytest)
	@echo "$(BLUE)Executando testes do Backend...$(NC)"
	pytest -v

test-backend-coverage: ## Testes do Backend com cobertura
	@echo "$(BLUE)Executando testes do Backend com cobertura...$(NC)"
	pytest --cov=app --cov-report=html --cov-report=term-missing
	@echo "Relatório gerado em backend/htmlcov/index.html"

test-frontend: ## Testes do Frontend (Vitest)
	@echo "$(BLUE)Executando testes do Frontend...$(NC)"
	npm test

test-frontend-coverage: ## Testes do Frontend com cobertura
	@echo "$(BLUE)Executando testes do Frontend com cobertura...$(NC)"
	npm test -- --coverage

# ============================================
# LINTING & CODE QUALITY
# ============================================

lint: lint-backend lint-frontend ## Executa linting em Backend e Frontend

lint-backend: ## Linting do Backend (ruff + mypy + security checks)
	@echo "$(BLUE)Linting Backend...$(NC)"
	ruff check . --fix
	@echo "$(BLUE)Type checking Backend...$(NC)"
	mypy app
	@echo "$(BLUE)Verificando dependências Backend...$(NC)"
	-safety check
	@echo "$(GREEN)✓ Backend lint concluído$(NC)"

lint-backend-security: ## Análise de segurança do Backend (bandit)
	@echo "$(BLUE)Análise de segurança Backend...$(NC)"
	bandit -r app --format json > security-report.json || true
	@echo "Relatório gerado em backend/security-report.json"

lint-frontend: ## Linting do Frontend (npm audit)
	@echo "$(BLUE)Verificando vulnerabilidades Frontend...$(NC)"
	npm audit

lint-frontend-fix: ## Fix automático de vulnerabilidades Frontend
	@echo "$(BLUE)Corrigindo vulnerabilidades Frontend...$(NC)"
	npm audit fix

# ============================================
# BUILD
# ============================================

build: build-backend build-frontend ## Prepara aplicação para produção

build-backend: ## Build do Backend (validações)
	@echo "$(BLUE)Validando Backend para produção...$(NC)"
	ruff check . && mypy app
	@echo "$(GREEN)✓ Backend validado$(NC)"

build-frontend: ## Build do Frontend (otimizado)
	@echo "$(BLUE)Building Frontend...$(NC)"
	npm run build
	@echo "$(GREEN)✓ Frontend built em frontend/dist/$(NC)"

# ============================================
# DOCKER
# ============================================

docker-up: ## Sobe containers (Backend + Frontend + PostgreSQL)
	@echo "$(BLUE)Iniciando Docker Compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Containers iniciados$(NC)"
	@echo "Backend: http://localhost:8000/docs"
	@echo "Frontend: http://localhost:5173"

docker-down: ## Desce todos os containers
	@echo "$(BLUE)Parando Docker Compose...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Containers parados$(NC)"

docker-down-volumes: ## Desce containers e remove volumes (limpa BD)
	@echo "$(BLUE)Parando e limpando volumes...$(NC)"
	docker-compose down -v
	@echo "$(GREEN)✓ Containers e volumes removidos$(NC)"

docker-logs: ## Exibe logs dos containers em tempo real
	@echo "$(BLUE)Logs Docker Compose:$(NC)"
	docker-compose logs -f

docker-logs-backend: ## Exibe logs do Backend
	docker-compose logs -f backend

docker-logs-frontend: ## Exibe logs do Frontend (Vite)
	docker-compose logs -f frontend

docker-logs-db: ## Exibe logs do PostgreSQL
	docker-compose logs -f postgres

# ============================================
# LIMPEZA
# ============================================

clean: ## Remove cache, .pyc, node_modules e builds
	@echo "$(BLUE)Limpando artifacts...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf backend/.pytest_cache backend/htmlcov backend/.mypy_cache
	rm -rf frontend/node_modules frontend/dist
	@echo "$(GREEN)✓ Limpeza concluída$(NC)"

clean-deep: clean docker-down-volumes ## Limpeza profunda (limpa tudo incluindo volumes Docker)
	@echo "$(GREEN)✓ Limpeza profunda concluída$(NC)"

# ============================================
# ATALHOS ÚTEIS
# ============================================

install-pre-commit: ## Instala git hooks para pre-commit
	pip install pre-commit
	pre-commit install

status: ## Exibe status de execução (containers e processos)
	@echo "$(BLUE)Docker Compose Status:$(NC)"
	docker-compose ps
	@echo ""
	@echo "$(BLUE)Processos locais:$(NC)"
	@(lsof -i :8000 2>/dev/null || echo "Backend não está rodando") | grep -v COMMAND || echo "Backend não está rodando"
	@(lsof -i :5173 2>/dev/null || echo "Frontend não está rodando") | grep -v COMMAND || echo "Frontend não está rodando"

docs: ## Abre documentação nos navegadores padrão
	@echo "$(BLUE)Abrindo documentação...$(NC)"
	@command -v xdg-open >/dev/null 2>&1 && xdg-open http://localhost:8000/docs || open http://localhost:8000/docs
	@command -v xdg-open >/dev/null 2>&1 && xdg-open http://localhost:5173 || open http://localhost:5173

.DEFAULT_GOAL := help
