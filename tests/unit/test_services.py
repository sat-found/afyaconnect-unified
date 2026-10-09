"""Service-level tests (FastAPI TestClient, no network)."""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICES = os.path.join(ROOT, 'services')

import sys  # noqa: E402 — path bootstrap before service imports
sys.path.insert(0, SERVICES)

from fastapi.testclient import TestClient  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(
        'svc_%s' % name, os.path.join(SERVICES, name, 'main.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return TestClient(mod.app)


def test_gateway_redacts_and_counts_interactions():
    c = load('access-gateway')
    r = c.post('/ussd', json={'channel': 'ussd',
        'text': 'Ba iya numfashi, call 08031234567'})
    assert r.status_code == 200
    body = r.json()
    assert '[PHONE_REDACTED]' in body['redacted_text']
    assert body['within_4_interactions'] is True
    assert body['language'] == 'ha'


def test_triage_agent_emergency_and_rationale():
    c = load('ai-triage-agent')
    r = c.post('/triage', json={'text': 'patient unconscious, severe bleeding'})
    body = r.json()
    assert body['triage_level'] == 'emergency'
    assert body['human_review_required'] is True
    assert set(body['clinical_rationale']) == {
        'level', 'confidence', 'red_flags', 'model_version'}


def test_exporter_gates():
    c = load('analytics-exporter')
    good = {'event_id': 'e1', 'event_type': 'triage', 'triage_level': 'red',
        'coarse_region': 'kano', 'region_level': 'lga', 'channel': 'ussd',
        'language': 'ha', 'created_at': '2026-01-01', 'k_count': 15}
    assert c.post('/export', json=good).json()['exported'] is True
    bad = dict(good, event_id='e2', k_count=3, region_level='lga',
        coarse_region='kano-ward-5')
    assert c.post('/export', json=bad).json()['exported'] is False


def test_diaspora_match_and_fhir():
    m = load('diaspora-matching')
    body = m.post('/match', json={'specialty_needed': 'cardiology',
        'language_needed': 'ha'}).json()
    assert body['matches'][0]['score'] >= 0.7
    f = load('fhir-adapter')
    r = f.get('/fhir/Patient')
    assert r.status_code == 200
    assert r.json()['resourceType'] == 'Bundle'
