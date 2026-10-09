# Service API reference

Interactive docs: each service serves Swagger UI at `/docs` and ReDoc at `/redoc`.

| Service | Local port | Key endpoints |
|---|---|---|
| access-gateway | 8081 | `POST /ussd` · `POST /sms` · `POST /voice` · `GET /` (demo UI) · `GET /healthz` |
| ai-triage-agent | 8082 | `POST /triage` · `GET /healthz` |
| fhir-adapter | 8083 | `GET /fhir/{Patient,Condition,Location}` · `GET /healthz` |
| analytics-exporter | 8084 | `POST /export` · `GET /healthz` |
| diaspora-matching | 8085 | `POST /match` · `GET /healthz` |

## End-to-end intake example

```bash
docker compose -f services/docker-compose.services.yml up --build -d

# USSD intake in Hausa (gateway forwards to ai-triage-agent, falls back locally)
curl -s -X POST localhost:8081/ussd \
  -H 'Content-Type: application/json' \
  -d '{"channel":"ussd","text":"Ba iya numfashi, ciwon kirji"}' | python3 -m json.tool

# Direct triage
curl -s -X POST localhost:8082/triage \
  -H 'Content-Type: application/json' \
  -d '{"text":"patient unconscious, severe bleeding"}' | python3 -m json.tool

# Analytics export (k-anonymity enforced; k_count<10 non-suppressed is rejected)
curl -s -X POST localhost:8084/export \
  -H 'Content-Type: application/json' \
  -d '{"event_id":"triage-1","event_type":"triage","triage_level":"red",
       "coarse_region":"gombe","region_level":"lga","channel":"ussd",
       "language":"ha","created_at":"2026-01-01","k_count":15}'

# FHIR read (note X-Read-Latency-ms header; AT-FHIR-01 requires <5s)
curl -si localhost:8083/fhir/Patient | head -20
```

## Conventions

- Every response carries `X-Request-ID` (echoed if the client sends one).
- Errors never break intake: the gateway degrades to `local-fallback` triage
  and marks `triage.source` accordingly.
- CORS allows the SAO origin (`:8091`) plus local dev (`:3000`).
- Env: `TRIAGE_AGENT_URL` (default empty → local fallback),
  `TRIAGE_TIMEOUT_S` (default 8).
