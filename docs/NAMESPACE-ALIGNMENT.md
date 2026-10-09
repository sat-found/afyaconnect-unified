# Namespace Alignment (Gate G0 — T001–T004, T011)

**Decision: adopt `gnuhealth.afya.*` for every custom model `__name__`.**
Module (directory) names: `gnuhealth_afya_*` (valid Tryton/python identifiers).

## Rationale

- Intuitive Tryton menu placement (GNU Health → AfyaConnect).
- Standard `gnuhealth.` domain prefix; easier discovery than `z_health_afya.*`.
- Source prototype (`afyaconnect`) already used `gnuhealth.afya.*` model names —
  only directory/module names change (`z_health_afya_*` → `gnuhealth_afya_*`).

## Mapping

| Legacy module dir | Unified module dir | Model names (unchanged) |
|---|---|---|
| `z_health_afya_core` | `gnuhealth_afya_core` | `gnuhealth.afya.config`, `.consent_record`, `.posthoc_consent_task`, `.external_ref` |
| `z_health_afya_access` | `gnuhealth_afya_access` | `gnuhealth.afya.access_session` |
| `z_health_afya_triage` | `gnuhealth_afya_triage` | `gnuhealth.afya.triage_session`, `.emergency_keyword`, `.review_triage(.start)` |
| `z_health_afya_dispatch` | `gnuhealth_afya_dispatch` | `gnuhealth.afya.dispatch_request`, `.kit_template` |
| `z_health_afya_diaspora` | `gnuhealth_afya_diaspora` | `gnuhealth.afya.diaspora_specialist`, `.case_brief`, `.consultation_session`, `.specialist_match` |
| `z_health_afya_analytics` | `gnuhealth_afya_analytics` | `gnuhealth.afya.analytics_outbox`, `.resource_snapshot` |

Wizard XML IDs migrate `z_health_afya_*.*` → `gnuhealth_afya_*.*`
(e.g. `z_health_afya_triage.wizard_review_triage` →
`gnuhealth_afya_triage.wizard_review_triage`).

## Consent decision (T008–T011)

`gnuhealth.afya.consent_record` links to **`party.party`** (not `gnuhealth.patient`):
emergency victims may be unconscious/unregistered; guardians, proxies and
bystanders are parties, not patients. Fields: `consent_status`,
`consent_actor`, `consent_scope`, `notes_category` (categorical — no free text).
`PostHocConsentTask` tracks deferred consent and links back to the triage session.

## Config decision (T005–T007)

`gnuhealth.afya.config` is a **`ModelSingleton`** (one row, id=1):
drops the redundant `name` field; adds `region_coarsening_cascade` alongside
`symptoms_raw_ttl_days` (30) and `k_anonymity_threshold` (10).
Migration: `ALTER TABLE z_health_afya_config RENAME TO gnuhealth_afya_config`
+ `ir.model` updates — see `docs/MIGRATION-GUIDE.md`.
