# Desafio 3 — Docker Compose Orquestrando Serviços

**Resumo**  
Solucão mínima com 3 serviços orquestrados pelo Docker Compose:

- **web**: aplicação Flask (porta `8080`) que consulta Redis e Postgres.
- **db**: PostgreSQL (dados persistidos em volume nomeado).
- **cache**: Redis (cache em memória).
  Menção temática: **"Flamengo — Tetracampeão da Libertadores 2025"** está inserida como exemplo de dado inicial.

## Estrutura do projeto

desafio3/
├─ web/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py
├─ db/
│ └─ init/
│ └─ init.sql
└─ docker-compose.yml

## O que cada serviço faz

- **db (Postgres)**: contém tabela `messages` preenchida pelo `init.sql`. Dados persistidos em volume nomeado `ch3_pgdata`.
- **cache (Redis)**: guarda a última mensagem buscada (chave `app:latest_message`) para acelerar respostas.
- **web (Flask)**:
  - `GET /message` → tenta retornar o valor em Redis (source: cache); em caso de miss, lê do Postgres (source: db) e popula o cache.
  - `GET /clear_cache` → limpa o cache.
  - `GET /health` → health check simples.

## Como rodar (passo a passo)

1. Abra o terminal na pasta do projeto

cd desafio3

2. Suba a stack

docker compose up --build -d

O compose:

- cria a rede ch3_net
- projeta dependências (depends_on com service_healthy para aguardar DB/Redis)
- constrói a imagem do web e sobe todos os serviços

3. Verifique serviços:

docker ps

4. Teste o endpoint principal:

curl http://localhost:8080/message

Primeira chamada: source: db (lê do Postgres e popula Redis).
Chamada subsequente (dentro de 60s): source: cache.

5. Limpar o cache e forçar leitura do DB:

curl http://localhost:8080/clear_cache
curl http://localhost:8080/message
