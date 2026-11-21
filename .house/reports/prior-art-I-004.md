# Prior-art card: I-004 "Schemat UZP jako prompt" (rules floor + open LLM + grounding verifier)

Date: 2026-11-21. Researcher: haiku. Status of checks: YC directory run with 3 phrasings; web checks on
primary sources (GitHub sidebars/READMEs, Hugging Face model cards). Items marked "unverified" were not confirmed
on a primary page.

## Closest existing (max 5)

1. **NuMind (YC Summer 2022, Active)**: "The LLM provider for Document Extraction". Source: YC directory
   https://www.ycombinator.com/companies/numind. Closest commercial company to the idea (LLM-based document
   extraction). Proprietary service as far as this check shows; it also publishes open-weights NuExtract models.
2. **ContextGem (open source, Apache-2.0)**: Python framework "to extract structured data and insights from
   documents using LLMs"; README says "Every extracted fact is traced back to its source." Source:
   https://github.com/shcherbak-ai/contextgem (licence and README text checked). Also listed on Product Hunt
   https://www.producthunt.com/products/contextgem. Very close on "schema-driven LLM extraction with source trace";
   no rules floor, no UZP schema comments, no verifier that rejects ungrounded values (not checked in code).
3. **Google LangExtract (open source, Apache-2.0)**: library for structured extraction from text with LLMs, precise
   source grounding and interactive HTML visualisation; supports Gemini, OpenAI and local models via Ollama.
   Source: https://github.com/google/langextract (licence Apache-2.0 and "This is not an officially supported Google
   product" checked on the README). Closest technical match to the "grounded value" part of I-004.
4. **NuExtract 1.5 (open weights, MIT)**: small JSON-template extraction models by NuMind (tiny variant is a
   Qwen2.5-0.5B fine-tune). Source: https://huggingface.co/numind/NuExtract-1.5-tiny (licence MIT on the card).
   This is the open model a jury would name for "schema -> JSON on CPU"; it is the model-side competitor, not a product.
5. **Constrained-decoding libraries (open source)**: Outlines (Apache-2.0, https://github.com/dottxt-ai/outlines) and
   Instructor (MIT, https://github.com/567-labs/instructor) enforce a JSON schema on LLM output. They solve the
   "well-formed JSON" half of I-004 (the llm/ adapter), not grounding or rules.

Commercial, for the judge's awareness (not open source): Reducto (YC W2024, https://www.ycombinator.com/companies/reducto),
Extend (YC W2023), Pulse (YC S2024), Nanonets (YC W2017), Invofox (YC S2022), Pigeon (YC W2023), Sieve (YC Spring 2025,
AI + human review for data cleaning). Source for the list: `house yc` output (3 phrasings: "extract structured JSON
from scanned legal documents with an LLM"; "document data extraction from PDFs with human review"; "intelligent
document processing invoices contracts to structured data").

Product Hunt (web search): ContextGem (open source, see 2), Docuglean (open-source SDK, schema-typed extraction, no
citations claimed), Normain (traceability-first, appears commercial), StractusAI (payment required, not open source).

## What is genuinely different

The UZP annotated `oczekiwane-json` files are the configuration (comments are the field spec), and the
deterministic rules always produce a complete JSON, so the LLM is an optional escalation that can only change a
field if the verifier finds the value in the document text (plus checksum for identifiers). ContextGem and LangExtract
trace facts to sources but make the LLM the extractor of record; NuExtract and Outlines/Instructor give a schema but no
grounding gate and no rules floor. The combination "rules floor + grounded-only LLM patch + schema taken from the
client's own annotated JSON" is not in the list above.

## Market signal

Real: commercial document-extraction companies in YC (Reducto, Extend, Pulse, Nanonets, Invofox, NuMind), so the
problem is funded. No RFS entry checked: the Y Combinator RFS page could not be read directly (search snippet only;
unverified). No Devpost/past-winner evidence found for HackNation or UZP (search returned nothing relevant;
unverified).

## Risk for the rubric

- **Novelty risk: HIGH on the generic idea.** A judge who knows LangExtract or ContextGem will say "LLM extraction with
  source tracing exists". Defence: the novelty is the combination and the config source (UZP's own commented schema),
  not "LLM extracts fields". Show the rules-only run (D-005 requirement) next to the LLM run, and the rejected-value
  log.
- **Architecture/flexibility:** using the client's annotated schema as config is strong for the 30% flexibility
  criterion; judge needs the adapter seam (LLM is one adapter behind an interface) shown in code.
- **Pitch:** name LangExtract and ContextGem openly before the judge does (regulamin §4.1 requires naming external
  solutions used; this card does not claim we use them).
- **Licence risk for the LLM part:** Qwen2.5-3B is under the Qwen Research licence (RISK), Llama-based PLLuM is Llama
  3.1 licence (RISK). Use Apache-2.0 or MIT weights only; see reports/licences.md.

## Reusable open source (with licences)

- Google LangExtract: Apache-2.0 (https://github.com/google/langextract)
- ContextGem: Apache-2.0 (https://github.com/shcherbak-ai/contextgem)
- NuExtract-1.5-tiny: MIT (https://huggingface.co/numind/NuExtract-1.5-tiny; base Qwen2.5-0.5B)
- Outlines: Apache-2.0 (https://github.com/dottxt-ai/outlines)
- Instructor: MIT (https://github.com/567-labs/instructor)
- llama.cpp: MIT (https://github.com/ggml-org/llama.cpp); Ollama: MIT (https://github.com/ollama/ollama)
- Bielik-1.5B-v3.0-Instruct: Apache-2.0 (https://huggingface.co/speakleash/Bielik-1.5B-v3.0-Instruct)

## Open points

- Not verified in code: whether ContextGem or LangExtract run a grounding check the way I-004's verifier would.
- RFS page, Devpost/HackNation winners: not retrieved.
- Hugging Face model card for Qwen3 small models showed no licence field to the fetcher; licence taken from the Qwen3
  GitHub README sentence "All our open-weight models are licensed under Apache 2.0".
