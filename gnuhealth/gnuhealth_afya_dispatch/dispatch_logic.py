# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure dispatch logic — no Tryton dependency (unit-testable)."""
from datetime import datetime, timezone

KIT_TEMPLATES = [
    ('trauma', 'Trauma Kit'),
    ('obstetric', 'Obstetric Emergency Kit'),
    ('cardiac', 'Cardiac Emergency Kit'),
    ('pediatric', 'Pediatric Emergency Kit'),
    ('respiratory', 'Respiratory Emergency Kit'),
    ('burns', 'Burns Kit'),
    ('sepsis', 'Sepsis Kit'),
    ('stroke', 'Stroke Kit'),
    ('mass_casualty', 'Mass Casualty Kit'),
    ('general', 'General Emergency Kit'),
]

DISPATCH_STATES = ['candidate', 'approved', 'submitted', 'en_route', 'arrived',
    'completed', 'cancelled', 'rejected', 'failed', 'returned']

DISPATCH_TRANSITIONS = {
    ('candidate', 'approved'), ('candidate', 'rejected'), ('candidate', 'cancelled'),
    ('approved', 'submitted'), ('approved', 'cancelled'),
    ('submitted', 'en_route'), ('submitted', 'failed'),
    ('en_route', 'arrived'), ('en_route', 'failed'),
    ('arrived', 'completed'), ('arrived', 'returned'),
}


def naers_accept_stub(payload):
    ref = 'NAERS-%s' % (abs(hash(str(sorted(payload.items())))) % 90000 + 10000)
    return {
        'status': 'accepted (STUB)',
        'assignment_ref': ref,
        'eta_minutes': 25,
        'accepted_at': datetime.now(timezone.utc).isoformat(),
    }


def is_valid_transition(frm, to):
    return (frm, to) in DISPATCH_TRANSITIONS
