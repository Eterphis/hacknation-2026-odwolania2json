# Prior-art card: I-002 Sprawa jako graf (cross-document entity resolution + formal-check report)

- **Agent / model:** researcher (haiku)
- **Date:** 2026-11-21
- **Sources checked:** YC directory via `house yc` (2 phrasings), YC RFS page, Product Hunt and Devpost via web search, Splink LICENSE fetched from GitHub raw.

## Closest existing (max 5)

1. **Parsewise** (YC Spring 2025, https://www.ycombinator.com/companies/parsewise): "Multi-document processing for your risk teams, AI agents, pipelines". Closest commercial match to cross-document processing. Configuration and linking method not verified.
2. **Splink** (open source, UK Ministry of Justice, https://github.com/moj-analytical-services/splink). Probabilistic record linkage / entity resolution without shared IDs, used in government. Not a document tool, but it is exactly the entity-resolution layer I-002 would need. Used in MoJ production (per MoJ blog, search result).
3. **Hazel** (YC Winter 2024, https://www.ycombinator.com/companies/hazel-2): "AI-enabled procurement for government". Domain-adjacent (government procurement), not appeal checks.
4. **Bonfire** (YC Winter 2015, acquired, https://www.ycombinator.com/companies/bonfire): RFPs and bidding for government procurement teams. Domain-adjacent, not document linking.
5. **Tender-analysis tools on Product Hunt** (SpikeCore AI, TenderFix, Tendrio, Madarik, Nabavkidata): extract requirements or line items from tender PDFs, do compliance matrices, one does OCR-based corruption monitoring. Vendor descriptions only. None found for appeals (odwolania).

Single-document extractors (Azure Document Intelligence, Google Document AI, Extend, Reducto) do not link values across documents, as far as their public docs describe.

## What is genuinely different

Using identifiers and values from all documents of one case as a graph, resolving roles (appellant, contracting authority, proxy) by cross-document constraints, using checksums as an OCR-repair oracle, and generating a formal-check report (wpis fee, deadline, power-of-attorney coverage) for a KIO appeal. The formal-check layer is the least-covered part in the sources found.

## Market signal

Cross-document processing and government procurement are both active (Parsewise, Hazel, Bonfire, tender tools). No product found that checks KIO appeal formalities. YC RFS summary (https://www.ycombinator.com/rfs, summarising fetch): "AI for City Hall" covers government procurement, permits and public records. Lead only.

## Risk for the rubric

- **Novelty risk: medium for the linking, low-medium for the formal checks.** Entity resolution is established (Splink, record linkage literature), so a judge will not see the linking as new. The formal-check report is the defensible novelty but it depends on correct domain rules (wpis amounts, deadlines), which must be verified with UZP. Pitch the checks as a pilot step, not as the core.
- **Hackathon prior art:** no Devpost winner for appeal checks found.

**Reusable open source:** see list below (Splink MIT, verified; pdfplumber MIT; avoid PyMuPDF AGPL-3.0)

## Reusable open source

- **Splink: MIT**, verified (https://raw.githubusercontent.com/moj-analytical-services/splink/master/LICENSE, "Copyright (c) 2020 Ministry of Justice"). Permissive, suitable for transfer to UZP.
- pdfplumber: **MIT**, verified (https://raw.githubusercontent.com/jsvine/pdfplumber/stable/LICENSE.txt).
- rapidfuzz (named in the ideation report as MIT): **not verified** in this session.
- networkx (BSD-3 per ideation report): not verified here.
- **Avoid PyMuPDF (AGPL-3.0)**, verified (https://raw.githubusercontent.com/pymupdf/PyMuPDF/main/COPYING).

## Open points

- Whether Parsewise does linking across a case, or only per-batch processing: not verified (product page not fetched).
- Formal-check rules (wpis amounts, deadlines) are not verified against primary law sources in this pass; this card does not validate them.
- Splink is probabilistic and heavy for three-document cases; a rule-based linker may be enough (judgement, not sourced).
