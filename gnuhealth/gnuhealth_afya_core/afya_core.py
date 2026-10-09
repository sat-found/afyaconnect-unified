# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Core models: config singleton, consent, post-hoc tasks, external refs."""
from trytond.exceptions import UserError
from trytond.model import ModelSingleton, ModelSQL, ModelView, fields
from trytond.transaction import Transaction


class AfyaConfig(ModelSingleton, ModelView):
    "AfyaConnect Configuration (singleton, id=1)"
    __name__ = 'gnuhealth.afya.config'

    symptoms_raw_ttl_days = fields.Integer(
        'symptoms_raw TTL (days)', required=True,
        help='Days before symptoms_raw is purged by scheduled job')
    k_anonymity_threshold = fields.Integer(
        'k-anonymity threshold', required=True,
        help='Minimum count for analytics dashboard tiles')
    region_coarsening_cascade = fields.Char(
        'Region coarsening cascade',
        help='JSON cascade definition, e.g. sector>lga>state>suppressed')

    @staticmethod
    def default_symptoms_raw_ttl_days():
        return 30

    @staticmethod
    def default_k_anonymity_threshold():
        return 10

    @staticmethod
    def default_region_coarsening_cascade():
        return 'sector>lga>state>suppressed'


class ConsentRecord(ModelSQL, ModelView):
    "AfyaConnect Consent Record"
    __name__ = 'gnuhealth.afya.consent_record'
    _rec_name = 'consent_status'

    consent_status = fields.Selection([
        ('explicit', 'Explicit'),
        ('verbal', 'Verbal'),
        ('proxy', 'Proxy'),
        ('emergency_limited_processing', 'Emergency limited processing'),
        ('refused', 'Refused'),
        ('unavailable', 'Unavailable'),
        ], 'Consent Status', required=True, sort=False)
    consent_actor = fields.Selection([
        ('patient', 'Patient'),
        ('guardian', 'Guardian'),
        ('health_worker', 'Health worker'),
        ('unknown', 'Unknown'),
        ], 'Consent Actor', required=True, sort=False)
    consent_scope = fields.Selection([
        ('triage', 'Triage'),
        ('dispatch', 'Dispatch'),
        ('consultation', 'Consultation'),
        ('analytics', 'Analytics'),
        ], 'Consent Scope', required=True, sort=False)
    notes_category = fields.Selection([
        ('unconscious_patient', 'Unconscious patient'),
        ('minor_patient', 'Minor patient'),
        ('proxy_health_worker', 'Proxy health worker'),
        ('emergency_no_consent', 'Emergency no consent'),
        ('not_applicable', 'Not applicable'),
        ], 'Notes Category', required=True, sort=False)
    party = fields.Many2One(
        'party.party', 'Party',
        help='Patient/guardian/bystander — parties, not patients, for emergencies')


class PostHocConsentTask(ModelSQL, ModelView):
    "Post-Hoc Consent Task"
    __name__ = 'gnuhealth.afya.posthoc_consent_task'
    _rec_name = 'triage_session'

    party = fields.Many2One('party.party', 'Party')
    triage_session = fields.Many2One(
        'gnuhealth.afya.triage_session', 'Triage Session')
    triage_session_ref = fields.Char(
        'Triage Session Ref (legacy)',
        help='Session ID reference kept for migration compat')
    resolved = fields.Boolean('Resolved')
    resolution_consent = fields.Many2One(
        'gnuhealth.afya.consent_record', 'Resolution Consent',
        states={'readonly': True})

    @staticmethod
    def default_resolved():
        return False

    @classmethod
    def write(cls, *args):
        # Resolution is wizard-only: deferred consent must be captured
        # deliberately, never by casual edits (T009/T044).
        actions = iter(args)
        for _tasks, values in zip(actions, actions):
            if set(values) & {'resolved', 'resolution_consent'}:
                if not Transaction().context.get('_afya_consent_wizard'):
                    raise UserError(
                        'Post-hoc consent can only be resolved via the '
                        'Resolve wizard.')
        return super().write(*args)


class ExternalRef(ModelSQL, ModelView):
    "External System Reference"
    __name__ = 'gnuhealth.afya.external_ref'
    _rec_name = 'external_id'

    system = fields.Char('System', required=True)
    external_id = fields.Char('External ID', required=True)
    triage_session = fields.Many2One(
        'gnuhealth.afya.triage_session', 'Triage Session')
    access_session = fields.Many2One(
        'gnuhealth.afya.access_session', 'Access Session')
    triage_session_ref = fields.Char('Triage Session Ref (legacy)')
    access_session_ref = fields.Char('Access Session Ref (legacy)')
