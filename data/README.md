# Seed data (`data/`)

Offline-generated, idempotent (XML IDs), synthetic — no real PII.

| File | Records |
|---|---|
| `gombe_facilities.xml` | 10 flagship Gombe facilities (extend to 50 in production seed) |
| `gombe_patients.xml` | 200 synthetic patients |
| `gombe_workers.xml` | 20 health workers |
| `emergency_keywords.xml` | ~52 EN/HA/FF emergency keywords |
| `afya_config.xml` | moved into `gnuhealth_afya_core/data/` (singleton) — see module |
| `afya_triage_cron.xml` | moved into `gnuhealth_afya_triage/data/` — see module |

Generate: `python3 scripts/seed-gombe.py` · Import: `bash scripts/seed-gombe.sh`.
