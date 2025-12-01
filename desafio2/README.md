# Desafio 2 — Volumes e Persistência

## Objetivo

Demonstrar persistência de dados usando volumes Docker.  
Solução mínima: um container PostgreSQL com dados armazenados em um **volume nomeado** e um container "reader" que consulta os dados para comprovar persistência.

---

## Estrutura dos arquivos

desafio2/
├─ db/
│ └─ init/
│ └─ init.sql # script de inicialização do banco (cria tabela + insere dados)
├─ reader/
│ ├─ Dockerfile
│ └─ read_db.py # script que conecta e lista os registros
├─ docker-compose.yml
└─ README.md

---

## Como funciona (resumo)

- `db` (imagem oficial `postgres`) usa:
  - variável de ambiente para usuário/senha/banco
  - **volume nomeado** `ch2_pgdata` montado em `/var/lib/postgresql/data` (dados do banco)
  - `./db/init/init.sql` é copiado para `/docker-entrypoint-initdb.d` para inserir dados **apenas na primeira inicialização do volume**
- `reader` é um container Python que se conecta ao banco (`host=db`) e imprime todas as linhas da tabela `notes`.
- **Importante**: o volume guarda os dados fora do ciclo de vida do container. Se você parar/remover o container do banco e reaproveitar o mesmo volume, os dados permanecem.

---

## Como executar e comprovar persistência

> Execute os comandos na pasta onde está o `docker-compose.yml` (challenge-02-volumes).

1. Subir a stack (constrói a imagem do reader e cria containers):

docker compose up --build -d

2. Esperar o Postgres inicializar (leva alguns segundos). Em seguida, rodar o reader para listar os dados:

docker compose run --rm reader

Saída esperada

Conectando em db:5432 como demo ao DB demo_db
Notas encontradas:

- [1] Primeira nota persistida (created_at: 2025-11-30 14:00:00)
- [2] Flamengo — Tetracampeão da Libertadores (exemplo) (created_at: 2025-11-30 14:00:00)

3. Parar e remover os containers (sem remover volumes):

docker compose down

4. Subir novamente:

docker compose up -d

5. Rodar o reader de novo:

docker compose run --rm reader

Espera-se ver a nota persistida, mesmo sem subir novamente o banco
