# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""access-gateway: USSD/SMS/voice/webhooks -> AccessSession intent + triage handoff.

Forwards to ai-triage-agent when TRIAGE_AGENT_URL is set (services compose /
Cloud Run); falls back to shared local classify() so the demo path always works.
"""
import os
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import (  # noqa: E402
    add_standard_middleware, classify, detect_language, get_logger, redact_phones)

from fastapi import FastAPI  # noqa: E402
from fastapi.responses import HTMLResponse  # noqa: E402
from pydantic import BaseModel  # noqa: E402

app = FastAPI(title='Afya Access Gateway', version='1.0.0')
add_standard_middleware(app, 'access-gateway')
logger = get_logger('access-gateway')

TRIAGE_AGENT_URL = os.environ.get('TRIAGE_AGENT_URL', '').rstrip('/')
TRIAGE_TIMEOUT_S = float(os.environ.get('TRIAGE_TIMEOUT_S', '8'))


class Inbound(BaseModel):
    channel: str = 'ussd'
    text: str = ''
    sender: str = ''
    language: str | None = None


def suggest_triage(clean_text, session_id):
    """Ask ai-triage-agent; fall back to shared local classify on any failure."""
    if TRIAGE_AGENT_URL:
        try:
            import httpx
            resp = httpx.post('%s/triage' % TRIAGE_AGENT_URL,
                              json={'text': clean_text, 'session_id': session_id},
                              timeout=TRIAGE_TIMEOUT_S)
            resp.raise_for_status()
            return dict(resp.json(), source='ai-triage-agent')
        except Exception as exc:  # noqa: BLE001 — fallback must never break intake
            logger.warning('triage-agent unreachable (%s); using local fallback', exc)
    level, conf, flags = classify(clean_text)
    return {'session_id': session_id, 'triage_level': level,
            'triage_confidence': conf,
            'clinical_rationale': {'level': level, 'confidence': conf,
                                   'red_flags': flags, 'model_version': 'afya-triage-v1-local'},
            'human_review_required': level == 'emergency',
            'source': 'local-fallback'}


@app.get('/healthz')
def healthz():
    return {'ok': True, 'service': 'access-gateway',
            'triage_agent': TRIAGE_AGENT_URL or 'local-fallback'}


@app.post('/ussd')
@app.post('/sms')
@app.post('/voice')
def inbound(msg: Inbound, channel: str = 'ussd'):
    t0 = time.time()
    ch = msg.channel or channel
    lang, conf = detect_language(msg.text)
    if msg.language in ('en', 'ha', 'ff'):
        lang, conf = msg.language, 1.0
    fallback = conf < 0.70
    session_id = 'ACC-%s' % uuid.uuid4().hex[:12]
    interactions = min(3, max(1, len(msg.text.split()) // 4 + 1))
    clean = redact_phones(msg.text)
    triage = suggest_triage(clean, 'TRI-%s' % session_id[4:])
    return {
        'session_id': session_id,
        'channel': ch,
        'language': lang,
        'language_confidence': conf,
        'fulfulde_fallback': fallback,
        'interactions_used': interactions,
        'within_4_interactions': interactions < 4,
        'redacted_text': clean,
        'triage': triage,
        'next': 'human-review' if triage.get('human_review_required') else 'completed',
        'latency_ms': round((time.time() - t0) * 1000, 1),
    }


@app.get('/', response_class=HTMLResponse)
def demo_ui():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'demo.html'), encoding='utf-8') as fh:
        return fh.read()
