#!/bin/bash
# 09 — deploy all 5 FastAPI services to Cloud Run.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" "${REGION:=europe-west1}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
for svc in access-gateway ai-triage-agent fhir-adapter analytics-exporter diaspora-matching; do
  echo "[09] deploying $svc..."
  gcloud run deploy "afya-$svc" --source "$ROOT/services/$svc" \
    --region "$REGION" --project "$PROJECT_ID" --allow-unauthenticated \
    --set-env-vars "AFYA_ENV=prod"
done
