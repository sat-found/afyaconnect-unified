"""Live acceptance checks (Gates G1/G2 automated subset).

Runs against live services (local compose or Cloud Run). Skips cleanly when
services are unreachable — pure-logic coverage lives in tests/unit.

Env: AFYA_GW_URL (default http://localhost:8081),
     AFYA_TRIAGE_URL, AFYA_FHIR_URL, AFYA_EXPORT_URL, AFYA_DIASPORA_URL.
"""
import os
import time

import httpx
import pytest

GW = os.environ.get('AFYA_GW_URL', 'http://localhost:8081').rstrip('/')
TRIAGE = os.environ.get('AFYA_TRIAGE_URL', 'http://localhost:8082').rstrip('/')
FHIR = os.environ.get('AFYA_FHIR_URL', 'http://localhost:8083').rstrip('/')
EXPORT = os.environ.get('AFYA_EXPORT_URL', 'http://localhost:8084').rstrip('/')
DIASPORA = os.environ.get('AFYA_DIASPORA_URL', 'http://localhost:8085').rstrip('/')

TIMEOUT = float(os.environ.get('AFYA_AT_TIMEOUT_S', '15'))

services = pytest.mark.services


def _ping(url):
    try:
        return httpx.get('%s/healthz' % url, timeout=3).status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _ping(GW), reason='live services not running (make services-up)')


@services
def test_at_acc_01_ussd_under_4_interactions():
    payload = {'channel': 'ussd', 'text': 'zazzabi mai tsanani, taimaka'}
    r = httpx.post('%s/ussd' % GW, json=payload, timeout=TIMEOUT).json()
    assert r['interactions_used'] < 4
    assert r['within_4_interactions'] is True


@services
def test_at_nav_01_emergency_concordance_and_schema():
    cases = [
        ('patient unconscious, severe bleeding', 'emergency'),
        ('ciwon kirji, ba iya numfashi', 'emergency'),
        ('a numaani, ballal', 'emergency'),
        ('high fever and severe headache', 'red'),
    ]
    for text, expected in cases:
        body = httpx.post('%s/triage' % TRIAGE, json={'text': text},
                          timeout=TIMEOUT).json()
        assert body['triage_level'] == expected, text
        assert set(body['clinical_rationale']) == {
            'level', 'confidence', 'red_flags', 'model_version'}
        assert 0 <= body['clinical_rationale']['confidence'] <= 1


@services
def test_at_lang_01_trilingual_parity():
    levels = {}
    for lang, text in [('en', 'chest pain, cannot breathe'),
                       ('ha', 'ciwon kirji, ba iya numfashi'),
                       ('ff', 'a numaani')]:
        body = httpx.post('%s/triage' % TRIAGE,
                          json={'text': text, 'language': lang}, timeout=TIMEOUT).json()
        levels[lang] = body['triage_level']
    assert levels == {'en': 'emergency', 'ha': 'emergency', 'ff': 'emergency'}


@services
def test_at_safe_01_emergency_routes_to_human_review():
    body = httpx.post('%s/ussd' % GW, json={'channel': 'voice',
                                            'text': 'patient unconscious'}, timeout=TIMEOUT).json()
    assert body['triage']['human_review_required'] is True
    assert body['next'] == 'human-review'


@services
def test_gateway_forwards_to_triage_agent_when_configured():
    health = httpx.get('%s/healthz' % GW, timeout=TIMEOUT).json()
    if health.get('triage_agent') == 'local-fallback':
        pytest.skip('gateway has no triage-agent configured')
    body = httpx.post('%s/ussd' % GW, json={'channel': 'ussd',
                                            'text': 'chest pain'}, timeout=TIMEOUT).json()
    assert body['triage']['source'] == 'ai-triage-agent'


@services
def test_at_disp_01_pipeline_latency_windows():
    t0 = time.time()
    gw = httpx.post('%s/ussd' % GW, json={'channel': 'ussd',
                                          'text': 'severe bleeding, help'}, timeout=TIMEOUT).json()
    elapsed = time.time() - t0
    assert gw['triage']['triage_level'] == 'emergency'
    assert elapsed < 30, 'Window B (escalation->candidate budget 30s): %.1fs' % elapsed
    assert gw['latency_ms'] < 30000


@services
def test_at_priv_01_no_pii_in_pipeline():
    payload = {'channel': 'sms', 'text': 'help 08031234567 or +2348031234567'}
    gw = httpx.post('%s/sms' % GW, json=payload, timeout=TIMEOUT).json()
    assert '08031234567' not in gw['redacted_text']
    assert '+2348031234567' not in gw['redacted_text']
    bad = httpx.post('%s/export' % EXPORT, json={
        'event_id': 'at-priv-1', 'event_type': 'triage', 'triage_level': 'red',
        'coarse_region': 'kano', 'region_level': 'lga', 'channel': 'sms',
        'language': 'en', 'created_at': '2026-01-01', 'k_count': 15,
        'symptoms_raw': 'should be rejected'}, timeout=TIMEOUT)
    # Strict schema: free-text keys are rejected, never silently dropped.
    assert bad.status_code == 422


@services
def test_at_fhir_01_read_latency():
    t0 = time.time()
    r = httpx.get('%s/fhir/Patient' % FHIR, timeout=TIMEOUT)
    elapsed = time.time() - t0
    assert r.status_code == 200
    assert r.json()['resourceType'] == 'Bundle'
    assert elapsed < 5, 'FHIR read budget 5s: %.2fs' % elapsed


@services
def test_at_dash_01_export_marks_exported():
    before = httpx.get('%s/' % EXPORT, timeout=TIMEOUT).json()['exported']
    r = httpx.post('%s/export' % EXPORT, json={
        'event_id': 'at-dash-%d' % int(time.time()), 'event_type': 'triage',
        'triage_level': 'yellow', 'coarse_region': 'gombe',
        'region_level': 'state', 'channel': 'ussd', 'language': 'ff',
        'created_at': '2026-01-01', 'k_count': 42}, timeout=TIMEOUT).json()
    assert r['exported'] is True
    after = httpx.get('%s/' % EXPORT, timeout=TIMEOUT).json()['exported']
    assert after == before + 1
