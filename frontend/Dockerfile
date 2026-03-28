# ============================================
# Development Frontend (Vite Dev Server)
# ============================================
FROM node:18-alpine

WORKDIR /app

# Instalar dependências
COPY package.json package-lock.json ./
RUN npm ci --prefer-offline --no-audit

# Copiar código-fonte
COPY . .

# Variáveis de ambiente
ENV VITE_API_URL=http://localhost:8000/api
ENV NODE_ENV=development

# Expor porta (Vite padrão)
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:5173/ || exit 1

# Comando padrão (dev com hot reload)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
