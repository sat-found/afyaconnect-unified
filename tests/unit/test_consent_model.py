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


def test_posthoc_resolution_is_wizard_only():
    assert '_afya_consent_wizard' in SRC
    assert 'resolution_consent' in SRC
    wiz = open(os.path.join(
        REPO, 'gnuhealth/gnuhealth_afya_core/wizard/afya_consent_wizard.py')).read()
    assert '_afya_consent_wizard=True' in wiz
    assert 'transition_resolve' in wiz
    assert "'resolved': True" in wiz or '"resolved": True' in wiz or "'resolved':True" in wiz
