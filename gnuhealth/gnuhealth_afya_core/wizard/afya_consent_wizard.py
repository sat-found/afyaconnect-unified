# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from trytond.exceptions import UserError
from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateTransition, StateView, Button


class ResolvePostHocConsentStart(ModelView):
    'Resolve Post-Hoc Consent Start'
    __name__ = 'gnuhealth.afya.resolve_posthoc_consent.start'

    resolution_consent = fields.Many2One(
        'gnuhealth.afya.consent_record', 'Resolution Consent', required=True)


class ResolvePostHocConsent(Wizard):
    'Resolve Post-Hoc Consent (sole writer of task resolution)'
    __name__ = 'gnuhealth.afya.resolve_posthoc_consent'

    start = StateView(
        'gnuhealth.afya.resolve_posthoc_consent.start',
        'gnuhealth_afya_core.resolve_posthoc_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Resolve', 'resolve', 'tryton-ok', default=True),
        ])
    resolve = StateTransition()

    def transition_resolve(self):
        pool = Pool()
        Task = pool.get('gnuhealth.afya.posthoc_consent_task')
        tasks = Task.browse(Transaction().context.get('active_ids'))
        if not tasks:
            raise UserError('No post-hoc consent tasks selected.')
        with Transaction().set_context(_afya_consent_wizard=True):
            Task.write(tasks, {
                'resolution_consent': self.start.resolution_consent.id,
                'resolved': True,
            })
        return 'end'
