# Prior-art card: I-005 "Dowód na stronie" (geometry-first token boxes + evidence viewer + click-to-teach)

Date: 2026-11-21. Researcher: haiku. Status of checks: YC directory run with 3 phrasings; web checks on primary
pages where fetchable. Items marked "unverified" were not confirmed on a primary page.

## Closest existing (max 5)

1. **Docling (open source, MIT)**: IBM Research document-conversion toolkit (layout, tables, OCR); converts PDFs to a
   unified document model. Code licence MIT (https://github.com/docling-project/docling, sidebar checked). Closest
   open-source "one page model for digital and scanned PDFs" stack. Its provenance / per-element bounding-box output
   is not confirmed here (unverified in this session). Models carry their own licences (see reports/licences.md).
2. **Azure AI Document Intelligence (Microsoft, proprietary cloud)**: custom extraction with per-field confidence and
   layout; priced per 1,000 pages with a free F0 tier (search snippet of the Azure pricing page; amounts not confirmed).
   Bounding-box output and confidence were not confirmed in the pricing snippet (unverified). Closest commercial
   "evidence on the page" product for a jury that knows IDP.
3. **Rossum (commercial, proprietary SaaS)**: document processing platform described as "proprietary transactional
   LLM"; trial, demo and pricing pages, no self-hosted option mentioned. Source: https://rossum.ai (fetched). It has
   a human-in-the-loop validation UI, which is the "click to correct" part of I-005, but the config-learning step is
   the closed part.
4. **Label Studio (open source, Apache-2.0)**: human-in-the-loop annotation and labelling, including OCR/document
   labelling templates. Licence Apache-2.0 (https://github.com/HumanSignal/label-studio, sidebar checked). It
   provides correction on the page, but does not write anchor rules back into an extraction config (not checked
   in code, unverified).
5. **Commercial IDP in YC (for the judge):** Reducto (YC W2024), Extend (YC W2023), Pulse (YC S2024), Nanonets (YC W2017),
   Invofox (YC S2022), Handl (YC W2020, converts invoices and forms). Source: `house yc` output with 3 phrasings
   ("intelligent document processing invoices contracts to structured data"; "document data extraction from PDFs with
   human review"). Product Hunt: TrueTrace (visual bounding-box citations on documents; open-source status unverified).

## What is genuinely different

Geometry-first rules as the main extraction path (label left or above, directional search, stop at the next label),
with a single layout model for digital and scanned PDFs, and a click-to-teach loop where a correction on the page
writes the anchor label into the class YAML. Docling and Azure give layout and boxes; Label Studio and Rossum give
human correction; none in the list above writes the correction back as an editable open configuration for the same
pipeline. This is the part to defend.

## Market signal

Real: several funded companies sell document extraction (Reducto, Extend, Pulse, Nanonets, Invofox, Handl), and the
Azure and Rossum products show a market for "evidence on the page". No RFS entry checked (the RFS page could not be
read directly; unverified). No HackNation/UZP past winners found (search returned nothing relevant; unverified).

## Risk for the rubric

- **Novelty risk: MEDIUM-HIGH on the viewer.** A judge who knows Docling, Azure DI or Rossum will say "boxes on the
  page exist". Defence: the viewer is not the novelty; the write-back of a corrected anchor into the open YAML class
  config is, and it is shown live with the config diff (I-005 jury wow).
- **Transparency (20%/30% criteria):** the brief explicitly rewards extraction transparency, so per-field evidence is
  a scored feature (rubric level 5 needs per-field evidence in the UI).
- **Risk of over-engineering:** Docling's provenance output, if it exists in the version we use, would replace part
  of the layout module; check before building our own.
- **Licence risk:** docling-models carry CDLA-Permissive-2.0 (not OSI-approved) alongside Apache-2.0 tags; per-model
  check needed (reports/licences.md). PyMuPDF (often used for page rendering) is AGPL-3.0: use pypdfium2 instead.

## Reusable open source (with licences)

- Docling (code): MIT (https://github.com/docling-project/docling); docling-models: CDLA-Permissive-2.0 and
  Apache-2.0 tags, per-file check open (https://huggingface.co/docling-project/docling-models)
- Label Studio: Apache-2.0 (https://github.com/HumanSignal/label-studio)
- pdfplumber: MIT (https://github.com/jsvine/pdfplumber) - word boxes for the text-layer path
- pypdfium2: Apache-2.0 OR BSD-3-Clause (https://github.com/pypdfium2-team/pypdfium2) - page rendering for the viewer
- Tesseract: Apache-2.0 (https://github.com/tesseract-ocr/tesseract); tessdata (incl. pol): Apache-2.0
  (https://github.com/tesseract-ocr/tessdata)
- RapidOCR: Apache-2.0 code, OCR models derived from PaddleOCR under Apache-2.0 (https://github.com/RapidAI/RapidOCR)

## Open points

- Confirm whether Docling's version we would pin returns per-element bounding boxes with provenance (unverified here).
- Azure bounding-box/confidence details and Rossum licensing beyond the marketing pages: not verified.
- TrueTrace open-source status: unverified.
- RFS and HackNation/Devpost checks: not retrieved.
