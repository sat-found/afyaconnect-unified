"""Gateway forwarding + middleware conventions."""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICES = os.path.join(ROOT, 'services')

import sys  # noqa: E402 — path bootstrap before service imports
sys.path.insert(0, SERVICES)

from fastapi.testclient import TestClient  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(
        'svc2_%s' % name.replace('-', '_'), os.path.join(SERVICES, name, 'main.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return TestClient(mod.app)


def test_gateway_suggests_triage_with_fallback_source():
    c = load('access-gateway')
    body = c.post('/ussd', json={'channel': 'ussd',
                                 'text': 'patient unconscious, severe bleeding'}).json()
    assert body['triage']['triage_level'] == 'emergency'
    assert body['triage']['source'] in ('ai-triage-agent', 'local-fallback')
    assert body['next'] == 'human-review'
    assert 'X-Request-ID' in c.post('/ussd',
                                    json={'channel': 'ussd', 'text': 'hi'}).headers


def test_request_id_echo_and_cors():
    c = load('ai-triage-agent')
    r = c.post('/triage', json={'text': 'hello'},
               headers={'X-Request-ID': 'req-123', 'Origin': 'http://localhost:8091'})
    assert r.headers['X-Request-ID'] == 'req-123'
    assert 'access-control-allow-origin' in {k.lower() for k in r.headers}


def test_shared_classify_consistency():
    gw = load('access-gateway')
    ta = load('ai-triage-agent')
    text = 'severe headache and high fever'
    via_gw = gw.post('/ussd', json={'channel': 'sms', 'text': text}).json()
    direct = ta.post('/triage', json={'text': text}).json()
    assert via_gw['triage']['triage_level'] == direct['triage_level'] == 'red'


def test_service_roots():
    for name in ['ai-triage-agent', 'fhir-adapter',
                 'analytics-exporter', 'diaspora-matching']:
        r = load(name).get('/')
        assert r.status_code == 200
        assert 'service' in r.json()
