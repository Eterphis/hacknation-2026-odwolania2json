---
id: T011
title: Restyle the web prototype in the Cold Trace visual identity (Eterphis)
status: todo
owner: null
branch: null
depends_on: [T007]
capabilities: [frontend]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -c \"import sys; from fastapi.testclient import TestClient; from web.app import app; c=TestClient(app); fs=[('files',(n,open('C:/Users/jasiu/workspace/uzp-data/dane/przyklad_07/'+n,'rb'),'application/pdf')) for n in ('odwolanie.pdf','pelnomocnictwo.pdf','potwierdzenie_przelewu.pdf')]; r=c.post('/api/process',files=fs); j=r.json(); names=sorted(d['output_name'] or '' for d in j['documents']); h=c.get('/'); css=c.get('/static/coldtrace/bundle.css'); js=c.get('/static/coldtrace/bundle.js'); ok=r.status_code==200 and names==['odwolanie.json','pelnomocnictwo.json','potwierdzenie_przelewu.json'] and h.status_code==200 and 'class=\\\"ct' in h.text and css.status_code==200 and js.status_code==200 and '/_blob/' not in css.text; print(r.status_code,names,css.status_code,js.status_code,ok); sys.exit(0 if ok else 1)\""
    timeout: 900
  - id: AC-3
    run: "! grep -rnE '#[0-9A-Fa-f]{6}\\b|#[0-9A-Fa-f]{3}\\b|border-radius: *[1-9]|box-shadow|backdrop-filter|filter: *blur' web --include=*.css --include=*.html --include=*.js --exclude-dir=coldtrace"
    timeout: 60
  - id: AC-4
    manual: "Judge opens `python -m web` in a browser: night is the default and the Daylight switch works; both modes pass the Cold Trace review checklist (design/cold-trace/README.md section 12): role tokens only, chamfers not rounding, colour only in lines/vias/traces, one prime key per view, Anybody wide + Martian Mono, sentence case, no shadows/glows/emoji, works at 375px with 44px touch targets; Eterphis lockup in the top bar; uploading przyklad_07 and the template case shows classes, rejected TED, JSON and the evidence table in the new look."
protected: []
---
## Objective
The web prototype from T007 (`web/`) wears the owner's visual identity, **Cold Trace** (Eterphis brand), instead of its interim styling. Same features and API, new look and copy tone: a UZP clerk uploads a case and reads classes, JSON and per-field evidence in a screen that looks like it came off the Cold Trace board. This is what the jury sees in the live demo and on screenshots, and transparency of extraction is scored, so the evidence view must stay the clearest part of the page.

## Inputs (local copies, read them first)
- `design/cold-trace/README.md` — the brand book: twelve rules, colour roles, type, shape, spacing, surface, motion, two modes, "Composing something the kit doesn't have", Never list, review checklist. It is the spec for this task.
- `design/cold-trace/tokens.json` — exact token values.
- `design/cold-trace/components/bundle.css` + `bundle.js` — the kit: load these instead of writing your own versions; `components/<Name>/README.md` + `preview.html` hold the canonical markup (Key, Frame, Field, Table, Tag, Toast, Toggle, Loaders, Navigation, Segmented, StatTile, Check, Curtain, Logo, Cover).
- `design/cold-trace/assets/` — Eterphis logos (mark-small for the 40px top-bar lockup, wordmark, favicon), grit textures, icon drawing rules (`ICONS.md`; draw any icon you need, e.g. upload/download, by those rules as inline SVG with `currentColor`).
- Source of truth if anything is unclear: the owner's design-system artifact https://claude.ai/artifact/WchMUpvmWZxesNduioFZ2o (the local copy is enough; do not edit the artifact).

## Requirements
- Vendor the kit into `web/static/coldtrace/` (bundle.css, bundle.js, grit PNGs, logo SVGs) and serve it; rewrite the two `url(/_blob/<id>)` grit references in the copied bundle.css to the local PNG paths (AC-2 checks no `/_blob/` remains). Do not otherwise edit the vendored kit; page-specific CSS goes in its own file using role tokens only (AC-3 forbids literal colours, rounded corners, shadows and blur outside `coldtrace/`).
- Fonts: the kit imports Anybody and Martian Mono from Google Fonts. The app must also work on-premise without internet: self-host the two fonts (both SIL OFL) under `web/static/coldtrace/fonts/` if you can fetch the woff2 files, otherwise keep the Google import with the kit's system fallbacks and say so in the report. List them in the report for docs/EXTERNAL_COMPONENTS.md (T008).
- Layout from the kit: top bar with the Eterphis horizontal lockup and the "Daylight" toggle (night default, before-paint theme snippet, `ColdTrace.setTheme`), `.ct-wrap` container, section heads with `.ct-ruler`; the upload drop zone as a `.ct-frame--well` with one prime key ("Przetwórz sprawę"); progress as the Loaders routed trace / sweep (OCR can take ~7 s per scanned page); per document a `.ct-frame` panel with a `.ct-tag` (via carries state: live = accepted, fault = rejected/odrzucony, arc = info) and score as a readout; tabs per the kit's composing rules (ink word + 2px signal trace); evidence in `.ct-table` inside `.ct-table-box` with tabular numbers; JSON in Martian Mono; ZIP/JSON download as ground keys; consistency checks as tags; errors as fault toasts that say how to fix.
- Copy in Polish, Cold Trace voice: sentence case, plain verbs, the result repeats the verb ("Przetwórz" → "Przetworzono"), errors say what broke and how to fix, no exclamation marks, no emoji.
- Keep the JSON API, routes and response shape unchanged (AC-2; T008 docs and later tasks rely on them). Keep or update `tests/test_web.py`.
- Works at 375px (one column, tables scroll inside the box), touch targets >= 44px, `prefers-reduced-motion` respected, visible signal focus.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read D-007 and `.house/reports/T007.md`. Python venv: C:/Users/jasiu/workspace/.venv. UZP data (read-only, never copy into the repo): C:/Users/jasiu/workspace/uzp-data.
- You own `web/` (templates, static, app wiring for static files) and `tests/test_web.py`. `design/cold-trace/` is the owner's reference copy: read-only.
- Verify visually in a browser at desktop width and 375px in both modes, with a real upload of przyklad_07 and of `uzp-data/szablon-aplikacja/input/case1` (scan + TED notice); save 2-4 screenshots under `docs/screenshots/` (they go into the README later).

## Out of scope
Engine, recipes, API changes, Docker/docs (T008).
