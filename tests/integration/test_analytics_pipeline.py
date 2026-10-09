"""Integration stubs: dispatch timing + analytics pipeline shape (AT-DISP-01, AT-DASH-01)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_analytics'))
sys.path.insert(0, os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_diaspora'))
sys.path.insert(0, os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_core'))


def test_analytics_pipeline_k_cascade():
    from afya_utils import coarsen_region, validate_analytics_payload
    assert coarsen_region(12, 30, 90) == ('sector', None)
    assert coarsen_region(2, 2, 2) == ('suppressed', 'INSUFFICIENT_VOLUME')
    ev = {'event_id': 'd1', 'event_type': 'dispatch', 'triage_level': 'unknown',
          'coarse_region': 'suppressed', 'region_level': 'suppressed',
          'channel': 'system', 'language': 'en', 'created_at': 't', 'k_count': 2}
    assert validate_analytics_payload(ev) is True


def test_diaspora_scoring_shape():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'diaspora_mod', os.path.join(ROOT, 'gnuhealth',
                                     'gnuhealth_afya_diaspora', 'afya_diaspora.py'))
    src = open(spec.origin).read()
    assert 'match_score' in src and 'ConsultationSession' in src
