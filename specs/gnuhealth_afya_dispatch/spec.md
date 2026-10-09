# gnuhealth_afya_dispatch — Spec

`gnuhealth.afya.dispatch_request` extends the `gnuhealth.support_request`
pattern: triage M2O, event_type, priority, facility M2O (gnuhealth.institution),
state machine + protected location/ETA fields (wizard-only),
`ApproveDispatch`/`CreateDispatchCandidate` wizards, NAERS stub client.
`gnuhealth.afya.kit_template`: event_type, items JSON, active.
