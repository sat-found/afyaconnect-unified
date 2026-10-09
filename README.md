# AfyaConnect × GNU Health HMIS — Unified Platform

AfyaConnect × GNU Health HMIS: Unified product platform. GNU Health 5.0.x (Tryton 7.0)
with AI-assisted emergency triage, dispatch, and multilingual access via voice/SMS/USSD.

Single source of truth combining GNU Health infrastructure rigor + AfyaConnect product features.

## Quick start

```bash
# 1. Local 3-tier stack (Nginx + uWSGI/Tryton + PostgreSQL)
cp docker/gnuhealth/trytond.conf.example docker/gnuhealth/trytond.conf  # then edit secrets
docker compose -f docker/docker-compose.yml up --build

# App: http://localhost:8091  |  SAO web client via Nginx
# 2. Seed Gombe demo data (50 facilities, 200 patients, 20 workers, 52 keywords)
bash scripts/seed-gombe.sh

# 3. Run unit tests (no Tryton server required — pure-logic suite)
python3 -m pytest tests/unit -q
```

## Repository layout

| Path | Contents |
|---|---|
| `gnuhealth/` | 6 Afya Tryton modules (`gnuhealth_afya_*`, namespace `gnuhealth.afya.*`) + `mosquito_registration` |
| `specs/` | Constitution + per-module requirements/spec (spec-driven development) |
| `sao-branding/` | Premium teal theme, dark mode, logo, login customization |
| `docker/` | Production-grade 3-tier stack: Nginx + uWSGI + PostgreSQL |
| `services/` | 5 Cloud Run microservices (FastAPI): gateway, triage-agent, fhir-adapter, analytics-exporter, diaspora-matching |
| `scripts/` | Lint/security/test + GCP bootstrap (01–10) + operational helpers |
| `data/` | Seed XML: config, cron, Gombe facilities/patients/workers, emergency keywords |
| `tests/` | Unit + integration + acceptance (8 AT suites) |
| `dashboards/` | Looker Studio configs (surveillance + emergency analytics) |
| `docs/` | merge-plan, ARCHITECTURE, NAMESPACE-ALIGNMENT, SECURITY, DEPLOYMENT, MODULE-INVENTORY, MIGRATION-GUIDE |

## Namespace decision

All custom models live under `gnuhealth.afya.*` (e.g. `gnuhealth.afya.triage_session`).
See `docs/NAMESPACE-ALIGNMENT.md`.

## Security

5 RBAC groups, method-level guards on protected fields, wizard-only mutations,
group-restricted buttons. See `docs/SECURITY.md`.

## Privacy (NDPA)

Phone redaction before `symptoms_raw` storage, 30-day TTL purge cron,
k-anonymity cascade, no free text / hashes / PII in analytics exports.

## License

Tryton modules: GPL-3.0-or-later. Cloud Run services & branding: Apache-2.0. See `LICENSE`.
