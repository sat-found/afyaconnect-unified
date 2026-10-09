# AfyaConnect × GNU Health HMIS — Unified Platform

> AI-assisted emergency triage, dispatch, and multilingual access (USSD · SMS · Voice)
> on GNU Health 5.0.x / Tryton 7.0 — one repo, one namespace, one demo path.

[![lint](https://github.com/sat-found/afyaconnect-unified/actions/workflows/lint.yaml/badge.svg)](https://github.com/sat-found/afyaconnect-unified/actions/workflows/lint.yaml)
[![security](https://github.com/sat-found/afyaconnect-unified/actions/workflows/security.yaml/badge.svg)](https://github.com/sat-found/afyaconnect-unified/actions/workflows/security.yaml)
[![tests](https://github.com/sat-found/afyaconnect-unified/actions/workflows/tests.yaml/badge.svg)](https://github.com/sat-found/afyaconnect-unified/actions/workflows/tests.yaml)
![Tryton 7.0](https://img.shields.io/badge/Tryton-7.0-0d9488)
![GNU Health 5.0](https://img.shields.io/badge/GNU_Health-5.0-0f766e)
![Licenses](https://img.shields.io/badge/licenses-GPL--3.0_%2B_Apache--2.0-blue)

Single source of truth combining GNU Health infrastructure rigor with AfyaConnect
product features. All custom models live under the `gnuhealth.afya.*` namespace;
GNU Health stays the system of record while stateless FastAPI services handle
citizen access, triage inference, FHIR reads, analytics export, and diaspora matching.

---

## 30-second tour

```bash
git clone https://github.com/sat-found/afyaconnect-unified.git && cd afyaconnect-unified
cp .env.example .env            # dev defaults only — never commit real secrets
make test                       # 31 tests, no server needed
make up                         # Nginx :8091 + Tryton + Postgres
make seed                       # Gombe demo data (10 facilities, 200 patients, 20 workers, 52 keywords)
```

Then open **http://localhost:8091** (branded SAO login) and, in another terminal,
the services demo path:

```bash
make services-up                 # gateway :8081, triage :8082, fhir :8083, analytics :8084, diaspora :8085
curl -s -X POST localhost:8081/ussd -H 'Content-Type: application/json' \
  -d '{"channel":"ussd","text":"Ba iya numfashi, ciwon kirji"}' | python3 -m json.tool
```

Or try the click-through demo UI at **http://localhost:8081** (EN · HA · FF).

---

## How it fits together

```
USSD/SMS/Voice ──► access-gateway :8081 ──► ai-triage-agent :8082
   (language detect + Fulfulde    │ forwards (TRIAGE_AGENT_URL),
    fallback + phone redaction)   │ local-fallback if unreachable
                                  ▼
                   ┌── GNU Health 5.0 / Tryton 7.0 ────────────────┐
                   │ gnuhealth_afya_core      config singleton,    │
                   │  consent, privacy utils, 5 RBAC groups        │
                   │ gnuhealth_afya_access    multichannel sessions│
                   │ gnuhealth_afya_triage    state machine,       │
                   │  ReviewTriage wizard, keyword detection       │
                   │ gnuhealth_afya_dispatch  10-state machine,    │
                   │  human-gate wizards, NAERS stub               │
                   │ gnuhealth_afya_diaspora  specialist matching  │
                   │ gnuhealth_afya_analytics k-anonymity outbox   │
                   └──────────────────────────────────────────────┘
                                  │ BigQuery-safe exports only
                                  ▼
                   analytics-exporter :8084 ──► BigQuery ──► Looker Studio
fhir-adapter :8083 exposes read-only Patient/Condition/Location (<5s, AT-FHIR-01).
diaspora-matching :8085 scores specialists (audio-only MVP).
```

Full reference: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) ·
service endpoints: [`docs/API.md`](docs/API.md) ·
deployment: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

---

## Repository layout

| Path | What lives there |
|---|---|
| `gnuhealth/` | 7 Tryton modules (`gnuhealth_afya_*` + `mosquito_registration`), every view with real form/tree arch |
| `specs/` | Constitution, design spec, model inventory, per-module requirements + spec, OpenSpec workflow |
| `sao-branding/` | Premium teal theme, dark mode, branded login hero, triage pills, logo |
| `docker/` | Production-grade 3-tier stack (Nginx + uWSGI/Tryton + PostgreSQL 15, all pinned) |
| `services/` | 5 FastAPI microservices + shared `common.py` + local compose (ports 8081–8085) |
| `scripts/` | `lint/security/test/autopep8`, `seed-gombe`, GCP bootstrap `setup/01–10`, `operational/` helpers |
| `data/` | Idempotent seed XML (facilities, patients, workers, 52 emergency keywords) |
| `tests/` | Unit + integration (`make test`) + 8 acceptance suites (`tests/acceptance/`) |
| `dashboards/` | Looker Studio configs (surveillance + emergency analytics) |
| `docs/` | merge-plan, architecture, namespace, security, deployment, migration, module inventory, API |

---

## Developer workflow

```bash
make help            # all targets
make test            # fast suite — must pass before every commit
make lint            # flake8 + XML validation
make security        # bandit + secret scan
make xml-check       # all 16+ Tryton/seed XML files parse + views resolve
```

Conventions (enforced in CI + `CONTRIBUTING.md`):

- **Namespace** — every model is `gnuhealth.afya.*` (see `docs/NAMESPACE-ALIGNMENT.md`).
- **Human gates** — dispatch and triage escalation require wizard approval; protected
  fields (`clinical_rationale`, `triage_level`, `triage_confidence`, `symptoms_raw`,
  dispatch assignments) reject direct writes (`docs/SECURITY.md`).
- **Privacy by design (NDPA)** — phone redaction on write, 30-day `symptoms_raw` purge
  cron, k-anonymity cascade (sector→lga→state→suppressed at k=10), allowlisted analytics
  payloads only. Report issues privately — see `SECURITY.md`.
- **Tests** — pure logic lives in `afya_utils` / `triage_logic` / `dispatch_logic` /
  `services/common.py` so it runs without a Tryton server; view↔model consistency is
  asserted by `tests/unit/test_views.py`.

---

## Gates & roadmap

| Gate | Means | Status |
|---|---|---|
| G0 | Namespace + config/consent reconciliation + security PoC | ✅ done |
| G1 | 6 modules ported; USSD→Triage→Review→Dispatch→Outbox demo works | ✅ done (try it above) |
| G2 | All 8 acceptance tests, NDPA audit, clinical ≥80%, bias <10% | 🔲 clinical run pending |

Planned: live NAERS + Africa's Talking sandbox wiring, video consults (post-MVP),
expanded security roles (5 → 9). See [`docs/merge-plan.md`](docs/merge-plan.md) §9–§12
and [`CHANGELOG.md`](CHANGELOG.md).

---

## License

- Tryton modules (`gnuhealth/`, `data/`, `specs/`): **GPL-3.0-or-later**
- Services, branding, setup scripts, dashboards: **Apache-2.0**

See [`LICENSE`](LICENSE) and [`.reuse/dep5`](.reuse/dep5). Security reports:
[`SECURITY.md`](SECURITY.md). Contributing: [`CONTRIBUTING.md`](CONTRIBUTING.md).
