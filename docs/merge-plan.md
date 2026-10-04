# AfyaConnect × GNU Health Unification Merge Plan

**Repository:** `sat-found/afyaconnect-unified`  
**Date:** September 2026  
**Status:** DRAFT - Ready for Review  
**Source Repositories:**
- `sat-found/GNU_correct` (infrastructure foundation)
- `sat-found/afyaconnect` (product prototype)

---

## Executive Summary

This document outlines the strategic consolidation of two related but divergent repositories into a single unified codebase: **afyaconnect-unified**.

**Key Decision:**
- **DO NOT** merge repositories wholesale.
- **DO** treat GNU_correct as the upstream GNU Health foundation.
- **DO** port afyaconnect's application layer (modules, branding, seed data, specs) into the unified repo.
- **DO** align conflicting data models, namespaces, and architectural decisions before code integration.

**Expected Outcome:**
- Single source of truth combining GNU Health infrastructure rigor + AfyaConnect product features.
- Clear separation between upstream GNU Health (vendored or pinned) and custom Afya modules.
- Validated module compatibility, namespace consistency, and deployment readiness.

---

## 1. Repository Structure

```
afyaconnect-unified/
│
├── README.md                           # Project overview, quick start
├── LICENSE                             # GPL-3.0 (Tryton) + Apache 2.0 (Cloud Run)
│
├── .github/
│   ├── workflows/                      # Ported from GNU_correct
│   │   ├── lint.yaml
│   │   ├── security.yaml
│   │   ├── tests.yaml
│   │   └── po-export.yaml
│   └── PULL_REQUEST_TEMPLATE.md        # OpenSpec-aligned PR template
│
├── docs/
│   ├── merge-plan.md                   # This file
│   ├── ARCHITECTURE.md                 # Hybrid architecture overview
│   ├── NAMESPACE-ALIGNMENT.md          # Model naming decisions
│   ├── MIGRATION-GUIDE.md              # Data model reconciliation
│   ├── MODULE-INVENTORY.md             # Complete module + field reference
│   └── DEPLOYMENT.md                   # Local Docker + GCP Cloud Run setup
│
├── specs/
│   ├── constitution.md                 # Ported from afyaconnect
│   ├── gnuhealth-model-inventory.md    # Ported from afyaconnect (Phase 0 deliverable)
│   ├── afya-design-spec.md             # Consolidated spec-driven development reference
│   │
│   ├── z_health_afya_core/
│   │   ├── requirements.md
│   │   └── spec.md
│   ├── z_health_afya_access/
│   │   ├── requirements.md
│   │   └── spec.md
│   ├── z_health_afya_triage/
│   │   ├── requirements.md
│   │   └── spec.md
│   ├── z_health_afya_dispatch/
│   │   ├── requirements.md
│   │   └── spec.md
│   ├── z_health_afya_diaspora/
│   │   ├── requirements.md
│   │   └── spec.md
│   ├── z_health_afya_analytics/
│   │   ├── requirements.md
│   │   └── spec.md
│   └── openspec/                       # Ported from GNU_correct
│       ├── README.md
│       ├── specs/
│       └── changes/
│
├── gnuhealth/                          # GNU Health base (vendored or submodule)
│   ├── tryton/                         # All 54+ upstream modules (or linked via submodule)
│   │   ├── health/
│   │   ├── health_ems/
│   │   ├── health_lab/
│   │   └── ... [54 core modules]
│   │
│   └── z_health_afya_*/                # AfyaConnect custom modules (ported from afyaconnect)
│       ├── z_health_afya_core/
│       ├── z_health_afya_access/
│       ├── z_health_afya_triage/
│       ├── z_health_afya_dispatch/
│       ├── z_health_afya_diaspora/
│       ├── z_health_afya_analytics/
│       └── mosquito_registration/
│
├── sao-branding/                       # Ported from afyaconnect
│   ├── css/
│   │   ├── afyaconnect.css
│   │   └── dark-mode.css
│   ├── js/
│   │   └── afyaconnect-theme.js
│   ├── assets/
│   │   ├── logo-afya.svg
│   │   └── favicon.ico
│   └── README.md
│
├── docker/                             # Docker & Compose (production-grade from afyaconnect)
│   ├── Dockerfile.gnuhealth
│   ├── Dockerfile.nginx
│   ├── docker-compose.yml              # 3-tier: Nginx + uWSGI + PostgreSQL
│   ├── nginx/
│   │   └── reverse_proxy.conf
│   ├── gnuhealth/
│   │   ├── trytond.conf
│   │   ├── init_and_run.sh
│   │   └── uwsgi.ini
│   └── README.md
│
├── scripts/
│   ├── lint.sh                         # Ported from GNU_correct
│   ├── security.sh
│   ├── autopep8.sh
│   ├── test_modules.sh
│   │
│   ├── seed-gombe.sh                   # Ported from afyaconnect
│   ├── seed-gombe.py
│   │
│   ├── setup/                          # GCP bootstrap (from spec v5.0)
│   │   ├── 01-gcp-project.sh
│   │   ├── 02-service-accounts.sh
│   │   ├── 03-secrets.sh
│   │   ├── 04-cloud-sql.sh
│   │   ├── 05-gnu-health.sh
│   │   ├── 06-bigquery.sh
│   │   ├── 07-pubsub.sh
│   │   ├── 08-cloud-scheduler.sh
│   │   ├── 09-deploy-services.sh
│   │   ├── 10-seed-data.sh
│   │   └── README.md
│   │
│   └── operational/
│       ├── start.sh
│       ├── stop.sh
│       ├── status.sh
│       └── logs.sh
│
├── services/                           # GCP Cloud Run (from spec; scaffold or planned)
│   ├── access-gateway/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── ai-triage-agent/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── fhir-adapter/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── analytics-exporter/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── diaspora-matching/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── README.md
│
├── tests/
│   ├── acceptance/
│   │   ├── AT-NAV-01-triage-scenarios.md
│   │   ├── AT-SAFE-01-human-gates.md
│   │   ├── AT-DISP-01-dispatch-timing.md
│   │   ├── AT-PRIV-01-privacy-controls.md
│   │   ├── AT-DASH-01-dashboard-freshness.md
│   │   ├── AT-LANG-01-multilingual.md
│   │   ├── AT-FHIR-01-read-latency.md
│   │   └── AT-ACC-01-access-interactions.md
│   │
│   ├── unit/
│   │   ├── test_afya_core.py
│   │   ├── test_afya_triage.py
│   │   ├── test_afya_dispatch.py
│   │   ├── test_privacy_utils.py
│   │   ├── test_consent_model.py
│   │   └── conftest.py
│   │
│   └── integration/
│       ├── test_gateway_to_triage.py
│       ├── test_triage_to_dispatch.py
│       ├── test_analytics_pipeline.py
│       └── conftest.py
│
├── data/
│   ├── afya_config.xml                 # Seed records for Afya config
│   ├── afya_triage_cron.xml            # Scheduled purge definitions
│   ├── gombe_facilities.xml            # Gombe State seed data (50 facilities)
│   ├── gombe_patients.xml              # 200 synthetic patients
│   ├── gombe_workers.xml               # 20 health workers
│   ├── emergency_keywords.xml          # ~52 multilingual emergency keywords
│   └── README.md
│
├── dashboards/                         # Looker / Looker Studio configs
│   ├── surveillance-dashboard.json
│   ├── emergency-analytics-dashboard.json
│   └── README.md
│
├── .gitignore
├── .reuse/                             # REUSE compliance (from GNU_correct)
│   └── dep5
│
├── CONTRIBUTING.md                     # Development workflow + OpenSpec process
├── CODE_OF_CONDUCT.md
│
└── docker-compose.yml                  # Root-level compose (points to docker/)
```

---

## 2. Phase 0: Alignment & Reconciliation (Week 1)

### 2.1 Model Namespace Decision

**Decision: Adopt `gnuhealth.afya.*` namespace**

**Rationale:**
- Provides intuitive Tryton menu placement (GNU Health → AfyaConnect)
- Standard pattern: `gnuhealth.` prefix for GNU Health domain modules
- Easier third-party discovery than `z_health_afya.*`
- Consistent with afyaconnect's current implementation

**Action Items:**

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T001** Rename all model classes and database tables from `z_health_afya.*` to `gnuhealth.afya.*` | Architecture Lead | All `__name__` attributes updated. All XML IDs updated. Schema migration script drafted. | — |
| **T002** Update all foreign key references and M2O/O2M fields | Dev Team | All relationship references resolve. No broken links in views. | T001 |
| **T003** Reconcile module `__init__.py` imports | Dev Team | Modules import from correct namespaces. No circular deps. | T001 |
| **T004** Produce `docs/NAMESPACE-ALIGNMENT.md` | Architecture Lead | Document filed. Reviewed by team. | T001–T003 |

---

### 2.2 Configuration Model Alignment

**Decision: Adopt ModelSingleton from GNU_correct**

**Current State:**
- GNU_correct: `z_health_afya.config` uses `ModelSingleton` (correct pattern)
- afyaconnect: `gnuhealth.afya.config` uses plain `ModelSQL` with seed record

**Action Items:**

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T005** Refactor `gnuhealth.afya.config` to use `ModelSingleton` | Dev Team | Class inherits from `ModelSingleton`. Remove redundant `name` field. XML seed updated. | T001 |
| **T006** Add configuration fields from afyaconnect spec | Dev Team | All fields present: `k_anonymity_threshold`, `symptoms_raw_ttl_days`, `region_coarsening_cascade`. | T005 |
| **T007** Write schema migration (old → new) | Database Admin | Migration script drafted. Tested on sample data. | T005 |

---

### 2.3 Consent Model Reconciliation

**Decision: Adopt `party.party` linkage (afyaconnect pattern); adopt field structure from afyaconnect**

**Rationale:**
- Emergency triage: victims may be unconscious or unregistered.
- Guardians, proxies, and bystanders are parties, not patients.
- Medically and legally superior for unidentified patients.

**Action Items:**

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T008** Finalize `gnuhealth.afya.consent_record` model from afyaconnect spec | Dev Team | Model includes: `consent_status`, `consent_actor`, `consent_scope`, `notes_category` (no free text). XML views complete. | T001 |
| **T009** Implement `PostHocConsentTask` model (afyaconnect) | Dev Team | Model creates, resolves. Linked to triage sessions. Audit trail present. | T001 |
| **T010** Write schema migration (GNU_correct `z_health_afya.consent` → unified) | Database Admin | Migration tested. Consent records transferred or re-created. | T008, T009 |
| **T011** Document consent decision in `docs/NAMESPACE-ALIGNMENT.md` | Architecture Lead | Rationale recorded. Clinical/legal justification noted. | T008–T010 |

---

### 2.4 Security PoC (Tryton + GNU Health 5.0.x)

**Action Items:**

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T012** Create test module: `test_security_poc` | Dev Team | Module scaffolded. No business logic; only pattern validation. | — |
| **T013** Implement one protected field (`clinical_rationale` on test model) | Dev Team | Field is read-only for non-admin. Override on `write()` enforces guard. Test passes. | T012 |
| **T014** Build one wizard with `@ModelView.button` | Dev Team | Wizard creates/updates protected field. Button restricted to group. Test passes. | T012 |
| **T015** Build one workflow transition with `@Workflow.transition` | Dev Team | Transition decorator works. State guards applied. Test passes. | T012 |
| **T016** Build one group-restricted button in XML | Dev Team | Button element includes `groups=` attribute. Visibility enforced. Test passes. | T012 |
| **T017** Confirm all 4 mechanisms work together | QA | Full integration test passes. Pattern validated for reuse. | T013–T016 |

**Gate G0 Checkpoint:**
- [ ] Namespace alignment complete (T001–T004)
- [ ] Config model refactored (T005–T007)
- [ ] Consent model finalized (T008–T011)
- [ ] Security PoC validated (T012–T017)
- [ ] Model inventory reconciled and committed

---

## 3. Phase 1: Module Porting (Weeks 2–3)

**Ports all 6 custom modules from afyaconnect into unified repo using aligned namespace.**

### 3.1 Core Module

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T018** Port `gnuhealth.afya.core` from afyaconnect | Dev Team | Module installed. Config singleton works. No import errors. | T001, T005 |
| **T019** Implement utilities: `redact_phone_numbers()`, `coarsen_region()`, `anonymize_payload()` | Dev Team | All functions present. Unit tests pass. | T018 |
| **T020** Add phone-number redaction before `symptoms_raw` storage | Dev Team | Nigerian patterns redacted. Test with Hausa/Fulfulde phonetics. | T019 |
| **T021** Implement `ir.cron` purge for `symptoms_raw` (30-day TTL) | Dev Team | Cron registered. Runs daily. Expired records cleared. Audit log recorded. | T018 |

### 3.2 Access Module

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T022** Port `gnuhealth.afya.access` from afyaconnect | Dev Team | `AccessSession` model created. Views present. | T001 |
| **T023** Integrate with USSD/SMS/Voice webhooks (from spec) | Dev Team | Gateway writes sessions. Session records complete. | T022 |
| **T024** Implement language detection + Fulfulde fallback | Dev Team | Gemini language detection works. Fallback triggers <70% confidence. Tests pass. | T022 |

### 3.3 Triage Module

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T025** Port `gnuhealth.afya.triage` from afyaconnect (Phase 1 implementation) | Dev Team | All models: `TriageSession`, `TriageProtocol`, `TriageSymptom`, `TriageFacilityRoute`, `EmergencyKeyword`. Views complete. | T001, T017 |
| **T026** Implement triage state machine (draft→completed→reviewed→escalated) | Dev Team | Transitions guarded. Workflow decorator applied. Tests pass. | T025 |
| **T027** Implement `ReviewTriage` wizard with guards (protected fields, button restrictions) | Dev Team | Wizard enforces field immutability. Only reviewers can access. AT-SAFE-01 partial passes. | T025, T017 |
| **T028** Implement clinical rationale JSON validation (§5.1 of spec) | Dev Team | Rationale schema enforced. Invalid records rejected on create/write. Tests pass. | T025 |
| **T029** Integrate emergency keyword detection | Dev Team | ~52 multilingual keywords seeded. Detection fires on intake. Tests pass. | T025 |
| **T030** Implement `CreateEvaluationFromTriage` wizard | Dev Team | Wizard creates `gnuhealth.patient.evaluation` from triage. ICD-10 codes linked. Tests pass. | T025 |

### 3.4 Dispatch Module

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T031** Port `gnuhealth.afya.dispatch` from afyaconnect (scaffold → PoC) | Dev Team | Extends `gnuhealth.support_request`. All models present. Views visible. | T001, T017 |
| **T032** Implement dispatch state machine (10 states: candidate→approved→submitted→en_route→arrived→completed) | Dev Team | States defined. Transitions guarded. Workflow decorators applied. | T031 |
| **T033** Implement `CreateDispatchCandidate` wizard (stops at candidate) | Dev Team | Wizard creates candidate. Does NOT auto-approve. Human gate required. Tests pass. | T031, T027 |
| **T034** Implement `ApproveDispatch` wizard with human gate | Dev Team | Only dispatcher role can approve. Protected fields immutable. Timer measured. AT-SAFE-01 dispatch portion passes. | T031, T017 |
| **T035** Seed 10 kit templates (by event type) | Dev Team | Templates visible in UI. Recommendations generated from triage. Tests pass. | T031 |
| **T036** Implement NAERS stub (accept, return mock response) | Dev Team | Stub API callable. Returns mock ambulance assignment. Tests pass. | T031 |

### 3.5 Diaspora Module

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T037** Port `gnuhealth.afya.diaspora` from afyaconnect (scaffold) | Dev Team | All models: `DiasporaSpecialist`, `CaseBrief`, `ConsultationSession`, `SpecialistMatch`. Views present. | T001, T017 |
| **T038** Seed 5 diaspora specialist profiles | Dev Team | Profiles visible. Mock matching works. Tests pass. | T037 |
| **T039** Implement `MatchSpecialist` + `GenerateCaseBrief` wizards | Dev Team | Wizards create consultation sessions. Mock audio/chat scaffold present. | T037 |

### 3.6 Analytics Module

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T040** Port `gnuhealth.afya.analytics` from afyaconnect (scaffold) | Dev Team | `AnalyticsOutbox`, `ResourceSnapshot` models present. Views created. | T001, T017 |
| **T041** Implement `create_from_triage` + `create_from_dispatch` with k-anonymity cascade | Dev Team | Outbox events created. k-anonymity threshold applied. Suppression logic works. Tests pass. | T040, T019 |
| **T042** Implement analytics schema validation (reject free text, hashes, PII) | Dev Team | Validator rejects malformed payloads. Exporter quality gates enforced. Tests pass. | T040 |

### 3.7 Security Groups & Method-Level Enforcement

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T043** Define 5 security groups (clinical_reviewer, dispatcher, diaspora_coordinator, dashboard_viewer, admin) | Architecture Lead | Groups created. Permission matrix documented in `docs/SECURITY.md`. | T017 |
| **T044** Apply method-level guards to all protected fields across all modules (using proven pattern from T017) | Dev Team | Protected fields on all models guarded. Wizard-only actions enforced. Tests pass. | T043, T017 |
| **T045** Apply group restrictions to all buttons, menus, and transitions | Dev Team | RBAC enforcement verified in UI. Tests pass. | T043, T044 |

### 3.8 Module Testing & Integration

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T046** Write comprehensive unit tests for all 6 modules | QA | Test coverage >80%. All tests pass in CI. | T018–T042 |
| **T047** Wire all modules for end-to-end integration testing | QA | Modules instantiate together. No conflicts. Dependencies resolve. | T018–T042 |
| **T048** Validate XML: all spec, view, action, and report definitions | QA | All 32+ XML files parse correctly. No undefined references. | T018–T042 |

**Gate G1 Checkpoint (Core Demo Path):**
- [ ] All 6 modules ported and integrated (T018–T045)
- [ ] Security PoC pattern applied across modules (T044–T045)
- [ ] Unit tests pass (T046)
- [ ] Core acceptance tests pass: AT-NAV-01 (partial), AT-SAFE-01, AT-DISP-01 (window B), AT-PRIV-01, AT-DASH-01 (stubbed)
- [ ] End-to-end demo path works: USSD → Triage → Review Wizard → Dispatch Wizard → Analytics Outbox

---

## 4. Phase 2: Branding & Demo Data (Week 3–4)

### 4.1 SAO Branding

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T049** Port sao-branding assets from afyaconnect | Frontend Lead | CSS, JS, SVG, favicon present. No build errors. | — |
| **T050** Integrate branding into Docker build | DevOps | Dockerfile copies branding. Nginx serves static assets. | T049 |
| **T051** Test branding in local Docker stack | QA | UI renders with teal palette, custom logo, branded login. | T050 |

### 4.2 Gombe Seed Data

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T052** Port `seed-gombe.py` + `seed-gombe.sh` from afyaconnect | Dev Team | Script present. Documented. Reproducible. | — |
| **T053** Seed 50 facilities, 200 patients, 20 health workers in unified DB | QA | All records created. No duplicates on re-run. | T052 |
| **T054** Seed ~52 multilingual emergency keywords (Hausa, Fulfulde, English) | QA | Keywords visible in triage workflow. Detection tested. | T052 |

---

## 5. Phase 3: Docker & Deployment (Week 4)

### 5.1 Docker Consolidation

**Decision: Use production-grade 3-tier stack from afyaconnect**

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T055** Consolidate Dockerfile + docker-compose.yml from afyaconnect | DevOps | 3-tier stack: Nginx + uWSGI + PostgreSQL. Builds without error. | T050 |
| **T056** Pin external dependencies (SAO, gnuhealth-all-modules, PostgreSQL versions) | DevOps | All versions locked. Checksums recorded. Builds reproducible. | T055 |
| **T057** Test full Docker stack locally | QA | Services start. App accessible at port 8091. All modules installed. | T055, T056 |
| **T058** Separate dev credentials from production secrets | DevOps | Dev defaults documented. Production via Secret Manager / environment. | T057 |

### 5.2 GCP Bootstrap Scripts

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T059** Port GCP setup scripts from spec (01-10) into `scripts/setup/` | DevOps | All scripts present. Documented. Tested on clean GCP project. | — |
| **T060** Bootstrap script acceptance test: fresh deployment on clean GCP project | QA | All 10 scripts run. Services reachable. Dashboard populated. Total time <2 hours. | T059 |

---

## 6. Phase 4: Testing & Validation (Weeks 5–6)

### 6.1 Acceptance Test Execution

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T061** Execute AT-NAV-01 (40 clinical scenarios) across all channels/languages | QA | ≥80% concordance. Red-flag sensitivity ≥95%. RAG top-3 relevance verified. | Phase 1, Phase 3 |
| **T062** Execute AT-SAFE-01 (human gates enforced) | QA | Dispatch requires approval. Protected fields immutable. Wizard-only actions enforced. | Phase 1 |
| **T063** Execute AT-DISP-01 (dispatch timing: all windows) | QA | Window A <60s, Window B <30s, Window D <90s (headline; human component noted). | Phase 1 |
| **T064** Execute AT-PRIV-01 (privacy controls) | QA | No PII in BigQuery. No free text. No hashes. Phone redaction active. Purge working. | Phase 1, Phase 3 |
| **T065** Execute AT-DASH-01 (dashboard freshness) | QA | <5 min refresh. Aggregation level displayed per tile. k-anonymity cascade working. | Phase 1 |
| **T066** Execute AT-LANG-01 (multilingual) | QA | All 3 languages tested. Fulfulde fallback triggers. <10% variance across languages. | Phase 1 |
| **T067** Execute AT-FHIR-01 (FHIR read latency) | QA | Patient, Condition, Location reads <5s. Synthetic patient retrieval works. | Services (Phase 5) |
| **T068** Execute AT-ACC-01 (access interactions) | QA | <4 interactions to complete USSD triage. User flow optimized. | Phase 1 |

### 6.2 Bias & Fairness Testing

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T069** Run 40 scenarios across languages (Hausa, Fulfulde, English) | QA | <10% variance in concordance/sensitivity. No language-specific bias detected. | T061 |
| **T070** Clinical validation: inter-rater agreement ≥80% | Clinical Advisor | Two independent reviewers score 40 scenarios. Cohen's kappa ≥0.80. | T061 |

### 6.3 NDPA Compliance Audit

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T071** Audit: no PII in BigQuery exports | Security Lead | Query results show zero PII. Phone redaction regex validated. Purge cron tested. | Phase 1, Phase 3 |
| **T072** Audit: consent flow compliance | Legal/Clinical | Consent status captured. No coercion. Emergency limited processing logged. | Phase 1 |
| **T073** Document NDPA compliance statement | Legal | Audit report filed. Gaps identified. Mitigation plan recorded. | T071, T072 |

**Gate G2 Checkpoint (Full Validation):**
- [ ] All 8 acceptance tests pass (T061–T068)
- [ ] Bias testing complete; <10% variance (T069)
- [ ] Clinical validation: inter-rater agreement ≥80% (T070)
- [ ] NDPA audit complete; compliance statement filed (T071–T073)
- [ ] Bootstrap scripts validated on clean GCP project (T060)

---

## 7. Phase 5: Cloud Services & Production (Weeks 7–8)

**Note:** Cloud Run services (Access Gateway, AI Triage Agent, FHIR Adapter, Analytics Exporter) are scaffolded in `services/` and documented but NOT fully implemented in MVP. This phase focuses on service readiness and local integration testing.

| Task | Owner | Acceptance Criteria | Depends |
|------|-------|-------------------|---------|
| **T074** Finalize `services/` directory with skeleton code for all 5 services | Backend Lead | All services have: `main.py`, `requirements.txt`, `Dockerfile`. Documented in `services/README.md`. | — |
| **T075** Implement local service testing framework | QA | Services can be instantiated locally via Docker. Integration tests against local Tryton. | T074 |
| **T076** Document GCP deployment for each service | DevOps | Each service has deployment guide: secrets, Cloud SQL connection, monitoring. | T074 |

---

## 8. Repository References (Archived)

Once consolidation is complete:

### 8.1 Archive GNU_correct

**Action:**
```bash
# On sat-found/GNU_correct
git archive --format tar.gz --output GNU_correct-archive-$(date +%Y%m%d).tar.gz HEAD
# Add to releases; mark repo as archived/read-only
```

**Rationale:** Preserve infrastructure foundation and OpenSpec methodology for reference.

### 8.2 Archive afyaconnect

**Action:**
```bash
# On sat-found/afyaconnect
git archive --format tar.gz --output afyaconnect-archive-$(date +%Y%m%d).tar.gz HEAD
# Add to releases; mark repo as archived/read-only
```

**Rationale:** Preserve product prototype and branding assets for reference.

### 8.3 Create Redirect References

**In both archived repos, add `CONSOLIDATED.md`:**

```markdown
# This repository has been consolidated into sat-found/afyaconnect-unified

See: https://github.com/sat-found/afyaconnect-unified

Archive date: [DATE]
Reason: Unified development platform combining infrastructure rigor + product features.
Historical reference: This repo is archived and read-only.
```

---

## 9. Timeline & Milestones

| Phase | Duration | Gates | Deliverables |
|-------|----------|-------|--------------|
| **Phase 0: Alignment** | Week 1 | G0 | Namespace finalized. Config/consent models reconciled. Security PoC validated. |
| **Phase 1: Modules** | Weeks 2–3 | G1 | 6 modules ported. Security patterns applied. Core demo path works. |
| **Phase 2: Branding** | Week 3–4 | — | SAO branding integrated. Gombe seed data loaded. |
| **Phase 3: Docker** | Week 4 | — | 3-tier stack builds. GCP bootstrap scripts ready. |
| **Phase 4: Testing** | Weeks 5–6 | G2 | All acceptance tests pass. NDPA audit complete. Clinical validation ≥80%. |
| **Phase 5: Cloud** | Weeks 7–8 | — | Cloud Run services scaffolded. Deployment guides complete. |

**Total Duration:** 8 weeks to MVP deployment readiness.

---

## 10. Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Module namespace misalignment blocks integration | M | H | T001–T004 gate G0. Comprehensive testing before proceeding. |
| Config/consent model conflicts | M | H | T005–T011 gate G0. Schema migration tested on sample data. |
| Security pattern fails in Tryton 7.0 | L | H | T012–T017 PoC before applying to all modules. Early validation. |
| Acceptance tests reveal unmet clinical requirements | M | M | T061–T070 parallel. Clinical advisor involved from Week 5. |
| NDPA audit finds PII leakage | L | H | T071–T073. Phone redaction, purge cron, and consent flow extensively tested. |
| GCP bootstrap scripts fail on fresh project | M | M | T060 repeated on clean GCP project. Full documentation. |
| Schedule overrun (12 weeks → 16 weeks) | M | M | Buffer in Phase 5. Cloud services demotable to scaffolds if needed. |

---

## 11. Success Criteria

### MVP Acceptance (Gate G2):

- ✅ **Architecture:** Single unified repository with clear namespace, namespace alignment, and no divergent data models.
- ✅ **Modules:** All 6 AfyaConnect modules ported, integrated, and tested.
- ✅ **Security:** Method-level guards, RBAC, protected fields, and wizard enforcement validated.
- ✅ **Demo Path:** USSD/SMS → Triage → Review → Dispatch → BigQuery works end-to-end.
- ✅ **Testing:** All 8 acceptance tests pass. Clinical validation ≥80%. Bias <10%.
- ✅ **Privacy:** NDPA compliance audit complete. No PII in exports. Purge working.
- ✅ **Deployment:** Local Docker stack builds. GCP bootstrap scripts validated on clean project.
- ✅ **Documentation:** All specs, architectural decisions, and deployment guides complete.

---

## 12. Next Steps

1. **Review & Approve Merge Plan** (this document)
2. **Create Phase 0 branch** (`feature/phase-0-alignment`) and assign T001–T017
3. **Establish governance** (gate sign-offs, code review process)
4. **Activate GitHub Actions CI/CD** (lint, security, tests)
5. **Kickoff Phase 0 work** (Week 1)

---

## Appendix A: Git Integration Strategy

### A.1 Importing GNU_correct Source

**Option 1: Subtree (Recommended)**
```bash
cd afyaconnect-unified
git remote add gnu-correct https://github.com/sat-found/GNU_correct.git
git subtree add --prefix gnuhealth-base gnu-correct feature/containerization --squash
```

**Option 2: Submodule**
```bash
git submodule add https://github.com/sat-found/GNU_correct.git gnuhealth-base
git submodule update --init --recursive
```

### A.2 Importing afyaconnect Modules

**Copy & Clean:**
```bash
# Clone afyaconnect
git clone https://github.com/sat-found/afyaconnect.git temp-afya
cd afyaconnect-unified

# Copy custom modules (filtering out upstream GNU Health)
cp -r temp-afya/gnuhealth/z_health_afya_* gnuhealth/
cp -r temp-afya/sao-branding/ .
cp temp-afya/scripts/seed-gombe.* scripts/
cp temp-afya/data/* data/
cp temp-afya/specs/* specs/

# Commit as port-afyaconnect
git add .
git commit -m "Port AfyaConnect modules, branding, and seed data from afyaconnect repo"

# Cleanup
rm -rf temp-afya
```

---

## Appendix B: Data Migration Scripts

### B.1 Namespace Migration Template

```sql
-- Migrate z_health_afya_config → gnuhealth_afya_config
ALTER TABLE z_health_afya_config RENAME TO gnuhealth_afya_config;

-- Update ir_model references
UPDATE ir_model SET model = 'gnuhealth.afya.config' 
  WHERE model = 'z_health_afya.config';

-- Update ir_model_field references
UPDATE ir_model_field SET model = 
  (SELECT id FROM ir_model WHERE model = 'gnuhealth.afya.config')
  WHERE model IN (SELECT id FROM ir_model WHERE model = 'z_health_afya.config');

-- Repeat for all models
```

---

End of Merge Plan. **Status: READY FOR REVIEW**

