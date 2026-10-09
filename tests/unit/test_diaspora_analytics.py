"""Diaspora matching + analytics snapshot builders (T039/T040)."""
import sys
import os

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, 'gnuhealth', 'gnuhealth_afya_diaspora'))
sys.path.insert(0, os.path.join(REPO, 'gnuhealth', 'gnuhealth_afya_analytics'))

from diaspora_logic import (  # noqa: E402
    CONSULT_EVENT_TYPES, is_valid_consult_event, match_score)


def test_match_score_specialty_dominates():
    assert match_score('cardiology', 'cardiology', ['en'], 'en') == 1.0
    assert match_score('cardiology', 'cardiology', ['en'], 'ha') == 0.8
    assert match_score('trauma', 'cardiology', ['en'], 'en') == 0.5
    assert match_score('trauma', 'cardiology', ['ha'], 'en') == 0.3


def test_match_score_handles_missing_languages():
    assert match_score('trauma', 'trauma', None, 'en') == 0.8
    assert match_score('trauma', 'trauma', [], 'ff') == 0.8


def test_consult_event_types_categorical():
    assert set(CONSULT_EVENT_TYPES) == {
        'scheduled', 'audio_started', 'audio_ended', 'held', 'closed', 'cancelled'}
    assert is_valid_consult_event('audio_started') is True
    assert is_valid_consult_event('video_started') is False
    assert is_valid_consult_event('free text note') is False


def test_snapshot_builder():
    from analytics_logic import build_snapshot_values
    vals = build_snapshot_values('FMC Gombe (coarse)', 12, 3)
    assert vals == {'facility_name': 'FMC Gombe (coarse)',
                    'beds_available': 12, 'ambulances_available': 3}
    with pytest.raises(ValueError):
        build_snapshot_values('x', -1, 0)
    with pytest.raises(ValueError):
        build_snapshot_values('', 1, 1)
