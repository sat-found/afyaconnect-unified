"""Pytest path bootstrapping: expose pure-logic modules without Tryton."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for sub in [
        os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_core'),
        os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_triage'),
        os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_dispatch'),
        os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_diaspora'),
        os.path.join(ROOT, 'gnuhealth', 'gnuhealth_afya_analytics'),
        os.path.join(ROOT, 'services')]:
    if sub not in sys.path:
        sys.path.insert(0, sub)
