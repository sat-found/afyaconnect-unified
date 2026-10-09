#!/bin/bash
# Live end-to-end demo: boots the 5 FastAPI services, runs the automated
# acceptance subset (Gates G1/G2), prints pipeline timings. No Docker needed.
# Usage: bash scripts/e2e-demo.sh [--no-test]
set -eu
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT/services:${PYTHONPATH:-}"
LOGDIR="${TMPDIR:-/tmp}/afya-e2e-logs"
mkdir -p "$LOGDIR"
GW=8081 TA=8082 FHIR=8083 AN=8084 DIA=8085
PIDS=""

cleanup() {
  [ -n "$PIDS" ] && kill $PIDS 2>/dev/null || true
  wait 2>/dev/null || true
}
trap cleanup EXIT

start() {  # $1=service dir $2=port [$3=extra env assignments]
  if [ -n "${3:-}" ]; then export "$3"; fi
  (cd "$ROOT/services/$1" && exec nohup python3 -m uvicorn main:app \
    --port "$2" --log-level warning >"$LOGDIR/$1.log" 2>&1) &
  PIDS="$PIDS $!"
  if [ -n "${3:-}" ]; then unset "${3%%=*}"; fi
  echo "started $1 on :$2 (log $LOGDIR/$1.log)"
}

wait_for() {  # $1=port $2=name
  for _ in $(seq 1 60); do
    if curl -sf "http://localhost:$1/healthz" >/dev/null 2>&1; then
      echo "$2 :$1 up"; return 0
    fi
    sleep 0.5
  done
  echo "FATAL: $2 on :$1 did not start; log:" >&2
  tail -20 "$LOGDIR/$2.log" >&2 || true
  exit 1
}

# Triage agent first: the gateway forwards to it when TRIAGE_AGENT_URL is set.
start ai-triage-agent $TA
wait_for $TA ai-triage-agent
start access-gateway $GW "TRIAGE_AGENT_URL=http://localhost:$TA"
start fhir-adapter $FHIR
start analytics-exporter $AN
start diaspora-matching $DIA
disown -a 2>/dev/null || true

wait_for $GW access-gateway
wait_for $FHIR fhir-adapter
wait_for $AN analytics-exporter
wait_for $DIA diaspora-matching

echo "--- pipeline: USSD(Hausa) -> triage -> review routing ---"
curl -s -X POST "http://localhost:$GW/ussd" -H 'Content-Type: application/json' \
  -d '{"channel":"ussd","text":"Ba iya numfashi, ciwon kirji 08031234567"}' | python3 -m json.tool

echo "--- FHIR read latency header ---"
curl -s -D - -o /dev/null "http://localhost:$FHIR/fhir/Patient" | grep -i -E "HTTP|X-Read-Latency" || true

if [ "${1:-}" != "--no-test" ]; then
  echo "--- acceptance suite (live) ---"
  python3 -m pytest tests/acceptance/test_at_live.py -v
fi
echo "E2E DEMO OK"
