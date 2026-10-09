# gnuhealth_afya_access — Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| REQ-ACCESS-001 | USSD completes in <4 interactions | AT-ACC-01 |
| REQ-ACCESS-002 | SMS/Voice/Webhooks create AccessSession with channel+language | AT-ACC-01 |
| REQ-ACCESS-003 | Language detection (Gemini) + Fulfulde fallback <70% confidence | AT-LANG-01 |
| REQ-ACCESS-004 | Session links to triage_session on escalation | AT-NAV-01 |
