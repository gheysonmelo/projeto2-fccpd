# Desafio 1 — Containers em Rede

Solução mínima para demonstrar comunicação entre dois containers Docker em uma rede personalizada.

- **web**: servidor Flask na porta `8000`, retornando JSON simples.
- **client**: container Alpine executando `curl` em loop.
- Inclui referência temática: **“Flamengo — Tetracampeão da Libertadores”**.

## Arquitetura

desafio1/
├─ web/ → Servidor Flask (porta 8000)
├─ client/ → Container com curl chamando o web periodicamente
└─ docker-compose.yml → Define serviços + rede docker

Os containers são conectados automaticamente pela rede nomeada criada pelo `docker-compose`.  
O cliente usa o hostname `web` (resolvido pelo DNS interno do Docker) para acessar `http://web:8000`.

## Funcionamento

### **web (Flask)**

- Expondo endpoint `GET /`.
- Retorna JSON contendo:
  - mensagem simples
  - menção ao Flamengo tetracampeão
  - timestamp
  - hostname do container

### **client (Alpine + curl)**

- Executa um script que a cada 5 segundos:
  - envia uma requisição para `http://web:8000`
  - imprime o resultado no console
- Serve para demonstrar comunicação contínua entre containers.

---

## Como executar

docker compose up --build -d

## Verificar se os containers subiram:

docker ps

## Testar o servidor Flask:

curl http://localhost:8000

## Ver os logs do cliente:

docker compose logs -f client

## Derrubar os containers:

docker compose down

## Exemplo de resposta JSON esperada

{
"message": "Olá do container web!",
"highlight": "Flamengo — Tetracampeão da Libertadores.",
"timestamp": 1700000000,
"hostname": "desafio1_web"
}
