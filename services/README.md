# Cloud Run services (FastAPI, stateless)

| Service | Endpoints |
|---|---|
| access-gateway | POST /ussd /sms /voice, GET / (demo UI), GET /healthz |
| ai-triage-agent | POST /triage, GET /healthz |
| fhir-adapter | GET /fhir/{Patient,Condition,Location}, GET /healthz |
| analytics-exporter | POST /export, GET /healthz |
| diaspora-matching | POST /match, GET /healthz |

Local run: `uvicorn main:app --port 8080` inside any service dir (repo root on
sys.path for `common.py`). Deploy: `bash scripts/setup/09-deploy-services.sh`.
