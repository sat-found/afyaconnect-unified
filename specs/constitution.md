# AfyaConnect Constitution (Unified)

**Version:** 2.0 (unified repo) · **Base:** GNU Health 5.0.x / Tryton 7.0 · **Method:** Spec-Driven Development

## Licensing

| Component | License |
|---|---|
| `gnuhealth_afya_*` Tryton modules, `data/`, `specs/` | GPL-3.0-or-later |
| `services/`, `sao-branding/`, `scripts/setup/`, `dashboards/` | Apache-2.0 |

## Gates

| Gate | Condition | Blocks |
|---|---|---|
| G0 | Namespace alignment + config/consent reconciliation + security PoC | Module porting |
| G1 | 6 modules ported; demo path USSD→Triage→Review→Dispatch→Outbox works | Branding/data/docker |
| G2 | All 8 acceptance tests pass; NDPA audit; clinical ≥80%; bias <10% | Production rollout |

## Principles

1. GNU Health is system of record; AI services are stateless.
2. Internal writes via Tryton RPC; external reads via FHIR (read-only MVP).
3. Human-in-the-loop: dispatch + escalations require wizard-enforced approval.
4. Analytics via outbox pattern — no GCP SDK inside Tryton.
5. No raw model reasoning stored — validated structured JSON rationale only.
6. Privacy by design: redaction on write, TTL purge, k-anonymity, no free text in exports.

## Demo truthfulness

Live = real integration (sandbox where applicable). Stubbed/Simulated must be
disclosed. NAERS + diaspora audio/chat are stubs in MVP.
