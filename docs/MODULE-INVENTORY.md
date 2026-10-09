# Module Inventory (reconciled, Gate G0)

## gnuhealth_afya_core
- `gnuhealth.afya.config` (ModelSingleton): `symptoms_raw_ttl_days=30`,
  `k_anonymity_threshold=10`, `region_coarsening_cascade`.
- `gnuhealth.afya.consent_record`: status/actor/scope/notes_category + `party`.
- `gnuhealth.afya.posthoc_consent_task`: party, triage ref, resolved, resolution.
- `gnuhealth.afya.external_ref`: system/external_id ↔ session refs.
- Utils: `redact_phone_numbers()`, `coarsen_region()`, `anonymize_payload()`,
  `validate_analytics_payload()`.

## gnuhealth_afya_access
- `gnuhealth.afya.access_session`: session_id, channel (ussd/sms/voice/web),
  language (en/ha/ff + detected/confidence + Fulfulde fallback flag),
  state (opened→in_progress→triaged→closed/abandoned), linked triage.

## gnuhealth_afya_triage
- `gnuhealth.afya.triage_session`: full state machine
  draft→completed→reviewed→escalated (+cancelled); protected + reviewer fields;
  `purge_expired_symptoms_raw()` cron.
- `gnuhealth.afya.emergency_keyword`: term/language/active (~52 seeded).
- Wizards: `ReviewTriage`, `CreateEvaluationFromTriage`.

## gnuhealth_afya_dispatch
- `gnuhealth.afya.dispatch_request`: 10 states
  candidate→approved→submitted→en_route→arrived→completed (+cancelled/rejected/failed/returned).
- `gnuhealth.afya.kit_template`: 10 seeded templates by event type.
- Wizards: `CreateDispatchCandidate` (stops at candidate — human gate),
  `ApproveDispatch` (dispatcher-only).
- NAERS stub: `accept()` returns mock assignment.

## gnuhealth_afya_diaspora
- `gnuhealth.afya.diaspora_specialist` (5 seeded), `.case_brief`,
  `.consultation_session`, `.specialist_match` (scored).
- Wizards: `MatchSpecialist`, `GenerateCaseBrief`.

## gnuhealth_afya_analytics
- `gnuhealth.afya.analytics_outbox`: `create_from_triage/create_from_dispatch`
  with k-anonymity cascade; schema validation rejects free text/hashes/PII.
- `gnuhealth.afya.resource_snapshot`: periodic facility aggregates.

## mosquito_registration (ported as-is)
- `mosquito.registration` demo registry model.
