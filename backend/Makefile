.PHONY: help setup setup-backend dev dev-backend test test-backend lint lint-backend build build-backend docker-up docker-down docker-logs clean db-seed

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

setup-backend: ## Setup do Backend (Poetry install + .env)
	@echo "$(BLUE)Instalando dependências do Backend...$(NC)"
	poetry install
	@echo "$(BLUE)Criando arquivo .env...$(NC)"
	@if [ ! -f .env ]; then cp .env.example .env; echo "arquivo .env criado em backend/"; fi
	@echo "$(GREEN)✓ Backend setup concluído$(NC)"

db-seed: ## Cria tabelas e popula banco de dados com dados seed
	@echo "$(BLUE)Criando banco de dados e inserindo dados seed...$(NC)"
	python setup_db.py
	@echo "$(GREEN)✓ Banco de dados inicializado$(NC)"

# ============================================
# DESENVOLVIMENTO (EXECUÇÃO)
# ============================================

dev-backend: ## Executa Backend (uvicorn com reload)
	@echo "$(BLUE)Iniciando Backend em http://localhost:8000$(NC)"
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ============================================
# TESTES
# ============================================

test-backend: ## Testes do Backend (pytest)
	@echo "$(BLUE)Executando testes do Backend...$(NC)"
	pytest -v

test-backend-coverage: ## Testes do Backend com cobertura
	@echo "$(BLUE)Executando testes do Backend com cobertura...$(NC)"
	pytest --cov=app --cov-report=html --cov-report=term-missing
	@echo "Relatório gerado em backend/htmlcov/index.html"

# ============================================
# LINTING & CODE QUALITY
# ============================================

lint-backend: ## Linting do Backend (ruff + mypy + security checks)
	@echo "$(BLUE)Linting Backend...$(NC)"
	ruff check . --fix
	@echo "$(BLUE)Type checking Backend...$(NC)"
	mypy app
	@echo "$(GREEN)✓ Backend lint concluído$(NC)"

lint-backend-vulnerability: ## Análise de segurança do Backend (safety)
	@echo "$(BLUE)Análise de vulnerabilidades Backend...$(NC)"
	safety check
	@echo "$(GREEN)✓ Backend vulnerability concluído$(NC)"

lint-backend-security: ## Análise de segurança do Backend (bandit)
	@echo "$(BLUE)Análise de segurança Backend...$(NC)"
	bandit -r app
	@echo "$(GREEN)✓ Backend security concluído$(NC)"

# ============================================
# BUILD
# ============================================

build-backend: ## Build do Backend (validações)
	@echo "$(BLUE)Validando Backend para produção...$(NC)"
	ruff check . && mypy app
	@echo "$(GREEN)✓ Backend validado$(NC)"

# ============================================
# DOCKER
# ============================================

docker-up: ## Sobe containers (Backend + PostgreSQL)
	@echo "$(BLUE)Iniciando Docker Compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Containers iniciados$(NC)"
	@echo "Backend: http://localhost:8000/docs"

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

docs: ## Abre documentação nos navegadores padrão
	@echo "$(BLUE)Abrindo documentação...$(NC)"
	@command -v xdg-open >/dev/null 2>&1 && xdg-open http://localhost:8000/docs || open http://localhost:8000/docs
	@command -v xdg-open >/dev/null 2>&1 && xdg-open http://localhost:5173 || open http://localhost:5173

.DEFAULT_GOAL := help
