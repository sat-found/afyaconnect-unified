# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Analytics outbox with k-anonymity cascade + schema validation."""
from trytond.model import ModelSQL, ModelView, fields

try:
    from trytond.modules.gnuhealth_afya_analytics.analytics_logic import (
        build_outbox_event, build_snapshot_values)
except ImportError:  # local test path
    from .analytics_logic import build_outbox_event, build_snapshot_values

# Re-exported for Tryton callers; __all__ keeps pyflakes quiet.
__all__ = ['build_outbox_event', 'build_snapshot_values',
           'AnalyticsOutbox', 'ResourceSnapshot']


class AnalyticsOutbox(ModelSQL, ModelView):
    "Analytics Outbox (BigQuery-safe only)"
    __name__ = 'gnuhealth.afya.analytics_outbox'
    _rec_name = 'event_id'

    event_id = fields.Char('Event ID', required=True)
    event_type = fields.Char('Event Type', required=True)
    triage_level = fields.Char('Triage Level')
    coarse_region = fields.Char('Coarse Region')
    region_level = fields.Char('Region Level')
    channel = fields.Char('Channel')
    language = fields.Char('Language')
    exported = fields.Boolean('Exported')

    @staticmethod
    def default_exported():
        return False

    @classmethod
    def create_from_triage(cls, triage, sector_count, lga_count,
                           state_count, threshold=10):
        event = build_outbox_event(
            'triage-%s' % triage.session_id, 'triage',
            triage.triage_level or 'unknown', 'ussd',
            'en', sector_count, lga_count, state_count, threshold)
        return cls.create([{
            'event_id': event['event_id'],
            'event_type': event['event_type'],
            'triage_level': event['triage_level'],
            'coarse_region': event['coarse_region'],
            'region_level': event['region_level'],
            'channel': event['channel'],
            'language': event['language'],
        }])

    @classmethod
    def create_from_dispatch(cls, dispatch, sector_count, lga_count,
                             state_count, threshold=10):
        event = build_outbox_event(
            'dispatch-%s' % dispatch.dispatch_ref, 'dispatch',
            'unknown', 'system', 'en',
            sector_count, lga_count, state_count, threshold)
        return cls.create([{
            'event_id': event['event_id'],
            'event_type': event['event_type'],
            'triage_level': event['triage_level'],
            'coarse_region': event['coarse_region'],
            'region_level': event['region_level'],
            'channel': event['channel'],
            'language': event['language'],
        }])

    @classmethod
    def pending(cls, limit=500):
        return cls.search([('exported', '=', False)], limit=limit)


class ResourceSnapshot(ModelSQL, ModelView):
    "Facility Resource Snapshot"
    __name__ = 'gnuhealth.afya.resource_snapshot'
    _rec_name = 'facility'

    facility = fields.Many2One('gnuhealth.institution', 'Facility')
    facility_name = fields.Char('Facility Name (coarse)')
    beds_available = fields.Integer('Beds Available')
    ambulances_available = fields.Integer('Ambulances Available')

    @classmethod
    def create_snapshot(cls, facility_name, beds_available,
                        ambulances_available, facility=None):
        values = build_snapshot_values(
            facility_name, beds_available, ambulances_available)
        if facility is not None:
            values['facility'] = facility
        return cls.create([values])
