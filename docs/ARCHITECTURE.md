# Architecture — AfyaConnect × GNU Health Unified

## Hybrid layout

```
USSD/SMS/Voice ──► access-gateway (Cloud Run, FastAPI)
                        │ creates gnuhealth.afya.access_session
                        ▼
                ai-triage-agent (Gemini + clinical rules)
                        │ writes gnuhealth.afya.triage_session
                        ▼
        ┌── GNU Health 5.0 / Tryton 7.0 ──────────────────┐
        │  gnuhealth_afya_core      (config singleton,     │
        │   consent, privacy utils)                        │
        │  gnuhealth_afya_access    (multichannel sessions)│
        │  gnuhealth_afya_triage    (state machine +       │
        │   ReviewTriage wizard + keyword detection)       │
        │  gnuhealth_afya_dispatch  (10-state machine +    │
        │   human-gate wizards + NAERS stub)               │
        │  gnuhealth_afya_diaspora  (specialist matching)  │
        │  gnuhealth_afya_analytics (k-anonymity outbox)   │
        └──────────────────────────────────────────────────┘
                        │ BigQuery-safe exports
                        ▼
              analytics-exporter ──► BigQuery ──► Looker Studio
fhir-adapter exposes Patient/Condition/Location reads (<5s, AT-FHIR-01).
```

## Deployment tiers

- **Local/demo:** 3-tier Docker — Nginx (:8091) + uWSGI/Tryton + PostgreSQL 15.
  See `docker/docker-compose.yml` and `docs/DEPLOYMENT.md`.
- **GCP production:** Cloud SQL + 5 Cloud Run services + Pub/Sub + Scheduler
  + BigQuery. Bootstrap via `scripts/setup/01-*.sh … 10-*.sh`.

## Key invariants

1. All custom models: `gnuhealth.afya.*` namespace.
2. Protected clinical fields are wizard-only (see `docs/SECURITY.md`).
3. No PII crosses into analytics; k-anonymity threshold default 10.
4. Every dispatch requires human approval (AT-SAFE-01).
5. `symptoms_raw` redacted on write, purged after 30-day TTL (cron daily).
