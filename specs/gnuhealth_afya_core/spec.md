# gnuhealth_afya_core — Spec

## Models
- `gnuhealth.afya.config(ModelSingleton, ModelView)`: `symptoms_raw_ttl_days`,
  `k_anonymity_threshold`, `region_coarsening_cascade` (JSON cascade definition).
- `gnuhealth.afya.consent_record`: selections per REQ-CORE-002 + `party` M2O.
- `gnuhealth.afya.posthoc_consent_task`: party, triage_session M2O,
  resolved bool, resolution_consent M2O (readonly except wizard).
- `gnuhealth.afya.external_ref`: system/external_id + session refs.

## Guards
Protected-field pattern originates here and is reused: `write()` checks context
flags; admin bypass via group membership check.

## Seed
`data/afya_config.xml`: singleton id=1. Groups in
`gnuhealth_afya_core/security/access_rights.xml`.
