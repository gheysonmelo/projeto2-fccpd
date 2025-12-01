# Desafio 5 — Microsserviços com API Gateway

## Resumo

Implementação simples de arquitetura com **API Gateway** que centraliza o acesso a dois microsserviços independentes:

- **users** — serviço que fornece lista de usuários (`/users`).
  - Porta: `5004`
  - Menção temática: `"Alô — Flamengo — Tetracampeão da Libertadores 2025!"` no `note` de um usuário.
- **orders** — serviço que fornece pedidos (`/orders`).
  - Porta: `5005`
- **gateway** — expõe `/users` e `/orders` e redireciona (proxy) as chamadas para os serviços correspondentes.
  - Porta: `8082` (ponto único de entrada para o sistema)

Todos os serviços executam em containers e são orquestrados com `docker-compose`.

## Estrutura

desafio5/
├─ gateway/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py
├─ users/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py
├─ orders/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py
└─ docker-compose.yml

## Como rodar

1. Abra o terminal na pasta `desafio5` (onde está o `docker-compose.yml`):

cd /caminho/para/desafio5

2. Suba todos os serviços (build + detach):

docker compose up --build -d

3. Verifique os containers:

docker ps

Endpoints (teste via host)

Gateway:

- GET http://localhost:8082/users → conteúdo proveniente do serviço users (via gateway)

- GET http://localhost:8082/orders → conteúdo proveniente do serviço orders (via gateway)

- GET http://localhost:8082/users_orders → orquestra chamadas e retorna ambos (exemplo composto)

- GET http://localhost:8082/health → health do gateway

Serviços (direto, apenas para debug):

- GET http://localhost:5004/users

- GET http://localhost:5005/orders
