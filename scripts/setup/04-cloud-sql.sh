#!/bin/bash
# 04 — Cloud SQL Postgres 15 (private IP) + database. Idempotent.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" "${REGION:=europe-west1}"
INST=afya-postgres

if ! gcloud sql instances describe "$INST" --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud sql instances create "$INST" --project="$PROJECT_ID" \
    --database-version=POSTGRES_15 --tier=db-custom-2-7680 --region="$REGION" \
    --no-assign-ip --network=default --backup-start-time=02:00
fi
gcloud sql databases create health --instance="$INST" --project="$PROJECT_ID" 2>/dev/null \
  || echo 'database health exists'
gcloud sql users set-password postgres --instance="$INST" --project="$PROJECT_ID" \
  --prompt-for-password
echo '[04] Cloud SQL ready'
