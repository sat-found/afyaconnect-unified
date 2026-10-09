# gnuhealth_afya_analytics — Spec

`analytics_outbox` (event_id UUID, event_type, coarse_region, triage_level,
channel, language, created_at, exported bool) with
`create_from_triage/create_from_dispatch` applying the cascade;
`resource_snapshot` (facility, beds_available, ambulances, timestamp).
Schema validation: allowlist of categorical fields only.
