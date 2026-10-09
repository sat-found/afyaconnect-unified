# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure diaspora logic — no Tryton dependency (unit-testable)."""

CONSULT_EVENT_TYPES = [
    'scheduled',
    'audio_started',
    'audio_ended',
    'held',
    'closed',
    'cancelled',
]


def match_score(specialist_specialty, needed_specialty,
                specialist_langs, needed_lang):
    """Mock matching score 0..1. Specialty fit dominates, language breaks ties."""
    score = 0.3
    if specialist_specialty == needed_specialty:
        score += 0.5
    if needed_lang in (specialist_langs or []):
        score += 0.2
    return round(min(score, 1.0), 2)


def is_valid_consult_event(event_type):
    return event_type in CONSULT_EVENT_TYPES
