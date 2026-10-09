#!/bin/bash
# Normalize line endings / autopep8 subset if available (port of GNU_correct autopep8.sh)
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if command -v autopep8 >/dev/null 2>&1; then
  autopep8 --in-place --max-line-length=100 -r gnuhealth services tests scripts
else
  echo "autopep8 not installed; skipping (pip install autopep8)"
fi
