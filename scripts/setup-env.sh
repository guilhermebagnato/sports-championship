#!/bin/bash
# Script para gerar SECRET_KEY segura e configurar .env para Docker

set -e

echo "🔐 Gerando SECRET_KEY segura para JWT..."

# Gerar SECRET_KEY com openssl
SECRET_KEY=$(openssl rand -hex 32)

echo ""
echo "✅ SECRET_KEY gerada com sucesso!"
echo ""
echo "Copie a chave abaixo para seu arquivo .env:"
echo ""
echo "SECRET_KEY=$SECRET_KEY"
echo ""

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "✅ Arquivo .env criado"
fi

# Atualizar .env com a nova SECRET_KEY (se openssl instalado)
if command -v sed &> /dev/null; then
    echo "Atualizando .env com SECRET_KEY..."
    
    # macOS precisa de -i ''
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/your-super-secret-key-change-this-in-production-with-something-long-and-random/$SECRET_KEY/" .env
    else
        sed -i "s/your-super-secret-key-change-this-in-production-with-something-long-and-random/$SECRET_KEY/" .env
    fi
    
    echo "✅ Arquivo .env atualizado"
fi

echo ""
echo "📋 Próximos passos:"
echo "1. Revisar .env e ajustar outras variáveis conforme necessário"
echo "2. Executar: docker-compose up -d"
echo "3. Acessar http://localhost:5173"
echo ""
