# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""ai-triage-agent: stateless symptom -> triage level + validated rationale JSON."""
import os
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import add_standard_middleware, classify, redact_phones  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from pydantic import BaseModel  # noqa: E402

app = FastAPI(title='Afya AI Triage Agent', version='1.0.0')
add_standard_middleware(app, 'ai-triage-agent')


class TriageIn(BaseModel):
    text: str = ''
    language: str = 'en'
    session_id: str | None = None


@app.get('/healthz')
def healthz():
    return {'ok': True, 'service': 'ai-triage-agent'}


@app.get('/')
def info():
    return {'service': 'ai-triage-agent', 'docs': '/docs', 'health': '/healthz'}


@app.post('/triage')
def triage(inp: TriageIn):
    t0 = time.time()
    clean = redact_phones(inp.text)
    level, conf, flags = classify(clean)
    rationale = {'level': level, 'confidence': conf, 'red_flags': flags,
        'model_version': 'afya-triage-v1'}
    human_review = level == 'emergency'
    return {
        'session_id': inp.session_id or ('TRI-%s' % uuid.uuid4().hex[:12]),
        'triage_level': level,
        'triage_confidence': conf,
        'clinical_rationale': rationale,
        'human_review_required': human_review,
        'symptoms_stored': clean,
        'latency_ms': round((time.time() - t0) * 1000, 1),
    }
