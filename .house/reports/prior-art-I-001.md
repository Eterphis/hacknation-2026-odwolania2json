# Prior-art card: I-001 Recipes (declarative YAML extraction per document class)

- **Agent / model:** researcher (haiku)
- **Date:** 2026-11-21
- **Sources checked:** YC directory via `house yc` (3 phrasings), YC RFS page, web search (Devpost, Product Hunt, GitHub/PyPI), licence files fetched from GitHub raw and PyPI JSON.

## Closest existing (max 5)

1. **invoice2data** (open source, Python, not YC). Template-per-vendor YAML/JSON files with `keywords`, `exclude_keywords` and regexp fields; a generic engine picks the template by keyword. Sources: https://github.com/invoice-x/invoice2data (README/FAQ via search result), PyPI metadata https://pypi.org/pypi/invoice2data/json (license "MIT"). Very close mechanism; limited to invoices, no Polish legal normalisers, no per-field evidence.
2. **Azure AI Document Intelligence, custom template model** (commercial, Microsoft). Labelled template per form type. Source: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-custom (search result only, not fetched in full). Same "one config per class" idea, but proprietary and cloud-only.
3. **Google Document AI, template-based extraction** (commercial). Labelled fixed-layout template; Google states a template model can reach good quality with about 3 training and 3 test documents for fixed layouts. Source: https://docs.cloud.google.com/document-ai/docs/ce-template-based (search result snippet). Proprietary.
4. **ParseHawk** (Apache-2.0 per EU Interoperable Europe listing, https://interoperable-europe.ec.europa.eu/collection/egovernment/solution/parsehawk). Local-first PDF/scan to JSON with JSON Schema validation. Not a YAML-recipe engine as far as the listing says; GitHub repo not verified.
5. **Parsewise** (YC Spring 2025, "Multi-document processing for your risk teams, AI agents, pipelines", https://www.ycombinator.com/companies/parsewise). Commercial, multi-document; configuration model not verified.

Other YC hits (not the same mechanism, same market): Extend, Reducto, Pulse, NuMind, Invofox, Nanonets, Handl, Lawyaw. Found via `house yc` with phrasings "extract structured data from legal PDF documents into JSON using configurable templates" and "document extraction with no-code rules for new document types".

## What is genuinely different

A single open, domain-neutral engine whose only knowledge lives in YAML recipes that also carry Polish normalisers (date_pl, amount_pl, NIP/REGON/IBAN validators), a schema-shaped output and per-field evidence (rule that fired plus source snippet), applied to KIO appeal documents where the output is a fixed UZP schema. The "new class = a file, shown live" demo is the differentiator, not the template idea itself.

## Market signal

Funded document-extraction companies exist (Extend, Reducto, Nanonets, Invofox, Handl) and invoice2data shows the template pattern is established open-source practice. No public-sector appeal (odwolanie KIO) extractor was found in YC, Product Hunt or Devpost searches. Product Hunt tender tools found (SpikeCore AI, TenderFix, Nabavkidata, Tendrio, Madarik) analyse tender documents, not appeals. Vendor claims are unverified.

## Risk for the rubric

- **Novelty risk: medium-high.** A judge who knows invoice2data or Azure/Google template models will say "template extraction exists". Defend with: the legal/Polish normaliser set, validators, per-field evidence in the UI, and the live new-class demo. Do not claim the pattern is new; claim the open, auditable, UZP-schema-driven version.
- **Hackathon prior art:** no Devpost winner matching "legal PDF to JSON, open source" was found. A Devpost project "Docalyzer" (pdf-parse plus Gemini to JSON) is a weak match; winner status not confirmed. Stanford LLM x Law Hackathon #6 (2026) winners were listed (https://law.stanford.edu/2026/04/27/2026-llm-x-law-hackathon-6-winners/) but are not extraction tools as far as the snippets show.
- **RFS:** YC RFS page (https://www.ycombinator.com/rfs), read via a summarising fetch: "AI for City Hall" (government procurement, permits, public records) is the nearest entry. Lead only; not verified verbatim.

**Reusable open source:** see list below (invoice2data MIT per PyPI; pdfplumber MIT; avoid PyMuPDF AGPL-3.0)

## Reusable open source

- invoice2data: **MIT** per PyPI metadata (https://pypi.org/pypi/invoice2data/json). GitHub LICENSE file not fetched (404 on two raw paths); confirm before reuse. Reuse the pattern as reference, or the code if the licence is confirmed.
- pdfplumber: **MIT**, verified (https://raw.githubusercontent.com/jsvine/pdfplumber/stable/LICENSE.txt).
- PyYAML and pydantic: not fetched here; both MIT by common knowledge, unverified in this session.
- **Avoid PyMuPDF: AGPL-3.0**, verified (https://raw.githubusercontent.com/pymupdf/PyMuPDF/main/COPYING). Conflicts with IP transfer to UZP.

## Open points

- Confirm invoice2data's LICENSE file on GitHub before any code reuse.
- Azure, Google and Parsewise configuration details were taken from search snippets, not full docs.
- Hackathon winners list for this exact contest type was not found in this pass.
