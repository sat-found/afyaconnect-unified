"""Dispatch logic: 10 kits, 10 states, guarded transitions, NAERS stub (T032-T036)."""
from dispatch_logic import (
    DISPATCH_STATES, KIT_TEMPLATES,
    is_valid_transition, naers_accept_stub)


def test_ten_kit_templates():
    assert len(KIT_TEMPLATES) == 10
    assert ('trauma', 'Trauma Kit') in KIT_TEMPLATES


def test_ten_states_and_guards():
    assert len(DISPATCH_STATES) == 10
    assert set(DISPATCH_STATES) >= {'candidate', 'approved', 'completed'}
    assert is_valid_transition('candidate', 'approved') is True
    assert is_valid_transition('candidate', 'completed') is False
    assert is_valid_transition('arrived', 'completed') is True


def test_naers_stub_disclosed():
    resp = naers_accept_stub({'dispatch_ref': 'DSP-1'})
    assert resp['status'] == 'accepted (STUB)'
    assert resp['assignment_ref'].startswith('NAERS-')
