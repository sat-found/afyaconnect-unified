#!/bin/bash
# 06 — BigQuery dataset + analytics tables (partitioned, PII-free by contract). Idempotent.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" "${REGION:=europe-west1}"
DS=afya_analytics

bq --project_id="$PROJECT_ID" mk --dataset --location="$REGION" "$DS" 2>/dev/null \
  || echo "dataset $DS exists"
# Outbox mirror: allowlisted categorical columns ONLY (AT-PRIV-01 contract).
bq --project_id="$PROJECT_ID" mk --table "$DS.triage_events" \
  event_id:STRING,event_type:STRING,triage_level:STRING,coarse_region:STRING,\
region_level:STRING,channel:STRING,language:STRING,created_at:TIMESTAMP,k_count:INTEGER \
  --time_partitioning_field=created_at 2>/dev/null || echo 'table triage_events exists'
echo '[06] BigQuery ready'
