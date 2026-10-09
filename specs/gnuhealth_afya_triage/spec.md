# gnuhealth_afya_triage — Spec

`gnuhealth.afya.triage_session` (Workflow): session_id, start time,
symptoms_raw (+expires_at), clinical_rationale JSON, triage_level
(green/yellow/red/emergency), confidence, human_review_required,
posthoc_consent_needed, consent M2O, reviewer_* (readonly), state.
`complete()` auto-flags emergency for review. `purge_expired_symptoms_raw()`
runs from `data/afya_triage_cron.xml`. `EmergencyKeyword(term, language, active)`.
