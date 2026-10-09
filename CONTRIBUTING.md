# Contributing to afyaconnect-unified

## Workflow (OpenSpec-aligned)

1. Read `specs/constitution.md` + the module spec you touch.
2. Branch: `feature/<phase>-<slug>` (e.g. `feature/phase-1-triage`).
3. Small commits; one concern per commit; `pytest tests/unit -q` must pass.
4. Open a PR using `.github/PULL_REQUEST_TEMPLATE.md`.

## Checks

```bash
bash scripts/lint.sh        # flake8 / pycodestyle + pyflakes
bash scripts/security.sh    # bandit + secret scan
bash scripts/test_modules.sh  # tryton module tests (needs server)
python3 -m pytest tests/unit -q  # fast pure-logic suite (no server)
```

## Tryton module rules

- Namespace: `gnuhealth.afya.*` for all model `__name__`.
- Config: `ModelSingleton` for `gnuhealth.afya.config`.
- Protected fields: never writable directly — guard in `write()`, mutate via wizards only.
- Buttons/menus/transitions: always `groups=` restricted.
- No free text in analytics payloads; redact phones before storing `symptoms_raw`.
