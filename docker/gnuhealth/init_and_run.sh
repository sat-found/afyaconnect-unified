#!/bin/bash
# Init + run Tryton: wait for Postgres, init DB, install Afya modules, serve via uWSGI.
# SPDX-License-Identifier: GPL-3.0-or-later
set -eu
CONF="${TRYTOND_CONF:-/opt/gnuhealth/etc/trytond.conf}"
: "${GNUHEALTH_DB_HOST:=postgres}" "${GNUHEALTH_DB_PORT:=5432}"
: "${GNUHEALTH_DB_USERNAME:=gnuhealth}" "${GNUHEALTH_DB_PASSWORD:?set GNUHEALTH_DB_PASSWORD}"
: "${GNUHEALTH_DB_NAME:=health}" "${TRYTON_ADMIN_PASSWORD:?set TRYTON_ADMIN_PASSWORD}"

echo "Waiting for Postgres $GNUHEALTH_DB_HOST:$GNUHEALTH_DB_PORT..."
for i in $(seq 1 60); do
  (echo > /dev/tcp/"$GNUHEALTH_DB_HOST"/"$GNUHEALTH_DB_PORT") 2>/dev/null && break
  sleep 2
done

export TRYTOND_DATABASE_URI="postgresql://${GNUHEALTH_DB_USERNAME}:${GNUHEALTH_DB_PASSWORD}@${GNUHEALTH_DB_HOST}:${GNUHEALTH_DB_PORT}/${GNUHEALTH_DB_NAME}"

if [ ! -f /var/lib/tryton/.afya-init-done ]; then
  echo "Initializing database..."
  trytond-admin -c "$CONF" -d "$GNUHEALTH_DB_NAME" --all --admin-password="$TRYTON_ADMIN_PASSWORD" || true
  for m in gnuhealth_afya_core gnuhealth_afya_access gnuhealth_afya_triage \
           gnuhealth_afya_dispatch gnuhealth_afya_diaspora gnuhealth_afya_analytics; do
    trytond-admin -c "$CONF" -d "$GNUHEALTH_DB_NAME" -m "$m" --update || true
  done
  touch /var/lib/tryton/.afya-init-done
fi

exec uwsgi --ini /opt/gnuhealth/etc/uwsgi.ini --set-placeholder conf="$CONF"
