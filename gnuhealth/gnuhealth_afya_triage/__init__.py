# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from . import afya_triage
from .wizard import afya_triage_wizard
from trytond.pool import Pool


def register():
    Pool.register(
        afya_triage.TriageSession,
        afya_triage.EmergencyKeyword,
        afya_triage_wizard.ReviewTriageStart,
        afya_triage_wizard.CreateEvaluationStart,
        module='gnuhealth_afya_triage', type_='model')
    Pool.register(
        afya_triage_wizard.ReviewTriage,
        afya_triage_wizard.CreateEvaluationFromTriage,
        module='gnuhealth_afya_triage', type_='wizard')
