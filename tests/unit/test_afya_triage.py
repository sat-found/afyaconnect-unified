"""Triage logic: rationale schema + keyword detection (T028-T029)."""
import json
import pytest
from triage_logic import (
    detect_emergency_keywords, needs_human_review, validate_rationale)


def good(level='red'):
    return json.dumps({'level': level, 'confidence': 0.9,
                       'red_flags': ['chest pain'], 'model_version': 'v1'})


def test_rationale_valid():
    assert validate_rationale(good()) is True
    assert validate_rationale('') is True


def test_rationale_rejections():
    with pytest.raises(Exception):
        validate_rationale('not json')
    with pytest.raises(Exception):
        validate_rationale(json.dumps({'level': 'red'}))
    with pytest.raises(Exception):
        validate_rationale(json.dumps({'level': 'purple', 'confidence': 0.5,
                                       'red_flags': [], 'model_version': 'v1'}))
    with pytest.raises(Exception):
        validate_rationale(json.dumps({'level': 'red', 'confidence': 9,
                                       'red_flags': [], 'model_version': 'v1'}))


def test_keywords_multilingual_case_insensitive():
    kws = [('ba iya numfashi', 'ha'), ('chest pain', 'en'), ('a numaani', 'ff')]
    assert detect_emergency_keywords('BA IYA NUMFASHI, help', kws) == ['ba iya numfashi']
    assert detect_emergency_keywords('Severe CHEST PAIN noted', kws) == ['chest pain']
    assert detect_emergency_keywords('routine visit', kws) == []
    assert detect_emergency_keywords('', kws) == []


def test_emergency_needs_review():
    assert needs_human_review('emergency') is True
    assert needs_human_review('red') is False
