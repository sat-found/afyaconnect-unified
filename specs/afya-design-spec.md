# Afya Design Spec (consolidated reference)

## Flows

### USSD triage (<4 interactions, AT-ACC-01)
`1 language → 2 symptoms → 3 confirm → done`. Gateway creates
`access_session` (opened→in_progress), calls triage-agent, writes
`triage_session` (draft), runs keyword detection independent of
language confidence; Fulfulde fallback <70% confidence (AT-LANG-01).

### Review gate (AT-SAFE-01)
Emergency triage sets `human_review_required`. `ReviewTriage` wizard is the
ONLY writer of reviewer fields; `reviewed`/`escalated` transitions follow.
Protected fields (`clinical_rationale`, `triage_level`, `triage_confidence`,
`symptoms_raw`) reject direct writes.

### Dispatch gate (AT-SAFE-01, AT-DISP-01)
`CreateDispatchCandidate` stops at `candidate`. `ApproveDispatch`
(dispatcher group only) → approved→submitted→en_route→arrived→completed.
Windows: A <60s candidate creation, B <30s escalation→candidate,
D <90s approval→submission (human component disclosed).

### Privacy pipeline (AT-PRIV-01)
Redact phones on write → TTL 30d purge cron → analytics outbox with
k-anonymity cascade (sector→lga→state→suppressed) → exporter quality gates
→ BigQuery → <5min dashboard freshness (AT-DASH-01).

### Clinical validation (AT-NAV-01)
40 scenarios; ≥80% concordance, ≥95% red-flag sensitivity, RAG top-3 relevance;
<10% cross-language variance; Cohen κ ≥0.80 inter-rater.
