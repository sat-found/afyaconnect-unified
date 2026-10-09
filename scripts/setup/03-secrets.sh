#!/bin/bash
# 03-secrets.sh — Secret Manager entries
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" ${REGION:=europe-west1}
echo "[03-secrets.sh] Secret Manager entries (project=$PROJECT_ID region=$REGION)"
