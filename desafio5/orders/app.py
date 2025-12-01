from flask import Flask, jsonify
import socket, time, os

app = Flask(__name__)

ORDERS = [
    {"id": 101, "user_id": 1, "total": 120.50, "created_at": "2024-11-01"},
    {"id": 102, "user_id": 3, "total": 350.00, "created_at": "2025-11-10"},
    {"id": 103, "user_id": 2, "total": 25.00, "created_at": "2025-01-15"}
]

@app.route("/orders")
def orders():
    return jsonify({
        "count": len(ORDERS),
        "orders": ORDERS,
        "service": "orders",
        "hostname": socket.gethostname(),
        "timestamp": int(time.time())
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "orders", "hostname": socket.gethostname()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    app.run(host="0.0.0.0", port=port)
