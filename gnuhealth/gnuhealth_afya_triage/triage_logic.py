# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure triage logic — no Tryton dependency (unit-testable).

afya_triage.py imports from here; tests import this module directly.
"""
import json

TRIAGE_LEVELS = ['green', 'yellow', 'red', 'emergency']
RATIONALE_REQUIRED_KEYS = frozenset({'level', 'confidence', 'red_flags', 'model_version'})


class TriageLogicError(ValueError):
    pass


def validate_rationale(value):
    if not value:
        return True
    try:
        data = json.loads(value)
    except (TypeError, ValueError):
        raise TriageLogicError('clinical_rationale must be valid JSON.')
    if not isinstance(data, dict):
        raise TriageLogicError('clinical_rationale must be a JSON object.')
    missing = RATIONALE_REQUIRED_KEYS - set(data.keys())
    if missing:
        raise TriageLogicError('clinical_rationale missing keys: %s' % sorted(missing))
    if data.get('level') not in TRIAGE_LEVELS:
        raise TriageLogicError('clinical_rationale.level must be one of %s' % TRIAGE_LEVELS)
    conf = data.get('confidence')
    if not isinstance(conf, (int, float)) or not 0 <= conf <= 1:
        raise TriageLogicError('clinical_rationale.confidence must be in [0,1].')
    if not isinstance(data.get('red_flags'), list):
        raise TriageLogicError('clinical_rationale.red_flags must be a list.')
    return True


def detect_emergency_keywords(text, keywords):
    if not text:
        return []
    lowered = text.lower()
    seen, matched = set(), []
    for term, _lang in keywords:
        t = (term or '').lower()
        if t and t in lowered and t not in seen:
            seen.add(t)
            matched.append(term)
    return matched


def needs_human_review(triage_level):
    return triage_level == 'emergency'
