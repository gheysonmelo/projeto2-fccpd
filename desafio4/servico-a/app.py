# service-a/app.py
from flask import Flask, jsonify
import time
import socket

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "Danilo Luiz - O redentor rubro negro", "joined": "2021-03-10", "active": True},
    {"id": 2, "name": "Miguel Becker - Vascaino", "joined": "2022-06-01", "active": True},
    {
        "id": 3,
        "name": "Gheyson Melo - Torcedor Flamengo",
        "joined": "2019-02-20",
        "active": True,
        "note": "Alô — em clima de campeão: Flamengo — Tetracampeão da Libertadores 2025!"
    }
]

@app.route("/users")
def users():
    return jsonify({"count": len(USERS), "users": USERS, "hostname": socket.gethostname(), "timestamp": int(time.time())})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "servico": "servico-a", "hostname": socket.gethostname()})

if __name__ == "__main__":
    port = int(__import__("os").environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
