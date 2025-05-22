# Usar a imagem base do Python 3.11 Debian Slim
FROM python:3.11-alpine

# Instalar o UV da Astral
RUN curl -LsSf https://astral.sh/uv/install.sh | bash

# Copiar o código da sua aplicação para o contêiner
WORKDIR /app
COPY . /app

# Configurar o PATH para garantir que o UV esteja acessível
ENV PATH=$PATH:/root/.local/bin

