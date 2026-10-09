# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from trytond.pool import Pool
from . import mosquito


def register():
    Pool.register(
        mosquito.MosquitoRegistration,
        module='mosquito_registration', type_='model')
