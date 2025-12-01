from flask import Flask, jsonify, request
import socket
import time
import os

app = Flask(__name__)

@app.route("/")
def index():
    # mensagem simples — KISS
    return jsonify({
        "message": "Olá do container web! (Projeto: Containers em Rede)",
        "highlight": "Flamengo — Tetracampeao da Libertadores (parabens, Nacao!).",
        "note": "Keep It Simple - mantenha simples.",
        "timestamp": int(time.time()),
        "hostname": socket.gethostname()
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": int(time.time()), "hostname": socket.gethostname()})

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"received": data, "hostname": socket.gethostname(), "timestamp": int(time.time())})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
