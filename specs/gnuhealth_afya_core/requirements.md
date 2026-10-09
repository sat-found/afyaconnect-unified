# gnuhealth_afya_core — Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| REQ-CORE-001 | Config is ModelSingleton (id=1): ttl=30, k=10, cascade | G0 T005–T007 |
| REQ-CORE-002 | Consent model: 6 statuses, 4 actors, 4 scopes, 5 note categories; party.party link; no free text | AT-PRIV-01 |
| REQ-CORE-003 | PostHocConsentTask tracks deferred consent → resolution | AT-PRIV-01 |
| REQ-CORE-004 | `redact_phone_numbers()` covers 0XXXXXXXXXX +234 patterns incl. Hausa/Fulfulde transliterations | AT-PRIV-01 |
| REQ-CORE-005 | `coarsen_region()` cascade sector→lga→state→suppressed at k=10 | AT-DASH-01 |
| REQ-CORE-006 | `anonymize_payload()` strips PII/hashes/free text; validator rejects violations | AT-PRIV-01 |
| REQ-CORE-007 | 5 RBAC groups seeded with permission matrix | AT-SAFE-01 |
