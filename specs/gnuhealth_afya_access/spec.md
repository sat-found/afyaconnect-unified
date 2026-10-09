# gnuhealth_afya_access — Spec

`gnuhealth.afya.access_session`: session_id, channel (ussd/sms/voice/web),
language (en/ha/ff), detected_language + confidence, fulfulde_fallback bool,
state (opened→in_progress→triaged→closed/abandoned), triage_session M2O,
timestamps. Gateway writes sessions; triage-agent advances to `triaged`.
