"""Consent model selections (T008 — categorical, no free text)."""
import re
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = open(os.path.join(REPO, 'gnuhealth/gnuhealth_afya_core/afya_core.py')).read()


def test_consent_selections():
    for token in ['emergency_limited_processing', 'health_worker', 'analytics',
            'notes_category', 'party.party']:
        assert token in SRC


def test_no_textarea_notes_field():
    assert not re.search(r"notes\s*=\s*fields\.Text", SRC)
