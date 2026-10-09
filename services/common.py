# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Shared helpers for AfyaConnect Cloud Run services (copied per-image)."""
import re

PHONE_RE = re.compile(r'(0[789][01]\d{8}|\+234[789][01]\d{8})')
ANALYTICS_ALLOWED = frozenset({
    'event_id', 'event_type', 'triage_level', 'coarse_region',
    'region_level', 'channel', 'language', 'created_at', 'k_count'})
FREE_TEXT = frozenset({'symptoms_raw', 'notes', 'rationale', 'summary', 'transcript'})


def redact_phones(text):
    return PHONE_RE.sub('[PHONE_REDACTED]', text) if text else text


def detect_language(text):
    """Stub language detect (en/ha/ff) with confidence; <0.70 -> Fulfulde fallback check."""
    t = (text or '').lower()
    ha_markers = ['ba iya', 'ciwon', 'jini', 'zazzabi', 'taimaka', 'gaggawa', 'haihuwa']
    ff_markers = ['numaani', 'mettu', 'ngol', 'ngesa', 'ballal', 'berde', 'bernde']
    if any(m in t for m in ha_markers):
        return 'ha', 0.85
    if any(m in t for m in ff_markers):
        return 'ff', 0.82
    return 'en', 0.9


def validate_analytics(payload):
    import json as _json
    for k in FREE_TEXT:
        if k in payload:
            raise ValueError('free text key forbidden: %s' % k)
    blob = _json.dumps(payload, sort_keys=True, default=str)
    if PHONE_RE.search(blob):
        raise ValueError('phone number in payload')
    if re.search(r'\b[0-9a-fA-F]{32}\b|\b[0-9a-fA-F]{40}\b|\b[0-9a-fA-F]{64}\b', blob):
        raise ValueError('hash in payload')
    unknown = set(payload) - ANALYTICS_ALLOWED
    if unknown:
        raise ValueError('non-allowlisted keys: %s' % sorted(unknown))
    return True
