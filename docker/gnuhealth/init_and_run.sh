#!/bin/bash
# Init + run Tryton: wait for Postgres, init DB (Afya module set only),
# install Afya modules, serve via uWSGI.
# SPDX-License-Identifier: GPL-3.0-or-later
set -eu
CONF="${TRYTOND_CONF:-/opt/gnuhealth/etc/trytond.conf}"
: "${GNUHEALTH_DB_HOST:=postgres}" "${GNUHEALTH_DB_PORT:=5432}"
: "${GNUHEALTH_DB_USERNAME:=gnuhealth}" "${GNUHEALTH_DB_PASSWORD:?set GNUHEALTH_DB_PASSWORD}"
: "${GNUHEALTH_DB_NAME:=health}" "${TRYTON_ADMIN_PASSWORD:?set TRYTON_ADMIN_PASSWORD}"
: "${TRYTON_ADMIN_EMAIL:=admin@afyaconnect.local}"

echo "Waiting for Postgres $GNUHEALTH_DB_HOST:$GNUHEALTH_DB_PORT..."
for _ in $(seq 1 60); do
  (echo > /dev/tcp/"$GNUHEALTH_DB_HOST"/"$GNUHEALTH_DB_PORT") 2>/dev/null && break
  sleep 2
done

export TRYTOND_DATABASE_URI="postgresql://${GNUHEALTH_DB_USERNAME}:${GNUHEALTH_DB_PASSWORD}@${GNUHEALTH_DB_HOST}:${GNUHEALTH_DB_PORT}/${GNUHEALTH_DB_NAME}"
export TRYTOND_CONFIG="$CONF"
printf '%s' "$TRYTON_ADMIN_PASSWORD" > /tmp/trytonpass
export TRYTONPASSFILE=/tmp/trytonpass

if [ ! -f "$CONF" ]; then
  echo "Generating $CONF from environment..."
  mkdir -p "$(dirname "$CONF")"
  cat > "$CONF" <<EOF
[database]
uri = $TRYTOND_DATABASE_URI
path = /var/lib/tryton

[web]
listen = 0.0.0.0:8000
root = /opt/gnuhealth/sao
EOF
fi
mkdir -p /var/lib/tryton /opt/gnuhealth/sao
if [ ! -f /opt/gnuhealth/sao/index.html ]; then
  cp /opt/gnuhealth/etc/sao-index.html /opt/gnuhealth/sao/index.html
fi

if [ ! -f /var/lib/tryton/.afya-init-done ]; then
  echo "Initializing Afya module set (dependencies auto-activated)..."
  trytond-admin -c "$CONF" -d "$GNUHEALTH_DB_NAME" \
    --email "$TRYTON_ADMIN_EMAIL" \
    -u gnuhealth_afya_core gnuhealth_afya_access gnuhealth_afya_triage \
       gnuhealth_afya_dispatch gnuhealth_afya_diaspora gnuhealth_afya_analytics \
       mosquito_registration \
    --activate-dependencies
  echo "Refreshing Tryton module list..."
  trytond-admin -c "$CONF" -d "$GNUHEALTH_DB_NAME" -m
  touch /var/lib/tryton/.afya-init-done
  echo "Database initialized."
fi

exec uwsgi --ini /opt/gnuhealth/etc/uwsgi.ini
