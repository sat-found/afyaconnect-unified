#!/bin/bash
# 07-pubsub.sh — Triage/dispatch/analytics topics
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" ${REGION:=europe-west1}
echo "[07-pubsub.sh] Triage/dispatch/analytics topics (project=$PROJECT_ID region=$REGION)"
