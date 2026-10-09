# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Mosquito registration demo registry (ported as-is, renamed module dir)."""
from trytond.model import ModelSQL, ModelView, fields


class MosquitoRegistration(ModelSQL, ModelView):
    "Mosquito Registration"
    __name__ = 'mosquito.registration'
    _rec_name = 'code'

    code = fields.Char('Code', required=True)
    location = fields.Char('Location')
    active = fields.Boolean('Active')

    @staticmethod
    def default_active():
        return True
