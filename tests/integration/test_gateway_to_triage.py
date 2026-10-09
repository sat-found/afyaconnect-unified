"""Integration: gateway -> triage -> outbox pipeline (G1 demo path, no server)."""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'services'))
sys.path.insert(0, os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_core'))
sys.path.insert(0, os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_triage'))
sys.path.insert(0, os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_dispatch'))

from fastapi.testclient import TestClient  # noqa: E402
from afya_utils import coarsen_region, redact_phone_numbers  # noqa: E402
from triage_logic import detect_emergency_keywords, validate_rationale  # noqa: E402
from dispatch_logic import is_valid_transition, naers_accept_stub  # noqa: E402


def _client(name):
    spec = importlib.util.spec_from_file_location(
        'int_%s' % name, os.path.join(ROOT, 'services', name, 'main.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return TestClient(mod.app)


def test_gateway_to_triage_to_outbox():
    gw = _client('access-gateway')
    ta = _client('ai-triage-agent')
    ex = _client('analytics-exporter')

    inbound = gw.post('/ussd', json={'channel': 'ussd',
        'text': 'Ba iya numfashi, ciwon kirji 08031234567'}).json()
    assert inbound['language'] == 'ha'
    assert '[PHONE_REDACTED]' in inbound['redacted_text']

    tri = ta.post('/triage', json={'text': inbound['redacted_text'],
        'session_id': 'TRI-DEMO-1'}).json()
    assert tri['triage_level'] == 'emergency'
    assert tri['human_review_required'] is True
    import json as _json
    validate_rationale(_json.dumps(tri['clinical_rationale']))

    level, _ = coarsen_region(3, 12, 50)
    out = ex.post('/export', json={'event_id': 'triage-TRI-DEMO-1',
        'event_type': 'triage', 'triage_level': tri['triage_level'],
        'coarse_region': 'gombe', 'region_level': level, 'channel': 'ussd',
        'language': 'ha', 'created_at': '2026-01-01', 'k_count': 12}).json()
    assert out['exported'] is True


def test_triage_to_dispatch_human_gate():
    assert is_valid_transition('candidate', 'approved')
    resp = naers_accept_stub({'dispatch_ref': 'DSP-TRI-DEMO-1'})
    assert resp['status'] == 'accepted (STUB)'
    assert detect_emergency_keywords('a numaani', [('a numaani', 'ff')])
    assert redact_phone_numbers('+2348031234567') == '[PHONE_REDACTED]'
