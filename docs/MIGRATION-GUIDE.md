# Migration Guide (legacy → unified)

## 1. Namespace rename

```sql
-- repeat per table; example: config
ALTER TABLE z_health_afya_config RENAME TO gnuhealth_afya_config;
UPDATE ir_model SET model='gnuhealth.afya.config'
 WHERE model='z_health_afya.config';
-- update ir_model_field.model + ir_ui_view / ir_action ids,
-- wizard ids z_health_afya_* → gnuhealth_afya_*
```

Tryton module names: uninstall `z_health_afya_*`, install `gnuhealth_afya_*`
in dependency order: core → access → triage → dispatch → diaspora → analytics.

## 2. Config ModelSQL → ModelSingleton (T005–T007)

- Delete duplicate rows, keep one; set id=1.
- Drop `name` column; add `region_coarsening_cascade JSON` default cascade.
- Replace `data/afya_config.xml` seed with singleton record (id=1).

## 3. Consent → party.party linkage (T008–T010)

- Add `party` FK; backfill from patient where possible, else NULL + open
  `posthoc_consent_task`.
- Replace free-text notes with `notes_category` enum.

## 4. Verification

```bash
python3 -c "import xml.dom.minidom,glob; [xml.dom.minidom.parse(f) for f in glob.glob('gnuhealth/**/*.xml',recursive=True)]"
python3 -m pytest tests/unit -q
```
