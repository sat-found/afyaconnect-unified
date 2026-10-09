# gnuhealth_afya_analytics — Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| REQ-ANALYTICS-001 | Outbox events carry UUIDs only; no PII/free text/hashes | AT-PRIV-01 |
| REQ-ANALYTICS-002 | k-anonymity k≥10 rolling 24h; cascade suppresses tiles | AT-DASH-01 |
| REQ-ANALYTICS-003 | Exporter quality gates reject malformed payloads | AT-PRIV-01 |
| REQ-ANALYTICS-004 | Dashboard freshness <5min | AT-DASH-01 |
