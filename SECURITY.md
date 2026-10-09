# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| `main` (pre-1.0) | Yes — security fixes land on `main` |
| Archived `GNU_correct` / `afyaconnect` | No — see `docs/merge-plan.md` §8 |

## Reporting a vulnerability

Email the maintainers via a private GitHub Security Advisory on this repo
(`Security > Advisories > New draft advisory`). Include:

- affected component (`gnuhealth_*` module, service, docker, script)
- reproduction steps and impact (especially PII/PHI exposure)
- whether the issue touches NDPA-regulated data flows

We aim to acknowledge within 2 business days and ship a fix within 14 days
for High/Critical issues.

## Built-in safeguards (defense in depth)

- Protected clinical fields are wizard-only (`docs/SECURITY.md`).
- Phone redaction on write + 30-day `symptoms_raw` purge.
- Analytics allowlist validation — no PII / free text / hashes in exports.
- `bash scripts/security.sh` runs bandit + secret scan in CI.
- Production secrets via Secret Manager / env — never committed (`.env.example` only).
