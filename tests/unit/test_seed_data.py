"""Seed-data contract tests (T035/T038/T053/T054): module data + generated XML."""
import glob
import os
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _records(xml_rel, model):
    root = ET.parse(os.path.join(REPO, xml_rel)).getroot()
    return [r for r in root.iter('record') if r.get('model') == model]


def _field(rec, name):
    for f in rec.iter('field'):
        if f.get('name') == name:
            return (f.text or '').strip()
    return None


def test_ten_kit_templates_seeded():
    recs = _records('gnuhealth/gnuhealth_afya_dispatch/data/kit_templates.xml',
                    'gnuhealth.afya.kit_template')
    assert len(recs) == 10
    import sys
    sys.path.insert(0, os.path.join(REPO, 'gnuhealth', 'gnuhealth_afya_dispatch'))
    from dispatch_logic import KIT_TEMPLATES
    assert {r.get('id') for r in recs} == {'kit_%s' % k for k, _v in KIT_TEMPLATES}
    assert {_field(r, 'event_type') for r in recs} == {k for k, _v in KIT_TEMPLATES}
    import json
    for r in recs:
        items = json.loads(_field(r, 'items_json'))
        assert isinstance(items, list) and len(items) >= 3, r.get('id')


def test_five_diaspora_specialists_seeded():
    recs = _records('gnuhealth/gnuhealth_afya_diaspora/data/diaspora_specialists.xml',
                    'gnuhealth.afya.diaspora_specialist')
    assert len(recs) == 5
    specs = {_field(r, 'specialty') for r in recs}
    assert specs == {'cardiology', 'obstetrics', 'pediatrics', 'trauma', 'neurology'}
    langs = ' '.join(_field(r, 'languages') for r in recs)
    assert 'ha' in langs and 'ff' in langs  # Hausa + Fulfulde coverage


def test_generated_gombe_seed_counts():
    pats = _records('data/gombe_patients.xml', 'party.party')
    workers = _records('data/gombe_workers.xml', 'party.party')
    kws = _records('data/emergency_keywords.xml', 'gnuhealth.afya.emergency_keyword')
    facs = _records('data/gombe_facilities.xml', 'gnuhealth.institution')
    assert len(pats) == 200
    assert len(workers) == 20
    assert len(kws) == 52
    assert len(facs) == 50
    langs = {_field(k, 'language') for k in kws}
    assert langs == {'en', 'ha', 'ff'}


def test_all_module_data_xml_parse():
    files = glob.glob(os.path.join(REPO, 'gnuhealth', '*', 'data', '*.xml'))
    assert len(files) >= 4
    for f in files:
        ET.parse(f)
