from flask import Flask, jsonify, request
import requests, os, socket, time

app = Flask(__name__)

USERS_HOST = os.environ.get("USERS_HOST", "users")
USERS_PORT = int(os.environ.get("USERS_PORT", 5004))
ORDERS_HOST = os.environ.get("ORDERS_HOST", "orders")
ORDERS_PORT = int(os.environ.get("ORDERS_PORT", 5005))

USERS_URL = f"http://{USERS_HOST}:{USERS_PORT}/users"
ORDERS_URL = f"http://{ORDERS_HOST}:{ORDERS_PORT}/orders"

def fetch(url, timeout=4):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    return jsonify({
        "message": "API Gateway - use /users or /orders",
        "hostname": socket.gethostname(),
        "timestamp": int(time.time())
    })

@app.route("/users")
def users_proxy():
    data = fetch(USERS_URL)
    if "error" in data:
        return jsonify({"error": "failed to fetch users", "detail": data["error"]}), 502
    # indicate gateway path
    data["_via_gateway"] = True
    data["_gateway_host"] = socket.gethostname()
    return jsonify(data)

@app.route("/orders")
def orders_proxy():
    data = fetch(ORDERS_URL)
    if "error" in data:
        return jsonify({"error": "failed to fetch orders", "detail": data["error"]}), 502
    data["_via_gateway"] = True
    data["_gateway_host"] = socket.gethostname()
    return jsonify(data)

@app.route("/users_orders")
def users_and_orders():
    users = fetch(USERS_URL)
    orders = fetch(ORDERS_URL)
    combined = {"users": users if "error" not in users else {"error": users.get("error")},
                "orders": orders if "error" not in orders else {"error": orders.get("error")},
                "_via_gateway": True,
                "_gateway_host": socket.gethostname()}
    return jsonify(combined)

@app.route("/health")
def health():
    return jsonify({"status":"ok", "service": "gateway", "hostname": socket.gethostname()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8082))
    app.run(host="0.0.0.0", port=port)
