#!/bin/bash
# AfyaConnect lint: pycodestyle + pyflakes (subset that exists in CI)
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
status=0
if command -v pycodestyle >/dev/null 2>&1; then
  pycodestyle gnuhealth services scripts tests --max-line-length=100 || status=$?
else
  python3 -m pycodestyle gnuhealth services scripts tests --max-line-length=100 || status=$?
fi
if command -v pyflakes >/dev/null 2>&1; then
  pyflakes gnuhealth services scripts tests || status=$?
else
  python3 -m pyflakes gnuhealth services scripts tests || status=$?
fi
exit $status
