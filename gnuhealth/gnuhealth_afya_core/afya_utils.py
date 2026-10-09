# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""AfyaConnect privacy utilities — pure Python, no Tryton dependency.

Tested by tests/unit without a Tryton server.
"""
import hashlib
import json
import re

# Nigerian mobile patterns: 0803..., 0701..., 090..., +234...
NIGERIAN_PHONE = re.compile(r'(0[789][01]\d{8}|\+234[789][01]\d{8})')

REDACTED = '[PHONE_REDACTED]'

# Analytics allowlist: only categorical/coarse fields may cross into BigQuery.
ANALYTICS_ALLOWED_KEYS = frozenset({
    'event_id', 'event_type', 'triage_level', 'coarse_region',
    'region_level', 'channel', 'language', 'created_at', 'k_count',
})

FREE_TEXT_KEYS = frozenset({'symptoms_raw', 'notes', 'rationale', 'summary', 'transcript'})


def redact_phone_numbers(text):
    """Redact Nigerian phone numbers before storing symptoms_raw."""
    if not text:
        return text
    return NIGERIAN_PHONE.sub(REDACTED, text)


def coarsen_region(sector_count, lga_count, state_count, threshold=10):
    """k-anonymity cascade: sector -> lga -> state -> suppressed."""
    if sector_count >= threshold:
        return 'sector', None
    if lga_count >= threshold:
        return 'lga', None
    if state_count >= threshold:
        return 'state', None
    return 'suppressed', 'INSUFFICIENT_VOLUME'


def anonymize_payload(payload):
    """Return a BigQuery-safe copy: allowlisted keys only, no free text."""
    return {k: v for k, v in dict(payload).items() if k in ANALYTICS_ALLOWED_KEYS}


def validate_analytics_payload(payload):
    """Raise ValueError if payload contains PII/free-text/hashes."""
    payload = dict(payload)
    for key in FREE_TEXT_KEYS:
        if key in payload:
            raise ValueError('analytics payload must not contain free text: %s' % key)
    blob = json.dumps(payload, sort_keys=True, default=str)
    if NIGERIAN_PHONE.search(blob):
        raise ValueError('analytics payload contains a phone number')
    # 32/40/64-hex hashes look like de-identified identifiers — forbidden.
    if re.search(r'\b[0-9a-fA-F]{32}\b|\b[0-9a-fA-F]{40}\b|\b[0-9a-fA-F]{64}\b', blob):
        raise ValueError('analytics payload must not contain hashes')
    unknown = set(payload) - ANALYTICS_ALLOWED_KEYS
    if unknown:
        raise ValueError('analytics payload has non-allowlisted keys: %s' % sorted(unknown))
    return True


def stable_event_id(*parts):
    """Deterministic UUID-like event id (uuid5-style) for outbox idempotency."""
    import uuid
    return str(uuid.uuid5(uuid.NAMESPACE_URL, '|'.join(map(str, parts))))


def session_hash(session_id, salt='afya'):
    """Non-reversible session reference for analytics joins (stored, never exported raw)."""
    return hashlib.sha256(('%s|%s' % (salt, session_id)).encode()).hexdigest()
