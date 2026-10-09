#!/bin/bash
# 06-bigquery.sh — Datasets + TTL views
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" ${REGION:=europe-west1}
echo "[06-bigquery.sh] Datasets + TTL views (project=$PROJECT_ID region=$REGION)"
