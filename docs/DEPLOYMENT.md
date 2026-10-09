# Deployment

## Local (Docker, 3-tier)

```bash
cp docker/gnuhealth/trytond.conf.example docker/gnuhealth/trytond.conf
# edit POSTGRES_PASSWORD / TRYTON_* secrets
docker compose -f docker/docker-compose.yml up --build -d
bash scripts/operational/status.sh
# SAO via http://localhost:8091
bash scripts/seed-gombe.sh   # demo data
```

Services: `nginx` (:8091 → sao + jsonrpc), `tryton` (uWSGI, :8000),
`postgres` (15-alpine, volume `pgdata`). Healthchecks on all three.

## GCP production (scripts/setup 01–10)

1. `01-gcp-project.sh` — project + APIs + region
2. `02-service-accounts.sh` — least-privilege SAs
3. `03-secrets.sh` — Secret Manager (db, tryton admin, gemini key)
4. `04-cloud-sql.sh` — Postgres 15 + private IP
5. `05-gnu-health.sh` — Tryton on Cloud Run (from `docker/Dockerfile.gnuhealth`)
6. `06-bigquery.sh` — datasets + row-level TTL views
7. `07-pubsub.sh` — triage/dispatch/analytics topics
8. `08-cloud-scheduler.sh` — daily purge + snapshot jobs
9. `09-deploy-services.sh` — all 5 FastAPI services
10. `10-seed-data.sh` — Gombe seed via Proteus

Acceptance: fresh-project bootstrap <2h (T060).
