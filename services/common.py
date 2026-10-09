# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""Shared helpers for AfyaConnect Cloud Run services (copied per-image)."""
import logging
import re
import time
import uuid

PHONE_RE = re.compile(r'(0[789][01]\d{8}|\+234[789][01]\d{8})')
ANALYTICS_ALLOWED = frozenset({
    'event_id', 'event_type', 'triage_level', 'coarse_region',
    'region_level', 'channel', 'language', 'created_at', 'k_count'})
FREE_TEXT = frozenset({'symptoms_raw', 'notes', 'rationale', 'summary', 'transcript'})

EMERGENCY_TERMS = ['unconscious', 'cannot breathe', 'ba iya numfashi', 'severe bleeding',
                   'jini mai yawa', 'chest pain', 'ciwon kirji', 'stroke', 'seizure', 'choking',
                   'a numaani', 'heart attack', 'pregnancy bleeding', 'labour pain']
RED_TERMS = ['high fever', 'zazzabi', 'convulsion', 'severe headache', 'ciwon kai',
             'difficulty breathing', 'allergic reaction']


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


def classify(text):
    """Symptom text -> (level, confidence, red_flags). Singleshared implementation."""
    t = (text or '').lower()
    red_flags = [k for k in EMERGENCY_TERMS if k in t]
    if red_flags:
        return 'emergency', 0.92, red_flags
    reds = [k for k in RED_TERMS if k in t]
    if reds:
        return 'red', 0.81, reds
    if len(t.split()) < 4:
        return 'green', 0.6, []
    return 'yellow', 0.7, []


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


def get_logger(service):
    logger = logging.getLogger('afya.%s' % service)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def add_standard_middleware(app, service):
    """CORS (SAO/demo origins) + X-Request-ID + access log. Industry-standard baseline."""
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.middleware.base import BaseHTTPMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:8091', 'http://localhost:3000', '*'],
        allow_methods=['GET', 'POST', 'OPTIONS'],
        allow_headers=['*'],
    )

    logger = get_logger(service)

    class RequestContextMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            rid = request.headers.get('X-Request-ID') or uuid.uuid4().hex[:12]
            t0 = time.time()
            response = await call_next(request)
            response.headers['X-Request-ID'] = rid
            logger.info('%s %s -> %s (%.1fms)',
                        request.method, request.url.path,
                        response.status_code, (time.time() - t0) * 1000)
            return response

    app.add_middleware(RequestContextMiddleware)
    return app
