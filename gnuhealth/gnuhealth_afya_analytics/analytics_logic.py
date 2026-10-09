# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure analytics logic — no Tryton dependency (unit-testable)."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'gnuhealth_afya_core'))

from afya_utils import (  # noqa: E402
    anonymize_payload, coarsen_region, validate_analytics_payload)


def build_outbox_event(event_id, event_type, triage_level, channel,
                       language, sector_count, lga_count, state_count,
                       threshold=10, created_at=None):
    """Build a validated BigQuery-safe outbox dict."""
    from datetime import datetime, timezone
    level, code = coarsen_region(
        sector_count, lga_count, state_count, threshold)
    payload = {
        'event_id': event_id,
        'event_type': event_type,
        'triage_level': triage_level,
        'coarse_region': code or level,
        'region_level': level,
        'channel': channel,
        'language': language,
        'created_at': created_at or datetime.now(timezone.utc).isoformat(),
        'k_count': max(sector_count, lga_count, state_count),
    }
    validate_analytics_payload(payload)
    return anonymize_payload(payload)


def build_snapshot_values(facility_name, beds_available, ambulances_available):
    """Validate + build a coarse resource snapshot dict."""
    beds = int(beds_available)
    ambulances = int(ambulances_available)
    if beds < 0 or ambulances < 0:
        raise ValueError('snapshot counts must be non-negative')
    if not facility_name:
        raise ValueError('snapshot needs a coarse facility name')
    return {
        'facility_name': facility_name,
        'beds_available': beds,
        'ambulances_available': ambulances,
    }
