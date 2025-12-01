# arquivo: reader/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY read_db.py .

RUN pip install --no-cache-dir psycopg2-binary

CMD ["python", "read_db.py"]
