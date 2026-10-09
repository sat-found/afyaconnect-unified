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
### Fixed
- `.env.example` no longer git-ignored; Dockerfile cleanup.

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
