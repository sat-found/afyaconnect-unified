#!/bin/bash
# 04-cloud-sql.sh — Postgres 15 private-IP instance
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" ${REGION:=europe-west1}
echo "[04-cloud-sql.sh] Postgres 15 private-IP instance (project=$PROJECT_ID region=$REGION)"
