# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Dispatch: 10-state machine, human-gate wizards, kit templates, NAERS stub."""
import logging
from datetime import datetime

from trytond.exceptions import UserError
from trytond.model import ModelSQL, ModelView, Workflow, fields
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction

logger = logging.getLogger(__name__)

PROTECTED_DISPATCH_FIELDS = frozenset({'ambulance_id', 'eta_minutes', 'destination_facility'})

KIT_TEMPLATES = [
    ('trauma', 'Trauma Kit'),
    ('obstetric', 'Obstetric Emergency Kit'),
    ('cardiac', 'Cardiac Emergency Kit'),
    ('pediatric', 'Pediatric Emergency Kit'),
    ('respiratory', 'Respiratory Emergency Kit'),
    ('burns', 'Burns Kit'),
    ('sepsis', 'Sepsis Kit'),
    ('stroke', 'Stroke Kit'),
    ('mass_casualty', 'Mass Casualty Kit'),
    ('general', 'General Emergency Kit'),
]


def naers_accept_stub(payload):
    """NAERS stub (disclosed): accept + return mock assignment. No network."""
    ref = 'NAERS-%s' % (abs(hash(str(sorted(payload.items())))) % 90000 + 10000)
    return {
        'status': 'accepted (STUB)',
        'assignment_ref': ref,
        'eta_minutes': 25,
        'accepted_at': datetime.utcnow().isoformat() + 'Z',
    }


class DispatchRequest(Workflow, ModelSQL, ModelView):
    "AfyaConnect Dispatch Request"
    __name__ = 'gnuhealth.afya.dispatch_request'
    _rec_name = 'dispatch_ref'

    dispatch_ref = fields.Char('Dispatch Ref', required=True)
    triage_session = fields.Many2One(
        'gnuhealth.afya.triage_session', 'Triage Session')
    event_type = fields.Selection(
        [(k, v) for k, v in KIT_TEMPLATES],
        'Event Type', sort=False)
    priority = fields.Selection([
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergent', 'Emergent'),
        ], 'Priority', sort=False)
    ambulance_id = fields.Char('Ambulance ID', readonly=True)
    eta_minutes = fields.Integer('ETA (minutes)', readonly=True)
    destination_facility = fields.Many2One(
        'gnuhealth.institution', 'Destination Facility')
    state = fields.Selection([
        ('candidate', 'Candidate'),
        ('approved', 'Approved'),
        ('submitted', 'Submitted'),
        ('en_route', 'En Route'),
        ('arrived', 'Arrived'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
        ('failed', 'Failed'),
        ('returned', 'Returned'),
        ], 'State', readonly=True, sort=False)

    @staticmethod
    def default_state():
        return 'candidate'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._transitions |= {
            ('candidate', 'approved'),
            ('candidate', 'rejected'),
            ('candidate', 'cancelled'),
            ('approved', 'submitted'),
            ('approved', 'cancelled'),
            ('submitted', 'en_route'),
            ('submitted', 'failed'),
            ('en_route', 'arrived'),
            ('en_route', 'failed'),
            ('arrived', 'completed'),
            ('arrived', 'returned'),
        }
        cls._buttons.update({
            'approve': {'invisible': ~Eval('state').in_(['candidate'])},
            'submit': {'invisible': ~Eval('state').in_(['approved'])},
        })

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        for requests, values in zip(actions, actions):
            if set(values) & PROTECTED_DISPATCH_FIELDS:
                ctx = Transaction().context
                if not ctx.get('_afya_dispatch_wizard'):
                    raise UserError(
                        'Dispatch assignment fields are wizard-only.')
        return super().write(*args)

    @classmethod
    @ModelView.button_action('gnuhealth_afya_dispatch.wizard_approve_dispatch')
    def approve(cls, requests):
        pass

    @classmethod
    @Workflow.transition('approved')
    def do_approve(cls, requests):
        pass

    @classmethod
    @Workflow.transition('submitted')
    def submit(cls, requests):
        for req in requests:
            resp = naers_accept_stub({'dispatch_ref': req.dispatch_ref})
            logger.info('NAERS stub accepted %s -> %s',
                req.dispatch_ref, resp['assignment_ref'])

    @classmethod
    @Workflow.transition('en_route')
    def en_route(cls, requests):
        pass

    @classmethod
    @Workflow.transition('arrived')
    def arrive(cls, requests):
        pass

    @classmethod
    @Workflow.transition('completed')
    def complete_dispatch(cls, requests):
        pass


class KitTemplate(ModelSQL, ModelView):
    "Dispatch Kit Template"
    __name__ = 'gnuhealth.afya.kit_template'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    event_type = fields.Char('Event Type', required=True)
    items_json = fields.Char('Items (JSON)')
    active = fields.Boolean('Active')

    @staticmethod
    def default_active():
        return True
