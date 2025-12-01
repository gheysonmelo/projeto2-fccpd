# Desafio 4 — Microsserviços Independentes

## Resumo rápido

Implementação minimalista com **dois microsserviços** independentes que se comunicam via HTTP:

- **Servico A** (`servico-a`) — provê lista de usuários em `/users`.
  - Porta: `5000`
  - Exemplo de dado inclui uma referência temática:  
    `"Alô — Flamengo — Tetracampeão da Libertadores 2025!"` (no campo `note` de um usuário).
- **Servico B** (`servico-b`) — consome `/users` do Servico A e expõe informações combinadas em `/combined`.
  - Porta: `5001`
  - Produz frases do tipo: `"Usuário Alice Silva — ativo desde 2021-03-10"`.

Ambos têm Dockerfile próprio e são orquestrados com `docker-compose`.

## Estrutura do projeto

desafio4/
├─ servico-a/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py
├─ servico-b/
│ ├─ Dockerfile
│ ├─ requirements.txt
│ └─ app.py
└─ docker-compose.yml

## Como rodar (passo a passo)

1. Abra o terminal na pasta `desafio4`.

2. Suba os serviços:

docker compose up --build -d

3. Verifique se os containers subiram:

docker ps

4. Testes rápidos:

- Listar usuários (Servico A):

curl http://localhost:5000/users

Resposta esperada (exemplo):

{
"count": 3,
"users": [
{"id": 1, "name": "Danilo Luiz - O redentor rubro negro", "joined": "2021-03-10", "active": True},
{"id": 2, "name": "Miguel Becker - Vascaino", "joined": "2022-06-01", "active": True},
{
"id": 3,
"name": "Gheyson Melo - Torcedor Flamengo",
"joined": "2019-02-20",
"active": True,
"note": "Alô — em clima de campeão: Flamengo — Tetracampeão da Libertadores 2025!"
}
],
"hostname":"ms_servico_a",
"timestamp":...
}

- Ver as informações combinadas (Servico B consome Servico A):

curl http://localhost:5001/combined

Resposta esperada (exemplo):

{
"source":"servico-a",
"count":3,
"summary":[
{"id":1,"display":"Danilo Luiz - O redentor rubro negro — ativo desde 2021-03-10","note":""},
{"id":2,"display":"Miguel Becker - Vascaino — ativo desde 2022-06-01","note":""},
{"id":3,"display":"Usuário Gheyson Melo - Torcedor Flamengo — ativo desde 2019-02-20","note":"Alô — Flamengo — Tetracampeão da Libertadores 2025!"}
],
"hostname":"ms_servico_b",
"timestamp":...
}
