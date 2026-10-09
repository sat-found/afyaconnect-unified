# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Diaspora: specialists, case briefs, consultations, scored matches."""
from trytond.model import ModelSQL, ModelView, Workflow, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateTransition, StateView, Button


def match_score(specialist_specialty, needed_specialty,
        specialist_langs, needed_lang):
    """Mock matching score 0..1. Pure function — unit-testable."""
    score = 0.3
    if specialist_specialty == needed_specialty:
        score += 0.5
    if needed_lang in (specialist_langs or []):
        score += 0.2
    return round(min(score, 1.0), 2)


class DiasporaSpecialist(ModelSQL, ModelView):
    "Diaspora Specialist"
    __name__ = 'gnuhealth.afya.diaspora_specialist'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    specialty = fields.Char('Specialty', required=True)
    languages = fields.Char('Languages (comma-separated)')
    timezone = fields.Char('Timezone')
    active = fields.Boolean('Active')

    @staticmethod
    def default_active():
        return True

    def language_list(self):
        return [x.strip() for x in (self.languages or '').split(',') if x.strip()]


class CaseBrief(ModelSQL, ModelView):
    "Case Brief (categorical — no free text)"
    __name__ = 'gnuhealth.afya.case_brief'
    _rec_name = 'brief_ref'

    brief_ref = fields.Char('Brief Ref', required=True)
    triage_session = fields.Many2One(
        'gnuhealth.afya.triage_session', 'Triage Session')
    specialty_needed = fields.Char('Specialty Needed', required=True)
    language_needed = fields.Char('Language Needed')
    urgency = fields.Selection([
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergent', 'Emergent'),
        ], 'Urgency', sort=False)


class ConsultationSession(Workflow, ModelSQL, ModelView):
    "Consultation Session (audio-only MVP)"
    __name__ = 'gnuhealth.afya.consultation_session'
    _rec_name = 'consult_ref'

    consult_ref = fields.Char('Consult Ref', required=True)
    case_brief = fields.Many2One('gnuhealth.afya.case_brief', 'Case Brief')
    specialist = fields.Many2One(
        'gnuhealth.afya.diaspora_specialist', 'Specialist')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('held', 'Held'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
        ], 'State', readonly=True, sort=False)

    @staticmethod
    def default_state():
        return 'scheduled'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._transitions |= {
            ('scheduled', 'held'),
            ('held', 'closed'),
            ('scheduled', 'cancelled'),
        }

    @classmethod
    @Workflow.transition('held')
    def hold(cls, sessions):
        pass

    @classmethod
    @Workflow.transition('closed')
    def close(cls, sessions):
        pass


class SpecialistMatch(ModelSQL, ModelView):
    "Specialist Match (scored)"
    __name__ = 'gnuhealth.afya.specialist_match'
    _rec_name = 'consultation'

    consultation = fields.Many2One(
        'gnuhealth.afya.consultation_session', 'Consultation')
    specialist = fields.Many2One(
        'gnuhealth.afya.diaspora_specialist', 'Specialist')
    score = fields.Float('Score')
    rationale_category = fields.Selection([
        ('specialty_fit', 'Specialty fit'),
        ('language_fit', 'Language fit'),
        ('availability_fit', 'Availability fit'),
        ], 'Rationale Category', sort=False)


class MatchSpecialistStart(ModelView):
    'Match Specialist Start'
    __name__ = 'gnuhealth.afya.match_specialist.start'

    case_brief = fields.Many2One(
        'gnuhealth.afya.case_brief', 'Case Brief', required=True)


class MatchSpecialist(Wizard):
    'Match Specialist (mock scoring)'
    __name__ = 'gnuhealth.afya.match_specialist'

    start = StateView(
        'gnuhealth.afya.match_specialist.start',
        'gnuhealth_afya_diaspora.match_specialist_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Match', 'match', 'tryton-ok', default=True),
        ])
    match = StateTransition()

    def transition_match(self):
        pool = Pool()
        Specialist = pool.get('gnuhealth.afya.diaspora_specialist')
        Consultation = pool.get('gnuhealth.afya.consultation_session')
        Match = pool.get('gnuhealth.afya.specialist_match')
        brief = self.start.case_brief
        specialists = Specialist.search([('active', '=', True)])
        consults = Consultation.create([{
            'consult_ref': 'CONS-%s' % brief.brief_ref,
            'case_brief': brief.id,
        }])
        consult = consults[0]
        for spec in specialists:
            Match.create([{
                'consultation': consult.id,
                'specialist': spec.id,
                'score': match_score(
                    spec.specialty, brief.specialty_needed,
                    spec.language_list(), brief.language_needed or 'en'),
                'rationale_category': 'specialty_fit',
            }])
        return 'end'


class GenerateCaseBriefStart(ModelView):
    'Generate Case Brief Start'
    __name__ = 'gnuhealth.afya.generate_case_brief.start'

    triage_session = fields.Many2One(
        'gnuhealth.afya.triage_session', 'Triage Session', required=True)
    specialty_needed = fields.Char('Specialty Needed', required=True)
    urgency = fields.Selection([
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergent', 'Emergent'),
        ], 'Urgency', required=True)


class GenerateCaseBrief(Wizard):
    'Generate Case Brief'
    __name__ = 'gnuhealth.afya.generate_case_brief'

    start = StateView(
        'gnuhealth.afya.generate_case_brief.start',
        'gnuhealth_afya_diaspora.generate_brief_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Generate', 'generate', 'tryton-ok', default=True),
        ])
    generate = StateTransition()

    def transition_generate(self):
        pool = Pool()
        Brief = pool.get('gnuhealth.afya.case_brief')
        Brief.create([{
            'brief_ref': 'BRIEF-%s' % self.start.triage_session.session_id,
            'triage_session': self.start.triage_session.id,
            'specialty_needed': self.start.specialty_needed,
            'urgency': self.start.urgency,
        }])
        return 'end'
