# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from trytond.exceptions import UserError
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateTransition, StateView, Button


class CreateDispatchCandidateStart(ModelView):
    'Create Dispatch Candidate Start'
    __name__ = 'gnuhealth.afya.create_dispatch_candidate.start'

    triage_session = fields.Many2One(
        'gnuhealth.afya.triage_session', 'Triage Session', required=True)
    event_type = fields.Char('Event Type', required=True)
    priority = fields.Selection([
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergent', 'Emergent'),
        ], 'Priority', required=True)


class CreateDispatchCandidate(Wizard):
    'Create Dispatch Candidate (STOPS at candidate — human gate required)'
    __name__ = 'gnuhealth.afya.create_dispatch_candidate'

    start = StateView(
        'gnuhealth.afya.create_dispatch_candidate.start',
        'gnuhealth_afya_dispatch.create_candidate_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Create Candidate', 'create_', 'tryton-ok', default=True),
        ])
    create_ = StateTransition()

    def transition_create_(self):
        pool = Pool()
        Dispatch = pool.get('gnuhealth.afya.dispatch_request')
        Dispatch.create([{
            'dispatch_ref': 'DSP-%s' % self.start.triage_session.session_id,
            'triage_session': self.start.triage_session.id,
            'event_type': self.start.event_type,
            'priority': self.start.priority,
        }])
        return 'end'


class ApproveDispatchStart(ModelView):
    'Approve Dispatch Start'
    __name__ = 'gnuhealth.afya.approve_dispatch.start'

    ambulance_id = fields.Char('Ambulance ID', required=True)
    eta_minutes = fields.Integer('ETA (minutes)', required=True)
    destination = fields.Many2One('gnuhealth.institution', 'Destination')


class ApproveDispatch(Wizard):
    'Approve Dispatch (dispatcher group only)'
    __name__ = 'gnuhealth.afya.approve_dispatch'

    start = StateView(
        'gnuhealth.afya.approve_dispatch.start',
        'gnuhealth_afya_dispatch.approve_dispatch_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Approve', 'approve', 'tryton-ok', default=True),
        ])
    approve = StateTransition()

    def transition_approve(self):
        pool = Pool()
        Dispatch = pool.get('gnuhealth.afya.dispatch_request')
        requests = Dispatch.browse(Transaction().context.get('active_ids'))
        if not requests:
            raise UserError('No dispatch requests selected.')
        with Transaction().set_context(_afya_dispatch_wizard=True):
            Dispatch.write(requests, {
                'ambulance_id': self.start.ambulance_id,
                'eta_minutes': self.start.eta_minutes,
            })
            Dispatch.do_approve(requests)
        return 'end'
