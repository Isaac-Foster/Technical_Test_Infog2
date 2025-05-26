# Usar a imagem slim do Python 3.11
FROM python:3.11-slim

# Instalar dependências essenciais para compilar psutil e outras dependências
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar o UV da Astral
RUN curl -LsSf https://astral.sh/uv/install.sh | bash

# Adicionar o diretório do UV ao PATH
ENV PATH=$PATH:/root/.local/bin

# Definir o diretório de trabalho
WORKDIR /app

# Copiar primeiro os arquivos de dependências
COPY pyproject.toml uv.lock* ./

# Instalar dependências do projeto incluindo dev (isso criará o .venv)
RUN uv sync

# Copiar o resto dos arquivos do código
COPY . /app

# Expor a porta da aplicação
EXPOSE 8000

# Usar uv run para executar comandos no ambiente virtual
CMD ["uv", "run", "task", "run"]