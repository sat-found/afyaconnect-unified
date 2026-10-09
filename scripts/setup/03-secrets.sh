#!/bin/bash
# 03 — Secret Manager entries (values prompted, never logged). Idempotent.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}"

secret() {  # $1=name $2=prompt
  if gcloud secrets describe "$1" --project="$PROJECT_ID" >/dev/null 2>&1; then
    echo "secret $1 exists (use 'gcloud secrets versions add' to rotate)"
    return 0
  fi
  read -rsp "$2: " value; echo
  printf '%s' "$value" | gcloud secrets create "$1" --project="$PROJECT_ID" \
    --replication-policy=automatic --data-file=-
  unset value
}

secret afya-db-password 'Postgres password'
secret afya-tryton-admin 'Tryton admin password'
secret afya-gemini-key 'Gemini API key'
echo '[03] secrets ready'
