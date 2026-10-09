# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from . import afya_dispatch
from .wizard import afya_dispatch_wizard
from trytond.pool import Pool


def register():
    Pool.register(
        afya_dispatch.DispatchRequest,
        afya_dispatch.KitTemplate,
        afya_dispatch_wizard.CreateDispatchCandidateStart,
        afya_dispatch_wizard.ApproveDispatchStart,
        module='gnuhealth_afya_dispatch', type_='model')
    Pool.register(
        afya_dispatch_wizard.CreateDispatchCandidate,
        afya_dispatch_wizard.ApproveDispatch,
        module='gnuhealth_afya_dispatch', type_='wizard')
