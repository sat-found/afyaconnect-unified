# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from . import afya_diaspora
from trytond.pool import Pool


def register():
    Pool.register(
        afya_diaspora.DiasporaSpecialist,
        afya_diaspora.CaseBrief,
        afya_diaspora.ConsultationSession,
        afya_diaspora.SpecialistMatch,
        afya_diaspora.MatchSpecialistStart,
        afya_diaspora.GenerateCaseBriefStart,
        module='gnuhealth_afya_diaspora', type_='model')
    Pool.register(
        afya_diaspora.MatchSpecialist,
        afya_diaspora.GenerateCaseBrief,
        module='gnuhealth_afya_diaspora', type_='wizard')
