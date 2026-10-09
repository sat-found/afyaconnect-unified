# gnuhealth_afya_dispatch — Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| REQ-DISP-001 | 10 states: candidate→approved→submitted→en_route→arrived→completed (+cancelled/rejected/failed/returned) | AT-DISP-01 |
| REQ-DISP-002 | CreateDispatchCandidate stops at candidate (human gate) | AT-SAFE-01 |
| REQ-DISP-003 | ApproveDispatch dispatcher-only; timer measured | AT-SAFE-01 |
| REQ-DISP-004 | 10 kit templates by event type; recommendations from triage | demo |
| REQ-DISP-005 | NAERS stub accepts + returns mock assignment (disclosed stub) | demo |
