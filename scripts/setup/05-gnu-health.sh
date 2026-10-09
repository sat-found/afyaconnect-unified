#!/bin/bash
# 05-gnu-health.sh — Tryton Cloud Run deploy
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" ${REGION:=europe-west1}
echo "[05-gnu-health.sh] Tryton Cloud Run deploy (project=$PROJECT_ID region=$REGION)"
