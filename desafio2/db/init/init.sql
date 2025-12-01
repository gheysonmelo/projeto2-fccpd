-- arquivo: db/init/init.sql
-- esse script roda apenas na primeira inicialização do volume (quando o DB é criado)
CREATE TABLE IF NOT EXISTS notes (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

INSERT INTO notes (content) VALUES ('Primeira nota persistida');
INSERT INTO notes (content) VALUES ('Flamengo — Tetracampeão da Libertadores 2025');
