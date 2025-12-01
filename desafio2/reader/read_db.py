# arquivo: reader/read_db.py
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor

PGHOST = os.environ.get("PGHOST", "localhost")
PGPORT = int(os.environ.get("PGPORT", 5432))
PGUSER = os.environ.get("PGUSER", "demo")
PGPASSWORD = os.environ.get("PGPASSWORD", "demopw")
PGDATABASE = os.environ.get("PGDATABASE", "demo_db")

def main():
    print(f"Conectando em {PGHOST}:{PGPORT} como {PGUSER} ao DB {PGDATABASE}")
    # tenta conexão com retries (DB pode demorar um pouco pra inicializar)
    for attempt in range(1, 11):
        try:
            conn = psycopg2.connect(
                host=PGHOST, port=PGPORT, user=PGUSER, password=PGPASSWORD, dbname=PGDATABASE
            )
            break
        except Exception as e:
            print(f"Tentativa {attempt}: erro ao conectar ({e}). Aguardando 2s...")
            time.sleep(2)
    else:
        print("Não foi possível conectar ao banco. Saindo.")
        return

    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, content, created_at FROM notes ORDER BY id;")
            rows = cur.fetchall()
            if not rows:
                print("Nenhuma nota encontrada.")
            else:
                print("Notas encontradas:")
                for r in rows:
                    print(f"- [{r['id']}] {r['content']} (created_at: {r['created_at']})")

    conn.close()

if __name__ == "__main__":
    main()
