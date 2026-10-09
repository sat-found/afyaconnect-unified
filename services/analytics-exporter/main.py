# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""analytics-exporter: poll outbox -> quality gates -> BigQuery (stubbed sink)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import add_standard_middleware, validate_analytics  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from pydantic import BaseModel, ConfigDict  # noqa: E402

app = FastAPI(title='Afya Analytics Exporter', version='1.0.0')
add_standard_middleware(app, 'analytics-exporter')
EXPORTED: list = []


class Event(BaseModel):
    # Strict schema: unknown keys (incl. free text) -> 422, never silently dropped.
    model_config = ConfigDict(extra='forbid')

    event_id: str
    event_type: str
    triage_level: str = 'unknown'
    coarse_region: str = 'suppressed'
    region_level: str = 'suppressed'
    channel: str = 'ussd'
    language: str = 'en'
    created_at: str = ''
    k_count: int = 0


@app.get('/healthz')
def healthz():
    return {'ok': True, 'service': 'analytics-exporter', 'exported': len(EXPORTED)}


@app.get('/')
def info():
    return {'service': 'analytics-exporter', 'docs': '/docs',
            'exported': len(EXPORTED)}


@app.post('/export')
def export(ev: Event):
    payload = ev.model_dump()
    try:
        validate_analytics(payload)
    except ValueError as exc:
        return {'exported': False, 'reason': str(exc)}
    if payload['k_count'] < 10 and payload['region_level'] != 'suppressed':
        return {'exported': False, 'reason': 'k-anonymity: must be suppressed'}
    EXPORTED.append(payload['event_id'])
    return {'exported': True, 'event_id': payload['event_id'], 'sink': 'bigquery (STUB)'}
