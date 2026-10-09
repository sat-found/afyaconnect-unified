# gnuhealth_afya_triage — Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| REQ-TRIAGE-001 | State machine draft→completed→reviewed→escalated (+cancelled), guarded transitions | AT-SAFE-01 |
| REQ-TRIAGE-002 | Protected fields wizard/admin-only | AT-SAFE-01 |
| REQ-TRIAGE-003 | ReviewTriage wizard only writer of reviewer fields | AT-SAFE-01 |
| REQ-TRIAGE-004 | Clinical rationale validated JSON (§5.1 schema) on create/write | AT-NAV-01 |
| REQ-TRIAGE-005 | ~52 multilingual keywords fire independent of language confidence | AT-LANG-01 |
| REQ-TRIAGE-006 | symptoms_raw redacted on create, TTL purge via ir.cron daily | AT-PRIV-01 |
| REQ-TRIAGE-007 | CreateEvaluationFromTriage → gnuhealth.patient.evaluation + ICD-10 | AT-NAV-01 |
