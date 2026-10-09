#!/bin/bash
# 10 — seed Gombe demo data against Cloud SQL via local proxy + Tryton shell.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" "${REGION:=europe-west1}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
python3 "$ROOT/scripts/seed-gombe.py"  # regenerate XML (idempotent by XML ID)
echo 'Start the proxy, then import data/*.xml via SAO (Administration > Import)'
echo "or: trytond-admin -c <conf> -d health --all  # after manual XML load"
cloud-sql-proxy "$PROJECT_ID:$REGION:afya-postgres" --port 5433 &
PROXY=$!
trap 'kill $PROXY 2>/dev/null || true' EXIT
sleep 3
echo "[10] proxy on :5433 (pid $PROXY) — Ctrl-C when done"
wait
