# ============================================
# Single Stage Build
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências de build e runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    postgresql-client \
    make \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pbr setuptools

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copiar poetry files
COPY pyproject.toml* ./

# Criar ambiente virtual e instalar dependências
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-interaction --no-ansi

# Copiar código-fonte (apenas backend/app)
COPY app ./app

# Ativar venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD /app/.venv/bin/python -c "import requests; requests.get('http://localhost:8000/api/health')" || exit 1

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
