# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Access sessions: USSD/SMS/voice/web entry points. Language + Fulfulde fallback."""
from trytond.model import ModelSQL, ModelView, Workflow, fields
from trytond.pyson import Eval


class AccessSession(Workflow, ModelSQL, ModelView):
    "AfyaConnect Access Session"
    __name__ = 'gnuhealth.afya.access_session'
    _rec_name = 'session_id'

    session_id = fields.Char('Session ID', required=True)
    channel = fields.Selection([
        ('ussd', 'USSD'),
        ('sms', 'SMS'),
        ('voice', 'Voice'),
        ('web', 'Web'),
        ], 'Channel', required=True, sort=False)
    language = fields.Selection([
        ('en', 'English'),
        ('ha', 'Hausa'),
        ('ff', 'Fulfulde'),
        ], 'Language', required=True, sort=False)
    detected_language = fields.Char('Detected Language')
    language_confidence = fields.Float('Language Confidence')
    fulfulde_fallback = fields.Boolean('Fulfulde Fallback')
    interaction_count = fields.Integer('Interaction Count')
    triage_session = fields.Many2One(
        'gnuhealth.afya.triage_session', 'Triage Session')
    state = fields.Selection([
        ('opened', 'Opened'),
        ('in_progress', 'In Progress'),
        ('triaged', 'Triaged'),
        ('closed', 'Closed'),
        ('abandoned', 'Abandoned'),
        ], 'State', readonly=True, sort=False)

    @staticmethod
    def default_state():
        return 'opened'

    @staticmethod
    def default_interaction_count():
        return 0

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._transitions |= {
            ('opened', 'in_progress'),
            ('in_progress', 'triaged'),
            ('in_progress', 'abandoned'),
            ('triaged', 'closed'),
            ('opened', 'abandoned'),
        }
        cls._buttons.update({
            'begin': {'invisible': ~Eval('state').in_(['opened'])},
            'mark_triaged': {'invisible': ~Eval('state').in_(['in_progress'])},
            'close': {'invisible': ~Eval('state').in_(['triaged'])},
        })

    @classmethod
    def create(cls, vlist):
        vlist = [dict(v) for v in vlist]
        for values in vlist:
            conf = values.get('language_confidence')
            if conf is not None and float(conf) < 0.70:
                values['fulfulde_fallback'] = True
        return super().create(vlist)

    @classmethod
    @Workflow.transition('in_progress')
    def begin(cls, sessions):
        pass

    @classmethod
    @Workflow.transition('triaged')
    def mark_triaged(cls, sessions):
        pass

    @classmethod
    @Workflow.transition('closed')
    def close(cls, sessions):
        pass
