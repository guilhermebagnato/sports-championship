# ============================================
# STAGE 1: Builder
# ============================================
FROM python:3.13-slim as builder

WORKDIR /tmp

# Instalar dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copiar apenas poetry files
COPY pyproject.toml poetry.lock ./

# Criar ambiente virtual e instalar dependências
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev --no-interaction --no-ansi

# ============================================
# STAGE 2: Runtime
# ============================================
FROM python:3.13-slim

WORKDIR /app

# Instalar apenas dependências de runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar ambiente virtual do builder
COPY --from=builder /tmp/.venv /app/.venv

# Copiar código-fonte
COPY . .

# Ativar venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
