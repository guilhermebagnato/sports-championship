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
	poetry run python setup_db.py
	@echo "$(GREEN)✓ Banco de dados inicializado$(NC)"

# ============================================
# DESENVOLVIMENTO (EXECUÇÃO)
# ============================================

dev-backend: ## Executa Backend (uvicorn com reload)
	@echo "$(BLUE)Iniciando Backend em http://localhost:8000$(NC)"
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ============================================
# TESTES
# ============================================

test-backend: ## Testes do Backend (pytest)
	@echo "$(BLUE)Executando testes do Backend...$(NC)"
	poetry run pytest -v

test-backend-coverage: ## Testes do Backend com cobertura
	@echo "$(BLUE)Executando testes do Backend com cobertura...$(NC)"
	poetry run pytest --cov=app --cov-report=html --cov-report=term-missing
	@echo "Relatório gerado em backend/htmlcov/index.html"

# ============================================
# LINTING & CODE QUALITY
# ============================================

lint-backend: ## Linting do Backend (ruff + mypy)
	@echo "$(BLUE)Linting Backend...$(NC)"
	poetry run isort .
	poetry run black .
	poetry run ruff check . --fix
	poetry run mypy app
	@echo "$(GREEN)✓ Backend lint concluído$(NC)"

lint-backend-vulnerability: ## Análise de segurança do Backend (safety)
	@echo "$(BLUE)Análise de vulnerabilidades Backend...$(NC)"
	poetry run safety check
	@echo "$(GREEN)✓ Backend vulnerability concluído$(NC)"

lint-backend-security: ## Análise de segurança do Backend (bandit)
	@echo "$(BLUE)Análise de segurança Backend...$(NC)"
	poetry run bandit -r app
	@echo "$(GREEN)✓ Backend security concluído$(NC)"

# ============================================
# LIMPEZA
# ============================================

clean: ## Remove cache, .pyc, node_modules e builds
	@echo "$(BLUE)Limpando artifacts...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf backend/.pytest_cache backend/htmlcov backend/.mypy_cache
	@echo "$(GREEN)✓ Limpeza concluída$(NC)"

# ============================================
# ATALHOS ÚTEIS
# ============================================

install-pre-commit: ## Instala git hooks para pre-commit
	pip install pre-commit
	pre-commit install

docs: ## Abre documentação nos navegadores padrão
	@echo "$(BLUE)Abrindo documentação...$(NC)"
	@command -v xdg-open >/dev/null 2>&1 && xdg-open http://localhost:8000/docs || open http://localhost:8000/docs

.DEFAULT_GOAL := help
