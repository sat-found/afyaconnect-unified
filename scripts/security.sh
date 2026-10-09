#!/bin/bash
# Security scan: bandit on python + naive secret grep. Fails on HIGH issues.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
status=0
if command -v bandit >/dev/null 2>&1; then
  bandit -r gnuhealth services -ll || status=$?
else
  python3 -m bandit -r gnuhealth services -ll || status=$?
fi
echo "--- secret scan (informational, fails on likely keys) ---"
if grep -rEn "AKIA[0-9A-Z]{16}|BEGIN (RSA )?PRIVATE KEY|AIza[0-9A-Za-z_-]{35}" \
  gnuhealth services scripts docker --exclude-dir=__pycache__ 2>/dev/null; then
  echo "POSSIBLE SECRET FOUND"; status=1
fi
# allowlisted example passwords use CHANGEME; flag anything else password-like committed
if grep -rEn "password\s*=\s*['\"][^'\"]*['\"]" docker scripts services \
  --exclude="*.example" 2>/dev/null | grep -v CHANGEME | grep -vi "password_env\|getenv\|environ"; then
  echo "HARDCODED PASSWORD SUSPECT — use env/Secret Manager"; status=1
fi
exit $status
