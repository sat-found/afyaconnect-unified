#!/bin/bash
# Seed Gombe demo data: generates XML offline, imports if Tryton is up.
# Usage: bash scripts/seed-gombe.sh [--xml-only]
set -eu
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 scripts/seed-gombe.py
if [ "${1:-}" = "--xml-only" ]; then exit 0; fi
if docker compose -f docker/docker-compose.yml ps tryton 2>/dev/null | grep -q Up; then
  echo "Tryton is running — import data/*.xml via Administration > Import (XML IDs are idempotent)."
  ls -la data/
else
  echo "Tryton not running (XML generated). Start with: docker compose -f docker/docker-compose.yml up -d"
fi
