"""Tryton view/model consistency: every view has arch; every arch field and
button resolves against the model definition. Guards T044–T048 at CI time."""
import glob
import os
import re
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GNU = os.path.join(REPO, 'gnuhealth')

IMPLICIT_FIELDS = {'id', 'create_date', 'write_date', 'create_uid', 'write_uid', 'rec_name'}

# model __name__ -> (py source, defined fields, defined methods)
MODELS = {}


def _index():
    for py in glob.glob(os.path.join(GNU, '*', '*.py')) + glob.glob(
            os.path.join(GNU, '*', 'wizard', '*.py')):
        src = open(py).read()
        fields = set(re.findall(r"(\w+)\s*=\s*fields\.", src))
        methods = set(re.findall(r"def\s+(\w+)\s*\(", src))
        for name in re.findall(r"__name__\s*=\s*'([^']+)'", src):
            MODELS[name] = (py, fields, methods)


_index()
assert MODELS, 'no Tryton models indexed'


def _views():
    out = []
    for xml in glob.glob(os.path.join(GNU, '**', '*.xml'), recursive=True):
        root = ET.parse(xml).getroot()
        for rec in root.iter('record'):
            if rec.get('model') != 'ir.ui.view':
                continue
            vals = {f.get('name'): (f.text or '').strip()
                for f in rec.iter('field') if f.get('name') in ('model', 'type', 'name')}
            arch = [f for f in rec.iter('field') if f.get('name') == 'arch']
            out.append((xml, rec.get('id'), vals, arch[0] if arch else None))
    return out


def test_all_views_have_arch():
    missing = ['%s#%s' % (xml, rid) for xml, rid, _v, arch in _views() if arch is None]
    assert not missing, 'views without arch: %s' % missing


def test_arch_fields_exist_on_model():
    problems = []
    for xml, rid, vals, arch in _views():
        model = vals.get('model')
        assert model in MODELS, '%s#%s references unknown model %s' % (xml, rid, model)
        _py, fields, _methods = MODELS[model]
        inner = (arch.text or '').strip()
        anode = ET.fromstring(inner)
        assert anode.tag in ('form', 'tree', 'graph', 'calendar', 'kanban'), \
            '%s#%s bad arch root %s' % (xml, rid, anode.tag)
        for f in anode.iter('field'):
            if f.get('name') not in fields | IMPLICIT_FIELDS:
                problems.append('%s#%s: unknown field %s on %s'
                    % (os.path.basename(xml), rid, f.get('name'), model))
    assert not problems, problems


def test_arch_buttons_exist_and_guarded():
    problems, unguarded = [], []
    for xml, rid, vals, arch in _views():
        model = vals.get('model')
        _py, _fields, methods = MODELS[model]
        inner = (arch.text or '').strip()
        for b in ET.fromstring(inner).iter('button'):
            name = b.get('name')
            if name and name not in methods:
                problems.append('%s#%s: button %s has no method on %s'
                    % (os.path.basename(xml), rid, name, model))
            if (model in ('gnuhealth.afya.triage_session',
                    'gnuhealth.afya.dispatch_request')
                    and name not in ('complete', 'begin', 'close',
                        'mark_triaged', 'en_route', 'arrive',
                        'complete_dispatch', 'cancel', 'escalate', 'reviewed')
                    and not b.get('groups')):
                unguarded.append('%s#%s: button %s lacks groups='
                    % (os.path.basename(xml), rid, name))
    assert not problems, problems
    assert not unguarded, unguarded
