# users/app.py
from flask import Flask, jsonify
import socket, time, os

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "Alice Silva", "joined": "2021-03-10", "active": True},
    {"id": 2, "name": "Bruno Costa", "joined": "2022-06-01", "active": True},
    {
        "id": 3,
        "name": "Torcedor Flamengo",
        "joined": "2019-02-20",
        "active": True,
        "note": "Alô — Flamengo — Tetracampeão da Libertadores 2025!"
    }
]

@app.route("/users")
def users():
    return jsonify({
        "count": len(USERS),
        "users": USERS,
        "service": "users",
        "hostname": socket.gethostname(),
        "timestamp": int(time.time())
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "users", "hostname": socket.gethostname()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    app.run(host="0.0.0.0", port=port)
