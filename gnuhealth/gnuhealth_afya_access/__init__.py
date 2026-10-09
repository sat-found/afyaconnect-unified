# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from trytond.pool import Pool
from . import afya_access


def register():
    Pool.register(
        afya_access.AccessSession,
        module='gnuhealth_afya_access', type_='model')
