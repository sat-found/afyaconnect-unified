# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from trytond.pool import Pool
from . import afya_core


def register():
    Pool.register(
        afya_core.AfyaConfig,
        afya_core.ConsentRecord,
        afya_core.PostHocConsentTask,
        afya_core.ExternalRef,
        module='gnuhealth_afya_core', type_='model')
