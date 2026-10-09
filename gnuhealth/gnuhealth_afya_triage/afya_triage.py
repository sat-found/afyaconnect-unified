# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Triage session: state machine, protected-field guards, rationale validation,
keyword detection, TTL purge. Security PoC pattern (G0 T012–T017) applied."""
import json
import logging
from datetime import datetime, timedelta

from trytond.exceptions import UserError
from trytond.model import ModelSQL, ModelView, Workflow, fields
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction

from trytond.modules.gnuhealth_afya_core.afya_utils import redact_phone_numbers

logger = logging.getLogger(__name__)

PROTECTED_FIELDS = frozenset({
    'clinical_rationale',
    'triage_level',
    'triage_confidence',
    'symptoms_raw',
})

REVIEWER_FIELDS = frozenset({
    'reviewer_decision',
    'reviewer_notes',
    'review_timestamp',
})

RATIONALE_REQUIRED_KEYS = frozenset({'level', 'confidence', 'red_flags', 'model_version'})

TRIAGE_LEVELS = ['green', 'yellow', 'red', 'emergency']


def validate_rationale(value):
    """Validate clinical rationale JSON (§5.1). Pure function — unit-testable."""
    if not value:
        return True
    try:
        data = json.loads(value)
    except (TypeError, ValueError):
        raise UserError('clinical_rationale must be valid JSON.')
    if not isinstance(data, dict):
        raise UserError('clinical_rationale must be a JSON object.')
    missing = RATIONALE_REQUIRED_KEYS - set(data.keys())
    if missing:
        raise UserError('clinical_rationale missing keys: %s' % sorted(missing))
    if data.get('level') not in TRIAGE_LEVELS:
        raise UserError('clinical_rationale.level must be one of %s' % TRIAGE_LEVELS)
    conf = data.get('confidence')
    if not isinstance(conf, (int, float)) or not 0 <= conf <= 1:
        raise UserError('clinical_rationale.confidence must be in [0,1].')
    if not isinstance(data.get('red_flags'), list):
        raise UserError('clinical_rationale.red_flags must be a list.')
    return True


def detect_emergency_keywords(text, keywords):
    """Case-insensitive substring match. Pure function — unit-testable.

    text: free input; keywords: iterable of (term, language).
    Returns list of matched terms (deduplicated, order-stable).
    """
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


class TriageSession(Workflow, ModelSQL, ModelView):
    "AfyaConnect Triage Session"
    __name__ = 'gnuhealth.afya.triage_session'
    _rec_name = 'session_id'

    session_id = fields.Char('Session ID', required=True)
    session_start_time = fields.DateTime('Session Start')
    symptoms_raw = fields.Text('Symptoms Raw')
    symptoms_raw_expires_at = fields.DateTime('symptoms_raw Expires At')
    clinical_rationale = fields.Text('Clinical Rationale JSON')
    triage_level = fields.Selection([
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('emergency', 'Emergency'),
        ], 'Triage Level', sort=False)
    triage_confidence = fields.Float('Triage Confidence')
    human_review_required = fields.Boolean('Human Review Required')
    posthoc_consent_needed = fields.Boolean('Post-Hoc Consent Needed')
    consent = fields.Many2One('gnuhealth.afya.consent_record', 'Consent')
    access_session = fields.Many2One(
        'gnuhealth.afya.access_session', 'Access Session')

    reviewer_decision = fields.Selection([
        (None, ''),
        ('confirmed', 'Confirmed'),
        ('overridden', 'Overridden'),
        ('rejected', 'Rejected'),
        ], 'Reviewer Decision', sort=False, readonly=True)
    reviewer_notes = fields.Text('Reviewer Notes', readonly=True)
    review_timestamp = fields.DateTime('Review Timestamp', readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('reviewed', 'Reviewed'),
        ('escalated', 'Escalated'),
        ('cancelled', 'Cancelled'),
        ], 'State', readonly=True, sort=False)

    @staticmethod
    def default_state():
        return 'draft'

    @staticmethod
    def default_human_review_required():
        return False

    @staticmethod
    def default_posthoc_consent_needed():
        return False

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._transitions |= {
            ('draft', 'completed'),
            ('completed', 'reviewed'),
            ('completed', 'escalated'),
            ('completed', 'cancelled'),
            ('reviewed', 'escalated'),
        }
        cls._buttons.update({
            'complete': {'invisible': ~Eval('state').in_(['draft'])},
            'review': {'invisible': ~(Eval('state').in_(['completed'])
                & Eval('human_review_required', False))},
        })

    @classmethod
    def _is_admin(cls):
        pool = Pool()
        User = pool.get('res.user')
        user = User(Transaction().user)
        for group in user.groups:
            if 'Afya Administrator' in (group.name or ''):
                return True
        return user.login == 'admin'

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        for sessions, values in zip(actions, actions):
            val_keys = set(values.keys())
            ctx = Transaction().context
            if val_keys & PROTECTED_FIELDS:
                if not ctx.get('_afya_allow_protected_write') and not cls._is_admin():
                    raise UserError(
                        'Protected triage fields cannot be modified directly.')
            if val_keys & REVIEWER_FIELDS:
                if not ctx.get('_afya_review_wizard'):
                    raise UserError(
                        'Reviewer fields can only be set via Review Triage wizard.')
        return super().write(*args)

    @classmethod
    def create(cls, vlist):
        vlist = [dict(x) for x in vlist]
        pool = Pool()
        Config = pool.get('gnuhealth.afya.config')
        ttl_days = 30
        try:
            configs = Config.search([], limit=1)
            if configs:
                ttl_days = configs[0].symptoms_raw_ttl_days or 30
        except Exception:  # pragma: no cover - DB unavailable
            pass
        for values in vlist:
            if values.get('clinical_rationale'):
                validate_rationale(values['clinical_rationale'])
            if values.get('symptoms_raw'):
                values['symptoms_raw'] = redact_phone_numbers(values['symptoms_raw'])
                values['symptoms_raw_expires_at'] = (
                    datetime.now() + timedelta(days=ttl_days))
        return super().create(vlist)

    @classmethod
    @ModelView.button
    @Workflow.transition('completed')
    def complete(cls, sessions):
        for session in sessions:
            if session.triage_level == 'emergency':
                cls.write([session], {'human_review_required': True})

    @classmethod
    @ModelView.button_action('gnuhealth_afya_triage.wizard_review_triage')
    def review(cls, sessions):
        pass

    @classmethod
    @ModelView.button_action('gnuhealth_afya_triage.wizard_create_evaluation')
    def create_evaluation(cls, sessions):
        pass

    @classmethod
    @Workflow.transition('reviewed')
    def reviewed(cls, sessions):
        pass

    @classmethod
    @Workflow.transition('escalated')
    def escalate(cls, sessions):
        pass

    @classmethod
    @Workflow.transition('cancelled')
    def cancel(cls, sessions):
        pass

    @classmethod
    def purge_expired_symptoms_raw(cls):
        expired = cls.search([
            ('symptoms_raw', '!=', None),
            ('symptoms_raw_expires_at', '<', datetime.now()),
        ])
        if expired:
            with Transaction().set_context(_afya_allow_protected_write=True):
                cls.write(expired, {'symptoms_raw': None})
            logger.info('Purged symptoms_raw from %d triage sessions', len(expired))
        return len(expired)


class EmergencyKeyword(ModelSQL, ModelView):
    "Emergency Keyword"
    __name__ = 'gnuhealth.afya.emergency_keyword'
    _rec_name = 'term'

    term = fields.Char('Term', required=True)
    language = fields.Selection([
        ('en', 'English'),
        ('ha', 'Hausa'),
        ('ff', 'Fulfulde'),
        ], 'Language', required=True)
    active = fields.Boolean('Active')

    @staticmethod
    def default_active():
        return True
