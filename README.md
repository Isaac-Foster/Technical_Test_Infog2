# Technical_Test_Infog2

Okay, aqui está um modelo de `README.md` gerado com base no documento de teste técnico fornecido.

-----

# Lu Estilo - API Comercial 🛍️

## 📝 Descrição do Problema

A Lu Estilo é uma empresa de confecção que está buscando novas oportunidades de negócio. Atualmente, o time comercial não possui nenhuma ferramenta que facilite a exploração de novos canais de vendas.

## 💡 Solução Proposta

Para ajudar o time comercial, foi desenvolvida uma **API RESTful utilizando FastAPI**. Esta API fornece dados e funcionalidades essenciais para facilitar a comunicação entre o time comercial, os clientes e a empresa. A API foi projetada para ser consumida por uma interface Front-End (a ser desenvolvida por outro time).

## ✨ Funcionalidades Principais (Endpoints)

A API implementa as seguintes funcionalidades, agrupadas por recurso:

### 🔑 Autenticação (`/auth`)

  * `POST /auth/login`: Autenticação de usuário.
  * `POST /auth/register`: Registro de novo usuário.
  * `POST /auth/refresh-token`: Refresh de token JWT.

### 👥 Clientes (`/clients`)

  * `GET /clients`: Listar todos os clientes, com suporte a paginação e filtro por nome e email.
  * `POST /clients`: Criar um novo cliente, validando email e CPF únicos.
  * `GET /clients/{id}`: Obter informações de um cliente específico.
  * `PUT /clients/{id}`: Atualizar informações de um cliente específico.
  * `DELETE /clients/{id}`: Excluir um cliente.

### 📦 Produtos (`/products`)

  * `GET /products`: Listar todos os produtos, com suporte a paginação e filtros por categoria, preço e disponibilidade.
  * `POST /products`: Criar um novo produto (descrição, valor de venda, código de barras, seção, estoque inicial, data de validade, imagens).
  * `GET /products/{id}`: Obter informações de um produto específico.
  * `PUT /products/{id}`: Atualizar informações de um produto específico.
  * `DELETE /products/{id}`: Excluir um produto.

### 🛒 Pedidos (`/orders`)

  * `GET /orders`: Listar todos os pedidos, com filtros por: período, seção dos produtos, id\_pedido, status do pedido e cliente.
  * `POST /orders`: Criar um novo pedido (múltiplos produtos, validação de estoque).
  * `GET /orders/{id}`: Obter informações de um pedido específico.
  * `PUT /orders/{id}`: Atualizar informações de um pedido específico (incluindo status).
  * `DELETE /orders/{id}`: Excluir um pedido.

-----

## 🛠️ Tecnologias Utilizadas

  * **Linguagem:** Python 3.x
  * **Framework:** FastAPI
  * **Banco de Dados:** PostgreSQL (Relacional)
  * **Testes:** Pytest
  * **Autenticação:** JWT (JSON Web Tokens)
  * **Containerização:** Docker
  * **Migrações de Banco de Dados:** (Ex: Alembic, ou sistema de migração do ORM escolhido)

-----

## 📋 Outros Requisitos Implementados

  * **Autenticação e Autorização:**
      * Uso de JWT para proteger as rotas.
      * Rotas de clientes, produtos e pedidos acessíveis apenas por usuários autenticados.
      * Implementação de níveis de acesso: `admin` e `usuário regular`, com restrições de ações específicas.
  * **Validação e Tratamento de Erros:**
      * Validações adequadas para todos os inputs dos endpoints.
      * Respostas de erro informativas e padronizadas.
      * (Opcional) Registro de erros críticos em um sistema de monitoramento (ex: Sentry).
  * **Banco de Dados:**
      * Utilização de um banco de dados relacional (PostgreSQL).
      * Implementação de migrações para facilitar a configuração e evolução do schema do banco.
      * Uso de índices adequados para otimizar a performance das consultas.

-----

## ⚙️ Configuração do Ambiente de Desenvolvimento

1.  **Clone o repositório:**

    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_AQUI]
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    # Linux/macOS
    source venv/bin/activate
    # Windows
    # venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```bash
    uv sync
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto, baseado no arquivo `.env.example` (se fornecido). Preencha com as configurações necessárias, como:

    ```env
    SECRET_KEY_JWT = ''

    ALGORITHM_JWT = 'HS256'
    EXPIRATION_TIME_JWT = 30

    DATABASE = ''
    DATABASE = ''

    ```

5.  **Configure o Banco de Dados PostgreSQL:**

      * Certifique-se de ter o PostgreSQL instalado e rodando.
      * Crie o banco de dados especificado na variável `DATABASE`.

6.  **Aplique as migrações do banco de dados:**
    *(Adicionar aqui o comando para rodar as migrações, ex: `alembic upgrade head` ou o comando específico da ferramenta de migração utilizada).*

    ```bash
    # Exemplo com Alembic:
    # alembic upgrade head
    ```

-----

## ▶️ Executando a Aplicação

Para iniciar o servidor FastAPI (com recarregamento automático durante o desenvolvimento):

```bash
task run
```

A API estará disponível em `http://127.0.0.1:8000`.

-----

## 📚 Documentação da API (Swagger)

Com a aplicação em execução, a documentação interativa (Swagger UI) gerada automaticamente pelo FastAPI pode ser acessada em:
[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)

Uma documentação alternativa (ReDoc) também está disponível em:
[http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)

A documentação inclui:

  * Exemplos de requisições e respostas para cada endpoint.
  * Descrições detalhadas, regras de negócio e casos de uso para cada endpoint.

-----

## 🧪 Executando os Testes

Para rodar os testes unitários e de integração utilizando pytest:

```bash
task test
```
OBS: rodar o teste fora do deploy é necessário mudar A DB no src/infra/database/sql.py
 -> Config.DATABASE_UR para Conffig.DATABASE_TEST
Certifique-se de que as configurações de banco de dados para o ambiente de teste estejam corretas (se diferente do desenvolvimento).

-----

## 🐳 Deploy com Docker

O projeto está configurado para ser executado em um container Docker.

1.  **Construa a imagem Docker e deploy:**

    ```bash
    docker compose up -d .
    ```

-----

## 📌 Notas Adicionais

  * Os endpoints e funcionalidades foram adaptados conforme o necessário para demonstrar as habilidades solicitadas.
  * Foram aplicadas boas práticas de programação e arquitetura.
  * As alterações no código foram divididas em commits pequenos e bem descritos.
  * O código fonte está disponível no GitHub: [LINK\_PARA\_O\_REPOSITORIO\_NO\_GITHUB]

-----

**Prazo de Entrega do Teste:** 26/05/2025

**Links Úteis:**

  * [FastAPI Documentation](https://fastapi.tiangolo.com/)
  * [Pytest Documentation](https://docs.pytest.org/)
  * [Docker Documentation](https://docs.docker.com/)
