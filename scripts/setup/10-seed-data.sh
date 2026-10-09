#!/bin/bash
# 10-seed-data.sh — Gombe seed via container job
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" ${REGION:=europe-west1}
echo "[10-seed-data.sh] Gombe seed via container job (project=$PROJECT_ID region=$REGION)"
