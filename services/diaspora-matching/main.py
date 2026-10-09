# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""diaspora-matching: mock specialist scoring (audio-only consults MVP)."""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Afya Diaspora Matching', version='1.0.0')

SPECIALISTS = [
    {'name': 'Dr. A. Modibbo', 'specialty': 'cardiology', 'languages': ['en', 'ha'], 'tz': 'America/New_York'},
    {'name': 'Dr. F. Bello', 'specialty': 'obstetrics', 'languages': ['en', 'ff'], 'tz': 'Europe/London'},
    {'name': 'Dr. S. Okoro', 'specialty': 'pediatrics', 'languages': ['en'], 'tz': 'America/Chicago'},
    {'name': 'Dr. H. Diallo', 'specialty': 'trauma', 'languages': ['ff', 'en'], 'tz': 'Europe/Paris'},
    {'name': 'Dr. K. Adeyemi', 'specialty': 'neurology', 'languages': ['en', 'ha'], 'tz': 'Canada/Eastern'},
]


class MatchIn(BaseModel):
    specialty_needed: str = 'cardiology'
    language_needed: str = 'en'


@app.get('/healthz')
def healthz():
    return {'ok': True, 'service': 'diaspora-matching'}


@app.post('/match')
def match(inp: MatchIn):
    ranked = []
    for s in SPECIALISTS:
        score = 0.3 + (0.5 if s['specialty'] == inp.specialty_needed else 0.0) \
            + (0.2 if inp.language_needed in s['languages'] else 0.0)
        ranked.append({**s, 'score': round(min(score, 1.0), 2)})
    ranked.sort(key=lambda r: -r['score'])
    return {'matches': ranked, 'mode': 'audio-only (STUB)'}
