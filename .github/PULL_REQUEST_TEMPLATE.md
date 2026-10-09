## Summary

> What phase / tasks does this change cover? (e.g. Phase 1 T025–T030)

## Spec alignment

- [ ] Constitution reviewed
- [ ] Module spec section referenced (link)
- [ ] Namespace `gnuhealth.afya.*` respected

## Safety & privacy

- [ ] Protected fields guarded, wizard-only mutations
- [ ] No PII / free text in analytics payloads
- [ ] Phone redaction + TTL purge considered

## Verification

- [ ] `python3 -m pytest tests/unit -q` passes
- [ ] `docker compose -f docker/docker-compose.yml config` passes
- [ ] Manual UI check (screenshot if branding touched)

## Gates

- [ ] G0 / G1 / G2 checkpoint items (delete as applicable)
