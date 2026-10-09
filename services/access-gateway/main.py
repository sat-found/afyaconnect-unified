# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""access-gateway: USSD/SMS/voice/webhooks -> AccessSession intent + triage handoff."""
import os
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import detect_language, redact_phones  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.responses import HTMLResponse  # noqa: E402
from pydantic import BaseModel  # noqa: E402

app = FastAPI(title='Afya Access Gateway', version='1.0.0')


class Inbound(BaseModel):
    channel: str = 'ussd'
    text: str = ''
    sender: str = ''
    language: str | None = None


@app.get('/healthz')
def healthz():
    return {'ok': True, 'service': 'access-gateway'}


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
    return {
        'session_id': session_id,
        'channel': ch,
        'language': lang,
        'language_confidence': conf,
        'fulfulde_fallback': fallback,
        'interactions_used': interactions,
        'within_4_interactions': interactions < 4,
        'redacted_text': redact_phones(msg.text),
        'next': 'triage-agent',
        'latency_ms': round((time.time() - t0) * 1000, 1),
    }


@app.get('/', response_class=HTMLResponse)
def demo_ui():
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AfyaConnect — Access Gateway</title>
<style>:root{--teal:#0d9488;--navy:#0f172a;--bg:#f6f9f9}*{box-sizing:border-box}
body{font-family:Inter,system-ui,sans-serif;background:var(--bg);color:var(--navy);margin:0}
header{background:linear-gradient(135deg,#0f766e,#14b8a6);color:#fff;padding:28px 20px}
main{max-width:720px;margin:-24px auto 40px;background:#fff;border-radius:16px;
box-shadow:0 12px 48px rgba(13,148,136,.16);padding:28px}
textarea,select{width:100%;padding:12px;border:1px solid #e2e8f0;border-radius:10px;font-size:15px}
button{background:var(--teal);color:#fff;border:0;border-radius:10px;padding:12px 20px;
font-weight:700;cursor:pointer}button:hover{filter:brightness(1.08)}
pre{background:#0f172a;color:#5eead4;border-radius:12px;padding:16px;overflow:auto}
.langs{display:flex;gap:8px;margin:12px 0}.langs button{background:#eef2f2;color:var(--navy)}</style></head>
<body><header><h1>AfyaConnect · Access Gateway</h1>
<p>USSD / SMS / Voice triage entry — EN · HA · FF</p></header>
<main><div class="langs"><button>English</button><button>Hausa</button><button>Fulfulde</button></div>
<select id="ch"><option value="ussd">USSD</option><option value="sms">SMS</option><option value="voice">Voice</option></select>
<p><textarea id="t" rows="3">Ba iya numfashi, ciwon kirji. Call 08031234567</textarea></p>
<p><button onclick="send()">Triage →</button></p><pre id="o">…</pre></main>
<script>async function send(){const r=await fetch('/ussd',{method:'POST',
headers:{'Content-Type':'application/json'},body:JSON.stringify({channel:ch.value,text:t.value})});
o.textContent=JSON.stringify(await r.json(),null,2)}</script></body></html>"""
