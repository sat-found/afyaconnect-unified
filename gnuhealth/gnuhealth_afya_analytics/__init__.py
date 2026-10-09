# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from . import afya_analytics
from trytond.pool import Pool


def register():
    Pool.register(
        afya_analytics.AnalyticsOutbox,
        afya_analytics.ResourceSnapshot,
        module='gnuhealth_afya_analytics', type_='model')
