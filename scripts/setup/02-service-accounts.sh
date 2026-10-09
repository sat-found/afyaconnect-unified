#!/bin/bash
# 02-service-accounts.sh — Least-privilege SAs
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" ${REGION:=europe-west1}
echo "[02-service-accounts.sh] Least-privilege SAs (project=$PROJECT_ID region=$REGION)"
