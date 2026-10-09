#!/bin/bash
# Smoke-test Afya Tryton modules against REAL trytond 7.0 (no DB needed).
# Installs trytond into an isolated venv, links modules, imports every model,
# checks namespaces/fields and validates tryton.cfg references.
# Usage: bash scripts/smoke_tryton_imports.sh [venv-dir]
set -eu
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${1:-${TMPDIR:-/tmp}/afya-smoke-venv}"

[ -d "$VENV" ] || python3 -m venv "$VENV"
"$VENV/bin/pip" install -q "trytond==7.0.*"

SITE="$("$VENV"/bin/python -c "import trytond, os; print(os.path.dirname(trytond.__file__))")"
for m in gnuhealth_afya_core gnuhealth_afya_access gnuhealth_afya_triage \
    gnuhealth_afya_dispatch gnuhealth_afya_diaspora gnuhealth_afya_analytics \
    mosquito_registration; do
  ln -sfn "$ROOT/gnuhealth/$m" "$SITE/modules/$m"
done

cd "$ROOT" && "$VENV"/bin/python - <<'EOF'
import configparser
import glob
import importlib
import os

for m in ['gnuhealth_afya_core', 'gnuhealth_afya_access', 'gnuhealth_afya_triage',
        'gnuhealth_afya_dispatch', 'gnuhealth_afya_diaspora',
        'gnuhealth_afya_analytics', 'mosquito_registration']:
    mod = importlib.import_module('trytond.modules.%s' % m)
    assert callable(mod.register), m
    print('import OK:', m)

from trytond.modules.gnuhealth_afya_triage.afya_triage import TriageSession
from trytond.modules.gnuhealth_afya_dispatch.afya_dispatch import DispatchRequest
from trytond.modules.gnuhealth_afya_core.afya_core import (
    AfyaConfig, ConsentRecord)
from trytond.model import ModelSingleton

assert issubclass(AfyaConfig, ModelSingleton), 'config must be a singleton'
for cls in [TriageSession, DispatchRequest, ConsentRecord]:
    assert cls.__name__.startswith('gnuhealth.afya.'), cls
for f in ['session_id', 'triage_level', 'reviewer_decision', 'state']:
    assert hasattr(TriageSession, f), f
for f in ['dispatch_ref', 'ambulance_id', 'state']:
    assert hasattr(DispatchRequest, f), f
print('models/fields OK')

for cfg in sorted(glob.glob('gnuhealth/*/tryton.cfg')):
    cp = configparser.ConfigParser()
    cp.read(cfg)
    assert cp.get('tryton', 'version').startswith('7.0'), cfg
    for x in cp.get('tryton', 'xml').split():
        assert os.path.exists(os.path.join(os.path.dirname(cfg), x.strip())), (cfg, x)
    print('cfg OK:', cfg)
print('TRYTON SMOKE OK')
EOF
