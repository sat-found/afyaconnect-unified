# SAO Branding — AfyaConnect premium theme

Teal trust palette (`#0d9488`), Inter type, card surfaces, gradient navbar,
branded login hero (EN/HA/FF switcher), triage-level pills (green/yellow/red/
pulsing emergency), dark mode (toggle + OS preference), focus-visible rings,
responsive + reduced-motion support.

## Files

- `css/afyaconnect.css` — design system (load with `theme="afyaconnect"`).
- `css/dark-mode.css` — dark overrides via `[data-afya-dark="1"]`.
- `js/afyaconnect-theme.js` — title, logo, login hero, dark toggle, pill painter.
- `assets/logo-afya.svg`, `assets/favicon.svg`.

## Install

```bash
bash sao-branding/apply-branding.sh /path/to/sao
# Docker: see docker/Dockerfile.nginx (copies sao-branding into the image)
```
