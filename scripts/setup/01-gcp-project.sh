#!/bin/bash
# 01 — project + APIs + region. Idempotent.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" "${REGION:=europe-west1}"
gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com sqladmin.googleapis.com \
  secretmanager.googleapis.com pubsub.googleapis.com cloudscheduler.googleapis.com \
  bigquery.googleapis.com --project="$PROJECT_ID"
echo "[01] project $PROJECT_ID ready (region $REGION)"
