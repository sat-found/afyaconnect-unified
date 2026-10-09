# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from trytond.pool import Pool
from . import afya_core
from .wizard import afya_consent_wizard


def register():
    Pool.register(
        afya_core.AfyaConfig,
        afya_core.ConsentRecord,
        afya_core.PostHocConsentTask,
        afya_core.ExternalRef,
        afya_consent_wizard.ResolvePostHocConsentStart,
        module='gnuhealth_afya_core', type_='model')
    Pool.register(
        afya_consent_wizard.ResolvePostHocConsent,
        module='gnuhealth_afya_core', type_='wizard')
