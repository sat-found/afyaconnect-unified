# Security (T012–T017 PoC → T043–T045 applied)

## Groups (5)

| XML ID | Name | Capabilities |
|---|---|---|
| `gnuhealth_afya_core.group_afya_admin` | Afya Administrator | full; bypasses protected-field guard |
| `gnuhealth_afya_core.group_clinical_reviewer` | Afya Clinical Reviewer | ReviewTriage wizard, `reviewed`/`escalated` transitions |
| `gnuhealth_afya_core.group_dispatcher` | Afya Dispatcher | ApproveDispatch wizard, dispatch transitions |
| `gnuhealth_afya_core.group_diaspora_coordinator` | Afya Diaspora Coordinator | specialist matching wizards |
| `gnuhealth_afya_core.group_dashboard_viewer` | Afya Dashboard Viewer | read analytics outbox / snapshots |

## Four enforced mechanisms (PoC-validated on Tryton 7.0)

1. **Protected-field guard** — `write()` override rejects direct writes to
   `clinical_rationale`, `triage_level`, `triage_confidence`, `symptoms_raw`
   unless context `_afya_allow_protected_write` or admin.
2. **Wizard-only reviewer fields** — `reviewer_decision/notes/timestamp` require
   context `_afya_review_wizard` set only by `ReviewTriage.transition_review`.
3. **Workflow transitions** — `@Workflow.transition(...)` on every state change;
   illegal jumps raise.
4. **Group-restricted buttons** — every `*.xml` button carries
   `groups="...group_clinical_reviewer,...group_dispatcher"` as appropriate.

Apply the triage-module pattern verbatim to all modules (T044–T045).
