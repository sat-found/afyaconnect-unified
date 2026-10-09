"""Privacy + consent invariants (AT-PRIV-01, T008)."""
import ast
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _parse(rel):
    with open(os.path.join(REPO, rel)) as fh:
        return ast.parse(fh.read())


def test_no_free_text_in_consent_model():
    tree = _parse('gnuhealth/gnuhealth_afya_core/afya_core.py')
    src = ast.dump(tree)
    assert 'notes_category' in src
    assert 'FreeText' not in src.replace('free text', '')


def test_protected_guard_strings_present():
    for rel in ['gnuhealth/gnuhealth_afya_triage/afya_triage.py',
                'gnuhealth/gnuhealth_afya_dispatch/afya_dispatch.py']:
        with open(os.path.join(REPO, rel)) as fh:
            src = fh.read()
        assert '_wizard' in src  # context-gated writes only
        assert 'UserError' in src


def test_outbox_builder_is_safe():
    import sys
    sys.path.insert(0, os.path.join(REPO, 'services'))
    from common import validate_analytics
    ev = {'event_id': 'triage-1', 'event_type': 'triage', 'triage_level': 'red',
          'coarse_region': 'lga', 'region_level': 'lga', 'channel': 'ussd',
          'language': 'ha', 'created_at': '2026-01-01', 'k_count': 15}
    assert validate_analytics(ev) is True
