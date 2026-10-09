#!/bin/bash
# 02 — least-privilege service accounts + IAM bindings. Idempotent.
set -eu
: "${PROJECT_ID:?export PROJECT_ID}" "${REGION:=europe-west1}"

sa() {  # $1=name $2=display
  gcloud iam service-accounts create "$1" --project="$PROJECT_ID" \
    --display-name="$2" 2>/dev/null \
    || echo "SA $1 exists"
}

bind() {  # $1=sa-name $2=role
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$1@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="$2" --condition=None >/dev/null
}

sa afya-tryton 'Afya Tryton runtime'
sa afya-exporter 'Afya analytics exporter'
sa afya-deployer 'Afya deployer (CI)'

bind afya-tryton roles/cloudsql.client
bind afya-tryton roles/secretmanager.secretAccessor
bind afya-exporter roles/bigquery.dataEditor
bind afya-exporter roles/secretmanager.secretAccessor
bind afya-exporter roles/pubsub.publisher
bind afya-deployer roles/run.admin
bind afya-deployer roles/iam.serviceAccountUser
echo '[02] service accounts ready'
