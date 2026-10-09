# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""diaspora-matching: mock specialist scoring (audio-only consults MVP)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import add_standard_middleware  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from pydantic import BaseModel  # noqa: E402

app = FastAPI(title='Afya Diaspora Matching', version='1.0.0')
add_standard_middleware(app, 'diaspora-matching')

SPECIALISTS = [
    {'name': 'Dr. A. Modibbo', 'specialty': 'cardiology',
        'languages': ['en', 'ha'], 'tz': 'America/New_York'},
    {'name': 'Dr. F. Bello', 'specialty': 'obstetrics',
        'languages': ['en', 'ff'], 'tz': 'Europe/London'},
    {'name': 'Dr. S. Okoro', 'specialty': 'pediatrics',
        'languages': ['en'], 'tz': 'America/Chicago'},
    {'name': 'Dr. H. Diallo', 'specialty': 'trauma',
        'languages': ['ff', 'en'], 'tz': 'Europe/Paris'},
    {'name': 'Dr. K. Adeyemi', 'specialty': 'neurology',
        'languages': ['en', 'ha'], 'tz': 'Canada/Eastern'},
]


class MatchIn(BaseModel):
    specialty_needed: str = 'cardiology'
    language_needed: str = 'en'


@app.get('/healthz')
def healthz():
    return {'ok': True, 'service': 'diaspora-matching'}


@app.get('/')
def info():
    return {'service': 'diaspora-matching', 'docs': '/docs',
            'specialists': len(SPECIALISTS)}


@app.post('/match')
def match(inp: MatchIn):
    ranked = []
    for s in SPECIALISTS:
        score = 0.3 + (0.5 if s['specialty'] == inp.specialty_needed else 0.0) \
            + (0.2 if inp.language_needed in s['languages'] else 0.0)
        ranked.append({**s, 'score': round(min(score, 1.0), 2)})
    ranked.sort(key=lambda r: -r['score'])
    return {'matches': ranked, 'mode': 'audio-only (STUB)'}
