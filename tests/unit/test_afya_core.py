"""Core privacy utils (T019-T020)."""
import pytest
from afya_utils import (
    anonymize_payload, coarsen_region, redact_phone_numbers,
    stable_event_id, validate_analytics_payload)


def test_redact_local_and_intl():
    assert redact_phone_numbers('call 08031234567 now') == 'call [PHONE_REDACTED] now'
    assert redact_phone_numbers('call +2348031234567 now') == 'call [PHONE_REDACTED] now'
    assert redact_phone_numbers('no phone here') == 'no phone here'
    assert redact_phone_numbers('') == ''
    assert redact_phone_numbers(None) is None


def test_coarsen_cascade():
    assert coarsen_region(15, 50, 200) == ('sector', None)
    assert coarsen_region(3, 12, 50) == ('lga', None)
    assert coarsen_region(3, 3, 50) == ('state', None)
    assert coarsen_region(1, 2, 3) == ('suppressed', 'INSUFFICIENT_VOLUME')


def test_analytics_allowlist_and_rejections():
    good = {'event_id': 'a', 'event_type': 'triage', 'triage_level': 'red',
            'coarse_region': 'kano', 'region_level': 'lga', 'channel': 'ussd',
            'language': 'ha', 'created_at': '2026-01-01', 'k_count': 15}
    assert validate_analytics_payload(good) is True
    assert anonymize_payload({**good, 'symptoms_raw': 'x'}) == good
    with pytest.raises(ValueError):
        validate_analytics_payload({**good, 'symptoms_raw': 'chest pain'})
    with pytest.raises(ValueError):
        validate_analytics_payload({**good, 'event_id': 'call 08031234567'})
    with pytest.raises(ValueError):
        validate_analytics_payload({**good, 'note_hash': 'd41d8cd98f00b204e9800998ecf8427e'})


def test_stable_event_id():
    assert stable_event_id('a', 'b') == stable_event_id('a', 'b')
    assert stable_event_id('a') != stable_event_id('b')
