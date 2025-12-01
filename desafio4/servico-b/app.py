from flask import Flask, jsonify
import requests
import os
import socket
import time

app = Flask(__name__)

SERVICO_A_HOST = os.environ.get("SERVICO_A_HOST", "servico-a")
SERVICO_A_PORT = int(os.environ.get("SERVICO_A_PORT", 5000))
SERVICO_A_URL = f"http://{SERVICO_A_HOST}:{SERVICO_A_PORT}/users"

def fetch_users():
    try:
        resp = requests.get(SERVICO_A_URL, timeout=3)
        resp.raise_for_status()
        data = resp.json()
        return data.get("users", [])
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    return jsonify({
        "message": "Servico B — consumidor de Servico A",
        "note": "Use /combined para ver os usuários processados",
        "hostname": socket.gethostname()
    })

@app.route("/combined")
def combined():
    users = fetch_users()
    if isinstance(users, dict) and "error" in users:
        return jsonify({"error": "failed to fetch users from servico-a", "detail": users["error"]}), 502

    # transforma os dados: "Usuário X ativo desde YYYY"
    summary = []
    for u in users:
        joined = u.get("joined", "unknown")
        name = u.get("name", f"User-{u.get('id')}")
        active = "ativo" if u.get("active") else "inativo"
        note = u.get("note", "")
        summary.append({
            "id": u.get("id"),
            "display": f"Usuário {name} — {active} desde {joined}",
            "note": note
        })

    return jsonify({
        "source": "servico-a",
        "count": len(summary),
        "summary": summary,
        "hostname": socket.gethostname(),
        "timestamp": int(time.time())
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "servico": "servico-b", "hostname": socket.gethostname()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
