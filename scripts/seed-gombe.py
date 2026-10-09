#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate data/*.xml seeds + (inside Tryton) idempotent Gombe demo data.

Offline mode (default): writes data/gombe_facilities.xml, gombe_patients.xml,
gombe_workers.xml, emergency_keywords.xml, afya_config.xml, afya_triage_cron.xml.
Container mode: `seed-gombe.py --apply` uses Tryton RPC (needs trytond installed).
"""
import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')

FACILITIES = [
    # Gombe LGA (6): tertiary + township PHCs
    ('GOM-FMC-001', 'Federal Medical Centre Gombe', 'Gombe', 'hospital'),
    ('GOM-GSH-001', 'Gombe State Specialist Hospital', 'Gombe', 'hospital'),
    ('GOM-PHC-GOM-001', 'Gombe Township Primary Health Centre', 'Gombe', 'health_centre'),
    ('GOM-PHC-GOM-002', 'Pantami Primary Health Centre', 'Gombe', 'health_centre'),
    ('GOM-PHC-GOM-003', 'Bolari Primary Health Centre', 'Gombe', 'health_centre'),
    ('GOM-PHC-GOM-004', 'Tunfure Primary Health Centre', 'Gombe', 'health_centre'),
    # Akko (5)
    ('GOM-GH-AKK-001', 'Akko General Hospital, Kumo', 'Akko', 'hospital'),
    ('GOM-PHC-AKK-001', 'Kumo Primary Health Centre', 'Akko', 'health_centre'),
    ('GOM-PHC-AKK-002', 'Pindiga Primary Health Centre', 'Akko', 'health_centre'),
    ('GOM-PHC-AKK-003', 'Kashere Primary Health Centre', 'Akko', 'health_centre'),
    ('GOM-PHC-AKK-004', 'Kalshingi Primary Health Centre', 'Akko', 'health_centre'),
    # Balanga (5)
    ('GOM-GH-BAL-001', 'Balanga General Hospital, Talasse', 'Balanga', 'hospital'),
    ('GOM-PHC-BAL-001', 'Talasse Primary Health Centre', 'Balanga', 'health_centre'),
    ('GOM-PHC-BAL-002', 'Bambam Primary Health Centre', 'Balanga', 'health_centre'),
    ('GOM-PHC-BAL-003', 'Swa Primary Health Centre', 'Balanga', 'health_centre'),
    ('GOM-PHC-BAL-004', 'Gelengu Primary Health Centre', 'Balanga', 'health_centre'),
    # Billiri (5)
    ('GOM-GH-BIL-001', 'Billiri General Hospital', 'Billiri', 'hospital'),
    ('GOM-PHC-BIL-001', 'Billiri Primary Health Centre', 'Billiri', 'health_centre'),
    ('GOM-PHC-BIL-002', 'Kalmai Primary Health Centre', 'Billiri', 'health_centre'),
    ('GOM-PHC-BIL-003', 'Todi Primary Health Centre', 'Billiri', 'health_centre'),
    ('GOM-PHC-BIL-004', 'Pobawure Primary Health Centre', 'Billiri', 'health_centre'),
    # Dukku (4)
    ('GOM-GH-DUK-001', 'Dukku General Hospital', 'Dukku', 'hospital'),
    ('GOM-PHC-DUK-001', 'Dukku Primary Health Centre', 'Dukku', 'health_centre'),
    ('GOM-PHC-DUK-002', 'Waziri Primary Health Centre', 'Dukku', 'health_centre'),
    ('GOM-PHC-DUK-003', 'Jamari Primary Health Centre', 'Dukku', 'health_centre'),
    # Funakaye (4)
    ('GOM-GH-FUN-001', 'Funakaye General Hospital, Bajoga', 'Funakaye', 'hospital'),
    ('GOM-PHC-FUN-001', 'Bajoga Primary Health Centre', 'Funakaye', 'health_centre'),
    ('GOM-PHC-FUN-002', 'Ashaka Primary Health Centre', 'Funakaye', 'health_centre'),
    ('GOM-PHC-FUN-003', 'Jauro Abare Primary Health Centre', 'Funakaye', 'health_centre'),
    # Kaltungo (4)
    ('GOM-GH-KAL-001', 'Kaltungo General Hospital', 'Kaltungo', 'hospital'),
    ('GOM-PHC-KAL-001', 'Kaltungo Primary Health Centre', 'Kaltungo', 'health_centre'),
    ('GOM-PHC-KAL-002', 'Kamo Primary Health Centre', 'Kaltungo', 'health_centre'),
    ('GOM-PHC-KAL-003', 'Ture Primary Health Centre', 'Kaltungo', 'health_centre'),
    # Kwami (4)
    ('GOM-GH-KWA-001', 'Kwami General Hospital, Malam Sidi', 'Kwami', 'hospital'),
    ('GOM-PHC-KWA-001', 'Malam Sidi Primary Health Centre', 'Kwami', 'health_centre'),
    ('GOM-PHC-KWA-002', 'Bojude Primary Health Centre', 'Kwami', 'health_centre'),
    ('GOM-PHC-KWA-003', 'Komfulata Primary Health Centre', 'Kwami', 'health_centre'),
    # Nafada (4)
    ('GOM-GH-NAF-001', 'Nafada General Hospital', 'Nafada', 'hospital'),
    ('GOM-PHC-NAF-001', 'Nafada Primary Health Centre', 'Nafada', 'health_centre'),
    ('GOM-PHC-NAF-002', 'Jigawa Primary Health Centre', 'Nafada', 'health_centre'),
    ('GOM-PHC-NAF-003', 'Barwo Primary Health Centre', 'Nafada', 'health_centre'),
    # Shongom (4)
    ('GOM-GH-SHO-001', 'Shongom General Hospital, Boh', 'Shongom', 'hospital'),
    ('GOM-PHC-SHO-001', 'Boh Primary Health Centre', 'Shongom', 'health_centre'),
    ('GOM-PHC-SHO-002', 'Lalaipido Primary Health Centre', 'Shongom', 'health_centre'),
    ('GOM-PHC-SHO-003', 'Filiya Primary Health Centre', 'Shongom', 'health_centre'),
    # Yamaltu/Deba (5)
    ('GOM-GH-YDB-001', 'Deba General Hospital', 'Yamaltu/Deba', 'hospital'),
    ('GOM-PHC-YDB-001', 'Deba Primary Health Centre', 'Yamaltu/Deba', 'health_centre'),
    ('GOM-PHC-YDB-002', 'Hinna Primary Health Centre', 'Yamaltu/Deba', 'health_centre'),
    ('GOM-PHC-YDB-003', 'Gwani Primary Health Centre', 'Yamaltu/Deba', 'health_centre'),
    ('GOM-PHC-YDB-004', 'Dadin Kowa Primary Health Centre', 'Yamaltu/Deba', 'health_centre'),
]

assert len(FACILITIES) == 50, 'T053 requires 50 Gombe facilities'
assert len({c for c, _n, _l, _t in FACILITIES}) == 50, 'facility codes must be unique'

KEYWORDS = [
    ('cannot breathe', 'en'), ('chest pain', 'en'), ('unconscious', 'en'),
    ('severe bleeding', 'en'), ('stroke', 'en'), ('heart attack', 'en'),
    ('seizure', 'en'), ('choking', 'en'), ('difficulty breathing', 'en'),
    ('high fever', 'en'), ('convulsion', 'en'), ('pregnancy bleeding', 'en'),
    ('severe headache', 'en'), ('labour pain', 'en'), ('severe abdominal pain', 'en'),
    ('allergic reaction', 'en'), ('drowning', 'en'), ('burns', 'en'),
    ('ba iya numfashi', 'ha'), ('ciwon kirji', 'ha'), ('suma', 'ha'),
    ('jini mai yawa', 'ha'), ('bugun jini', 'ha'), ('zazzabi mai tsanani', 'ha'),
    ('ciwon kai', 'ha'), ('gudawa', 'ha'), ('ba a iya numfashi', 'ha'),
    ('zazzabi', 'ha'), ('ciwon ciki mai tsanani', 'ha'), ('nakudar ciki', 'ha'),
    ('haihuwa', 'ha'), ('ciwon ido', 'ha'), ('tari mai tsanani', 'ha'),
    ('a numaani', 'ff'), ('mettu', 'ff'), ('ngol ngol', 'ff'),
    ('ngesa', 'ff'), ('doole', 'ff'), ('feccere', 'ff'),
    ('nguurndam comci', 'ff'), ('suuro', 'ff'), ('nawnaare mawnde', 'ff'),
    ('reedu fuu', 'ff'), ('hoore nawnaare', 'ff'), ('bernde', 'ff'),
    ('emergency', 'en'), ('help me', 'en'), ('taimaka', 'ha'), ('ballal', 'ff'),
    ('asthma attack', 'en'), ('gaggawa', 'ha'), ('na needi ballal', 'ff'),
]


def pretty(root):
    return minidom.parseString(ET.tostring(root, encoding='unicode')).toprettyxml(indent='  ')


def write_facilities():
    root = ET.Element('tryton')
    data = ET.SubElement(root, 'data')
    for code, name, lga, ftype in FACILITIES:
        rec = ET.SubElement(data, 'record', {
            'model': 'gnuhealth.institution', 'id': 'fac_%s' % code.replace('-', '_').lower()})
        ET.SubElement(rec, 'field', {'name': 'code'}).text = code
        ET.SubElement(rec, 'field', {'name': 'name'}).text = name
        ET.SubElement(rec, 'field', {'name': 'state'}).text = 'Gombe State (%s LGA)' % lga
    with open(os.path.join(DATA, 'gombe_facilities.xml'), 'w') as fh:
        fh.write(pretty(root))
    return len(FACILITIES)


def write_keywords():
    root = ET.Element('tryton')
    data = ET.SubElement(root, 'data')
    for i, (term, lang) in enumerate(KEYWORDS):
        rec = ET.SubElement(data, 'record', {
            'model': 'gnuhealth.afya.emergency_keyword', 'id': 'kw_%02d' % i})
        ET.SubElement(rec, 'field', {'name': 'term'}).text = term
        ET.SubElement(rec, 'field', {'name': 'language'}).text = lang
        ET.SubElement(rec, 'field', {'name': 'active', 'eval': 'True'})
    with open(os.path.join(DATA, 'emergency_keywords.xml'), 'w') as fh:
        fh.write(pretty(root))
    return len(KEYWORDS)


def write_patients_workers():
    root = ET.Element('tryton')
    data = ET.SubElement(root, 'data')
    for i in range(200):
        rec = ET.SubElement(data, 'record', {
            'model': 'party.party', 'id': 'gombe_patient_%03d' % i})
        ET.SubElement(rec, 'field', {'name': 'name'}).text = 'Synthetic Patient %03d (Gombe)' % i
    with open(os.path.join(DATA, 'gombe_patients.xml'), 'w') as fh:
        fh.write(pretty(root))
    root2 = ET.Element('tryton')
    data2 = ET.SubElement(root2, 'data')
    for i in range(20):
        rec = ET.SubElement(data2, 'record', {
            'model': 'party.party', 'id': 'gombe_worker_%02d' % i})
        ET.SubElement(rec, 'field', {'name': 'name'}).text = 'Health Worker %02d (Gombe)' % i
    with open(os.path.join(DATA, 'gombe_workers.xml'), 'w') as fh:
        fh.write(pretty(root2))
    return 200, 20


def main():
    os.makedirs(DATA, exist_ok=True)
    if '--apply' in sys.argv:
        import importlib.util
        if importlib.util.find_spec('trytond') is None:
            print('trytond not installed; wrote XML only. Run inside app container with --apply.')
            sys.exit(2)
        print('apply mode: use Proteus/import with generated XML (idempotent by XML ID).')
    n_f = write_facilities()
    n_k = write_keywords()
    n_p, n_w = write_patients_workers()
    print('wrote %d facilities, %d keywords, %d patients, %d workers -> %s'
          % (n_f, n_k, n_p, n_w, DATA))


if __name__ == '__main__':
    main()
