#!/usr/bin/env sh
TARGET="http://web:8080/health"

echo "Cliente iniciado - fazendo requisições para $TARGET"

while true; do
  echo "=== $(date -u +"%Y-%m-%dT%H:%M:%SZ") - solicitando $TARGET ==="
  RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}\n" "$TARGET" || echo "curl-failed")
  echo "$RESPONSE"
  echo ""
  sleep 5
done
