#!/bin/bash
# 08-cloud-scheduler.sh — Daily purge + snapshot jobs
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" ${REGION:=europe-west1}
echo "[08-cloud-scheduler.sh] Daily purge + snapshot jobs (project=$PROJECT_ID region=$REGION)"
