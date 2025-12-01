CREATE TABLE IF NOT EXISTS messages (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

INSERT INTO messages (content) VALUES ('Mensagem inicial: sistema pronto.');
INSERT INTO messages (content) VALUES ('Flamengo — Tetracampeão da Libertadores 2025!');
