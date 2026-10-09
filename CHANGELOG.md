# Changelog — Keep a Changelog (https://keepachangelog.com), SemVer.

## [Unreleased]
### Added
- Repo standards: Makefile, pyproject (pytest/ruff/black/coverage), pre-commit,
  editorconfig, `.env.example`, SECURITY.md, CODEOWNERS, `.dockerignore`.
- Services: shared classify in `common.py`, gateway→triage-agent forwarding with
  local fallback, CORS + X-Request-ID middleware, services compose (8081–8085),
  `docs/API.md`, gateway/middleware tests.
- Tryton: complete form/tree arch for all 7 modules, group-guarded clinical
  buttons, `test_views.py` view↔model consistency suite.
- Live acceptance suite (`tests/acceptance/test_at_live.py`, 9 checks) + `make e2e`
  demo script; verified 9/9 against booted services.
- `make smoke`: all 7 Tryton modules import clean against real trytond 7.0.58;
  namespaces, fields, tryton.cfg references asserted.
- Real idempotent GCP bootstrap commands (02–10).
- Plan features: 10 kit templates + 5 diaspora specialists module seeds (T035/T038),
  `ResolvePostHocConsent` wizard with wizard-only guard (T009), 50 Gombe facilities
  across 11 LGAs (T053), `ConsultationEvent` audio scaffold + `match_score` logic
  module (T039), `ResourceSnapshot.create_snapshot` + `analytics_logic` module (T040).
### Fixed
- `.env.example` no longer git-ignored; Dockerfile cleanup.
- analytics-exporter: strict `extra='forbid'` schema — free-text keys now 422
  instead of being silently dropped (PII-drop bug caught by live AT-PRIV-01).

## [0.5.0] — 2026-10-09
### Added
- 5 Cloud Run FastAPI services with demo UI, tests, Dockerfiles.
- 24-test pytest suite (unit + integration), 8 acceptance-test stubs, dashboards.

## [0.4.0] — 2026-10-09
### Added
- 3-tier Docker stack, GCP bootstrap scripts 01–10, Gombe seed data (52 keywords).

## [0.3.0] — 2026-10-09
### Added
- Premium SAO branding: teal theme, dark mode, login hero, triage pills, logo.

## [0.2.0] — 2026-10-09
### Added
- All 7 Tryton modules (`gnuhealth.afya.*` namespace): core/access/triage/dispatch/diaspora/analytics + mosquito.

## [0.1.0] — 2026-10-09
### Added
- Foundation docs (architecture, namespace, security, deployment), specs, CI.
