# Prior-art card: I-003 Naucz na przykładach (rule induction from PDF + JSON pairs)

- **Agent / model:** researcher (haiku)
- **Date:** 2026-11-21
- **Sources checked:** YC directory via `house yc` (2 phrasings), YC RFS page, web search (academic wrapper induction, Google and Azure docs, Product Hunt, Devpost), LangExtract LICENSE fetched from GitHub raw.

## Closest existing (max 5)

1. **Wrapper induction, WIEN / Kushmerick et al.** (academic, IJCAI 1997, https://ijcai.org/proceedings/1997/106). Learns extraction rules (landmarks) for web pages from labelled example responses; the paper reports about 2 to 44 examples for effective learning and seconds of CPU per site. Same concept (examples in, rules out) but for HTML, 1997. Prior art a technical jury could cite. Dissertation UW-CSE-97-11-04 (https://dada.cs.washington.edu/research/tr/1997/11/UW-CSE-97-11-04.pdf) describes WIEN in detail; not read in full here.
2. **Azure AI Document Intelligence custom models** (commercial, https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-custom). Learns from labelled documents; Microsoft's guidance states at least five labelled documents per custom model (search snippets; the minimum is version-dependent, check the page for the API version used). Direct match for "5 to 10 pairs gives a model".
3. **Google Document AI custom extractor** (commercial, https://docs.cloud.google.com/document-ai/docs/custom-based-extraction). Per search snippet, a custom model needs a minimum of 10 training and 10 test documents; template mode can work with about 3 training documents for fixed layouts. Proprietary.
4. **LangExtract** (open source, Google, https://github.com/google/langextract, Apache-2.0). Few-shot examples steer an LLM to extract structured data, with each result mapped to character offsets in the source; ungrounded results get `char_interval = None`. Uses LLMs (Gemini, OpenAI, Ollama), so not offline-by-default, and not a learned rule config. Closest open-source match for "examples plus grounding".
5. **Nanonets / Rossum** (commercial, vendor claims): learned models per document type. Vendor claims only (https://nanonets.com/vs/rossum is vendor marketing); no independent detail found.

No YC company found whose core is learning extraction rules from examples (YC searches returned NuMind, Invofox, Reducto, Pulse, Extend and Nanonets as document extraction APIs, not rule induction). No Devpost winner or Product Hunt product found with this mechanism.

## What is genuinely different

Output is a human-readable, editable extraction config (same format as I-001's recipes) learned from a handful of PDF plus JSON pairs, with cross-validated F1 per field shown before use, applied to Polish legal documents with a fixed output schema. Commercial tools learn opaque models; LangExtract is LLM-prompted, not rule-learned.

## Market signal

Learning from examples is commercially established (Azure, Google, Nanonets, Rossum all sell it). The open-source, readable-config variant with per-field CV is not found in these sources. No public-sector or appeal-specific product found.

## Risk for the rubric

- **Novelty risk: high for the concept, medium for the readable-config variant.** A jury member who knows Azure custom models or WIEN will say "this exists". Defend with the open, editable YAML output, per-field CV, and the fact that it runs without an LLM. Cite WIEN and Azure openly in the pitch; this strengthens credibility.
- **Practical risk (not prior art):** the synthetic training set makes induced labels overfit the generator (ideation report). Azure's and Google's minimums (5 and 10 documents) suggest 5 to 10 pairs is at the low end of what commercial tools require, so expect weaker induction than the demo implies.

**Reusable open source:** see list below (LangExtract Apache-2.0, verified; avoid PyMuPDF AGPL-3.0)

## Reusable open source

- **LangExtract: Apache-2.0**, verified (https://raw.githubusercontent.com/google/langextract/main/LICENSE). Reusable as a reference for grounding, or directly; it needs an LLM endpoint.
- WIEN: academic method, no code licence found in this pass; re-implement from the paper rather than reuse code of unknown licence.
- python-crfsuite / sklearn-crfsuite (MIT per ideation report): **not verified** in this session.
- scikit-learn (BSD-3 per ideation report): not verified here.
- **Avoid PyMuPDF (AGPL-3.0)**, verified (https://raw.githubusercontent.com/pymupdf/PyMuPDF/main/COPYING).

## Open points

- WIEN algorithm details taken from search snippets of the 1997 paper and dissertation; not read in full.
- Azure and Google minimum counts are from search snippets; check the pages for the exact API version.
- No Devpost or Product Hunt match found for learning extraction from examples.
