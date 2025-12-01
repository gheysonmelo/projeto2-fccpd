import os
import time
from flask import Flask, jsonify
import socket
import psycopg2
from psycopg2.extras import RealDictCursor
import redis

app = Flask(__name__)

# config via env
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_USER = os.environ.get("DB_USER", "demo")
DB_PASS = os.environ.get("DB_PASS", "demopw")
DB_NAME = os.environ.get("DB_NAME", "demo_db")

REDIS_HOST = os.environ.get("REDIS_HOST", "cache")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

CACHE_KEY = "app:latest_message"

def get_redis():
    for i in range(1, 11):
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_connect_timeout=2)
            r.ping()
            return r
        except Exception as e:
            print(f"Redis connect attempt {i} failed: {e}; retrying...")
            time.sleep(1)
    raise RuntimeError("Could not connect to Redis")

def get_db_conn():
    for i in range(1, 11):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME
            )
            return conn
        except Exception as e:
            print(f"DB connect attempt {i} failed: {e}; retrying...")
            time.sleep(1)
    raise RuntimeError("Could not connect to Postgres")

@app.route("/")
def index():
    return jsonify({
        "message": "Service orchestration (web -> cache/db)",
        "hostname": socket.gethostname(),
        "note": "Use /message to get the app message (cached in Redis)."
    })

@app.route("/message")
def message():
    r = get_redis()
    
    cached = r.get(CACHE_KEY)
    if cached:
        return jsonify({
            "source": "cache",
            "message": cached.decode("utf-8")
        })
    
    conn = get_db_conn()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC LIMIT 1;")
            row = cur.fetchone()
            if not row:
                content = "Nenhuma mensagem encontrada."
            else:
                content = row["content"]
    conn.close()
   
    try:
        r.set(CACHE_KEY, content, ex=60)
    except Exception as e:
        print(f"Warning: failed to set cache: {e}")
    return jsonify({
        "source": "db",
        "message": content
    })

@app.route("/clear_cache")
def clear_cache():
    r = get_redis()
    r.delete(CACHE_KEY)
    return jsonify({"cleared": True})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "hostname": socket.gethostname()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
