# GNU Health Model Inventory (Unified, G0 approved reference)

**Platform:** GNU Health 5.0.x / Tryton 7.0. **Task:** T002.

## Upstream models we extend / link

| Model | Use |
|---|---|
| `party.party` | consent + posthoc tasks link here (not `gnuhealth.patient`) — victims may be unregistered |
| `gnuhealth.patient` | created/linked by `CreateEvaluationFromTriage` wizard |
| `gnuhealth.patient.evaluation` | target of triage→evaluation wizard (ICD-10 codes) |
| `gnuhealth.support_request` | extended pattern for `gnuhealth.afya.dispatch_request` |
| `gnuhealth.institution` | Gombe facilities seed target; `resource_snapshot` aggregates |
| `ir.cron` | daily `symptoms_raw` purge job |
| `res.group` / `ir.ui.menu` | 5 Afya RBAC groups; menu `GNU Health → AfyaConnect` |

## Custom models (all `gnuhealth.afya.*`)

core: config (Singleton), consent_record, posthoc_consent_task, external_ref ·
access: access_session · triage: triage_session, emergency_keyword ·
dispatch: dispatch_request, kit_template · diaspora: diaspora_specialist,
case_brief, consultation_session, specialist_match ·
analytics: analytics_outbox, resource_snapshot.

## Verification

```bash
docker compose -f docker/docker-compose.yml exec tryton python3 -c "
from trytond.pool import Pool; p=Pool('health'); p.init()
for m in ['gnuhealth.afya.triage_session','gnuhealth.afya.dispatch_request']: print(m, p.get(m).__name__)"
```
