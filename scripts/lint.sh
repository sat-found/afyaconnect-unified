#!/bin/bash
# AfyaConnect lint — SINGLE SOURCE OF TRUTH for style (CI + `make lint`).
# Rules: pycodestyle (E501/W503/E128/E131 enforced, 100 cols) + pyflakes.
# Fix style with: python3 -m autopep8 --in-place --select=E,W --max-line-length=100 -r <dirs>
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
status=0
if command -v pycodestyle >/dev/null 2>&1; then
  pycodestyle gnuhealth services scripts tests || status=$?
else
  python3 -m pycodestyle gnuhealth services scripts tests || status=$?
fi
if command -v pyflakes >/dev/null 2>&1; then
  pyflakes gnuhealth services scripts tests || status=$?
else
  python3 -m pyflakes gnuhealth services scripts tests || status=$?
fi
exit $status
