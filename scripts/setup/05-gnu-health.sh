#!/bin/bash
# 05 — Tryton on Cloud Run (from docker/Dockerfile.gnuhealth). Idempotent redeploy.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" "${REGION:=europe-west1}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
gcloud run deploy afya-tryton --project="$PROJECT_ID" --region="$REGION" \
  --source "$ROOT" --dockerfile=docker/Dockerfile.gnuhealth \
  --service-account="afya-tryton@$PROJECT_ID.iam.gserviceaccount.com" \
  --add-cloudsql-instances="$PROJECT_ID:$REGION:afya-postgres" \
  --set-env-vars=GNUHEALTH_DB_HOST=/cloudsql/"$PROJECT_ID:$REGION:afya-postgres",GNUHEALTH_DB_NAME=health \
  --set-secrets=GNUHEALTH_DB_PASSWORD=afya-db-password:latest,TRYTON_ADMIN_PASSWORD=afya-tryton-admin:latest \
  --cpu=2 --memory=4Gi --min-instances=1 --max-instances=5 --no-allow-unauthenticated
echo '[05] Tryton deployed (private ingress; front via LB)'
