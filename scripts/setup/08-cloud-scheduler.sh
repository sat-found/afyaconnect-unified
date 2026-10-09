#!/bin/bash
# 08 — Cloud Scheduler: daily outbox sweep + snapshot ping. Idempotent.
# NOTE: services expose /healthz today; point these jobs at export/snapshot
# handlers once implemented (see specs/gnuhealth_afya_analytics/spec.md).
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" "${REGION:=europe-west1}"
SA="afya-exporter@$PROJECT_ID.iam.gserviceaccount.com"

job() {  # $1=name $2=schedule $3=uri-path
  gcloud scheduler jobs create http "$1" --project="$PROJECT_ID" --location="$REGION" \
    --schedule="$2" --uri="https://afya-analytics-exporter-a.run.app$3" \
    --http-method=GET --oidc-service-account-email="$SA" 2>/dev/null \
    || gcloud scheduler jobs update http "$1" --project="$PROJECT_ID" \
      --location="$REGION" --schedule="$2" \
      --uri="https://afya-analytics-exporter-a.run.app$3" >/dev/null
}
job afya-daily-export '0 1 * * *' '/healthz'
job afya-snapshot-ping '*/15 * * * *' '/healthz'
echo '[08] Scheduler ready'
