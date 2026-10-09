#!/bin/bash
# Tryton module test runner (needs a running Tryton/Postgres).
# Fast suite lives in tests/unit (no server). This script is for CI with services.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mods="gnuhealth_afya_core gnuhealth_afya_access gnuhealth_afya_triage gnuhealth_afya_dispatch gnuhealth_afya_diaspora gnuhealth_afya_analytics"
for m in $mods; do
  echo "== validating $m =="
  python3 -m py_compile gnuhealth/$m/*.py gnuhealth/$m/wizard/*.py 2>/dev/null || python3 -m py_compile gnuhealth/$m/*.py
  python3 -c "import xml.dom.minidom,glob; [xml.dom.minidom.parse(f) for f in glob.glob('gnuhealth/$m/**/*.xml',recursive=True)]; print('$m XML OK')"
done
python3 -m pytest tests/unit -q
