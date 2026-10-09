#!/bin/bash
set -eu
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
docker compose -f "$ROOT/docker/docker-compose.yml" up --build -d
echo "AfyaConnect up: http://localhost:${APP_PORT:-8091}"
