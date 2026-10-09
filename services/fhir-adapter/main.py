# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""fhir-adapter: read-only FHIR R4 (Patient/Condition/Location) over Tryton data."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import add_standard_middleware  # noqa: E402

from fastapi import FastAPI, Response  # noqa: E402

app = FastAPI(title='Afya FHIR Adapter', version='1.0.0')
add_standard_middleware(app, 'fhir-adapter')

DEMO = {
    'Patient': [{'id': 'gombe-001', 'name': 'Synthetic Patient 001 (Gombe)'}],
    'Condition': [{'id': 'cond-001', 'code': 'R06.02', 'display': 'Shortness of breath'}],
    'Location': [{'id': 'GOM-FMC-001', 'name': 'Federal Medical Centre Gombe'}],
}


@app.get('/healthz')
def healthz():
    return {'ok': True, 'service': 'fhir-adapter'}


@app.get('/')
def info():
    return {'service': 'fhir-adapter', 'docs': '/docs',
            'resources': ['Patient', 'Condition', 'Location']}


@app.get('/fhir/{resource}')
def read(resource: str, response: Response):
    t0 = time.time()
    if resource not in DEMO:
        response.status_code = 404
        return {'resourceType': 'OperationOutcome', 'issue': [{'severity': 'error'}]}
    latency = (time.time() - t0) * 1000
    response.headers['X-Read-Latency-ms'] = str(round(latency, 1))
    return {'resourceType': 'Bundle', 'type': 'searchset',
            'entry': [{'resource': {'resourceType': resource, **r}} for r in DEMO[resource]]}
