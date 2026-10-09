# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from datetime import datetime

from trytond.exceptions import UserError
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateTransition, StateView, Button


class ReviewTriageStart(ModelView):
    'Review Triage Start'
    __name__ = 'gnuhealth.afya.review_triage.start'

    reviewer_decision = fields.Selection([
        ('confirmed', 'Confirmed'),
        ('overridden', 'Overridden'),
        ('rejected', 'Rejected'),
        ], 'Reviewer Decision', required=True)
    reviewer_notes = fields.Text('Reviewer Notes')


class ReviewTriage(Wizard):
    'Review Triage (reviewer-group only; sole writer of reviewer fields)'
    __name__ = 'gnuhealth.afya.review_triage'

    start = StateView(
        'gnuhealth.afya.review_triage.start',
        'gnuhealth_afya_triage.review_triage_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Submit Review', 'review', 'tryton-ok', default=True),
        ])
    review = StateTransition()

    def transition_review(self):
        pool = Pool()
        TriageSession = pool.get('gnuhealth.afya.triage_session')
        sessions = TriageSession.browse(Transaction().context.get('active_ids'))
        if not sessions:
            raise UserError('No triage sessions selected.')
        with Transaction().set_context(_afya_review_wizard=True):
            TriageSession.write(sessions, {
                'reviewer_decision': self.start.reviewer_decision,
                'reviewer_notes': self.start.reviewer_notes,
                'review_timestamp': datetime.now(),
            })
            TriageSession.reviewed(sessions)
        return 'end'


class CreateEvaluationStart(ModelView):
    'Create Evaluation Start'
    __name__ = 'gnuhealth.afya.create_evaluation.start'

    patient = fields.Many2One('gnuhealth.patient', 'Patient', required=True)
    icd10 = fields.Many2One('gnuhealth.pathology', 'Primary Diagnosis (ICD-10)')


class CreateEvaluationFromTriage(Wizard):
    'Create Evaluation From Triage'
    __name__ = 'gnuhealth.afya.create_evaluation'

    start = StateView(
        'gnuhealth.afya.create_evaluation.start',
        'gnuhealth_afya_triage.create_evaluation_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Create Evaluation', 'create_', 'tryton-ok', default=True),
        ])
    create_ = StateTransition()

    def transition_create_(self):
        pool = Pool()
        Evaluation = pool.get('gnuhealth.patient.evaluation')
        TriageSession = pool.get('gnuhealth.afya.triage_session')
        sessions = TriageSession.browse(Transaction().context.get('active_ids'))
        for session in sessions:
            Evaluation.create([{
                'patient': self.start.patient.id,
                'state': 'in_progress',
                'information': 'Created from triage %s (level=%s)' % (
                    session.session_id, session.triage_level),
            }])
        return 'end'
