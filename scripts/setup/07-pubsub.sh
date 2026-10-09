#!/bin/bash
# 07 — Pub/Sub topics + exporter subscription. Idempotent.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}"

topic() {
  gcloud pubsub topics create "$1" --project="$PROJECT_ID" 2>/dev/null \
    || echo "topic $1 exists"
}
topic afya-triage-events
topic afya-dispatch-events
topic afya-export-requests
gcloud pubsub subscriptions create afya-exporter-sub \
  --topic=afya-export-requests --project="$PROJECT_ID" \
  --ack-deadline=60 2>/dev/null || echo 'subscription exists'
echo '[07] Pub/Sub ready'
