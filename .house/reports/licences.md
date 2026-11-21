# Licence check for ODWOLANIA2JSON (researcher, 2026-11-21)

Rule applied (from the task brief and regulamin §4): winner transfers economic rights to UZP, so only open-source
components, including open-source LLM weights, CPU only. Verdict OK = OSI-approved permissive licence on the primary
page. RISK = copyleft (AGPL/GPL/LGPL/MPL-at-runtime), non-OSI licence, or licence not confirmed on a primary page.
"(sidebar)" = licence shown on the GitHub repo sidebar; "(HF)" = Hugging Face model card YAML field.
Not a legal opinion; verify with the UZP legal team before the pitch.

## Document and OCR libraries

| Component | Licence | Source | Verdict |
|---|---|---|---|
| pdfplumber | MIT (sidebar) | https://github.com/jsvine/pdfplumber | OK |
| pdfminer.six | MIT | not fetched (known MIT; unverified in this session) | OK (verify) |
| pypdfium2 | Apache-2.0 or BSD-3-Clause; PDFium bundles BSD-style deps, ship their licences | https://github.com/pypdfium2-team/pypdfium2 | OK |
| PyMuPDF | AGPL-3.0 (sidebar); commercial licence from Artifex | https://github.com/pymupdf/PyMuPDF | RISK (AGPL) |
| Tesseract | Apache-2.0 (sidebar) | https://github.com/tesseract-ocr/tesseract | OK |
| pytesseract | Apache-2.0 | not fetched (unverified) | OK (verify) |
| Polish tessdata (pol.traineddata) | Apache-2.0 "All data in the repository are licensed under the Apache-2.0 License" | https://github.com/tesseract-ocr/tessdata | OK |
| RapidOCR (code) | Apache-2.0 (README) | https://github.com/RapidAI/RapidOCR | OK |
| RapidOCR ONNX models | derived from PaddleOCR, Apache-2.0 per repo README; per-model terms in MODEL_LICENSES.md | https://github.com/RapidAI/RapidOCR | OK (check MODEL_LICENSES.md) |
| ocrmypdf | MPL-2.0 (sidebar); needs Ghostscript at runtime | https://github.com/ocrmypdf/OCRmyPDF | RISK (depends on Ghostscript, see next line) |
| Ghostscript | AGPL (open source) or commercial from Artifex; "Combining Ghostscript with other software might bring further obligations under AGPL" | https://ghostscript.com/licensing (search summary, not fetched directly) | RISK (AGPL) |
| docling (code) | MIT (sidebar) | https://github.com/docling-project/docling | OK |
| docling models | HF tags "cdla-permissive-2.0" and "apache-2.0" on one page; no statement which file has which | https://huggingface.co/docling-project/docling-models | RISK until each model file is mapped to a licence (CDLA-Permissive-2.0 is not on the OSI list) |

## NLP and utilities

| Component | Licence | Source | Verdict |
|---|---|---|---|
| simplemma | MIT (sidebar) | https://github.com/adbar/simplemma | OK |
| Morfeusz2 (software and SGJP dictionary) | BSD-2-Clause per Morfeusz paper (LREC 2014) and Morfologik licence file "BSD-licensed dictionary of Polish (SGJP)"; sgjp.pl itself did not load (TLS error) | https://aclanthology.org/L14-1597/ ; https://www.sgjp.pl/morfeusz/ (not reachable) | OK (confirm on sgjp.pl) |
| spaCy pl_core_news_md (and sm/lg) | GPL-3.0 (HF "License: gpl-3.0") | https://huggingface.co/spacy/pl_core_news_md | RISK (GPL) |
| rapidfuzz | MIT (sidebar) | https://github.com/RapidFuzz/RapidFuzz | OK |
| pydantic | MIT (sidebar) | https://github.com/pydantic/pydantic | OK |
| FastAPI | MIT (sidebar) | https://github.com/fastapi/fastapi | OK |
| Streamlit | Apache-2.0 (sidebar) | https://github.com/streamlit/streamlit | OK |
| Gradio | Apache-2.0 (sidebar) | https://github.com/gradio-app/gradio | OK |

## LLM runtimes and extraction tools

| Component | Licence | Source | Verdict |
|---|---|---|---|
| llama.cpp | MIT (sidebar) | https://github.com/ggml-org/llama.cpp | OK |
| Ollama | MIT (sidebar) | https://github.com/ollama/ollama | OK |
| Google LangExtract (if used) | Apache-2.0 (sidebar and README) | https://github.com/google/langextract | OK |
| NuExtract-1.5-tiny | MIT (HF) | https://huggingface.co/numind/NuExtract-1.5-tiny | OK |
| NuExtract-1.5 (larger) | MIT per HF listing (search snippet; card not fetched); newer NuExtract3 exists (not checked) | https://huggingface.co/numind/NuExtract-1.5 | OK (verify card) |

## Open-weights LLMs

| Model | Licence | Source | Verdict |
|---|---|---|---|
| Bielik-11B-v2.6-Instruct | Apache-2.0 (HF "License: apache-2.0"); NVIDIA-hosted copy uses NVIDIA Open Model License, so use the SpeakLeash weights | https://huggingface.co/speakleash/Bielik-11B-v2.6-Instruct | OK (CPU-heavy) |
| Bielik-4.5B-v3.0-Instruct | Apache-2.0 (HF); 4.6B params, instruct | https://huggingface.co/speakleash/Bielik-4.5B-v3.0-Instruct | OK |
| Bielik-1.5B-v3.0-Instruct | Apache-2.0 (HF); ~1.6B params (card text; widget shows 2B), instruct | https://huggingface.co/speakleash/Bielik-1.5B-v3.0-Instruct | OK |
| PLLuM-12B-chat-2412 | Apache-2.0 (HF) | https://huggingface.co/CYFRAGOVPL/PLLuM-12B-chat | OK |
| PLLuM-12B-nc-chat-2412 and other "nc" variants | CC-BY-NC-4.0 (HF / collection) | https://huggingface.co/CYFRAGOVPL/PLLuM-12B-chat (family note) | RISK (non-commercial, non-OSI) |
| Llama-PLLuM-8B (chat/instruct/base, incl. 2512) and Llama-PLLuM-70B | Llama 3.1 licence (HF "License: llama3.1") | https://huggingface.co/CYFRAGOVPL/Llama-PLLuM-8B-instruct-2512 | RISK (Llama licence, not OSI) |
| PLLuM 2512 small (4B/12B) | not checked on the page; 12B base/chat earlier were Apache-2.0 | https://huggingface.co/CYFRAGOVPL/models | RISK until checked |
| Qwen2.5-1.5B-Instruct | Apache-2.0 (HF) | https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct | OK |
| Qwen2.5-3B-Instruct | "qwen-research" (HF) | https://huggingface.co/Qwen/Qwen2.5-3B-Instruct | RISK (Qwen Research licence) |
| Qwen3 small (0.6B-4B) | "All our open-weight models are licensed under Apache 2.0" (QwenLM/Qwen3 README). Qwen3-1.7B card did not expose a licence field to the fetcher | https://github.com/QwenLM/Qwen3 ; https://huggingface.co/Qwen/Qwen3-1.7B | OK (confirm on each card) |
| Mistral-7B-Instruct-v0.3 | Apache-2.0 (HF) | https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3 | OK (7B, too slow on CPU) |
| Basal-mini: basal-1.5-mini (1.5B, Oct 2026) and basal-2.0-mini (1.5B, 2026-10-12) by Remek Kinas; Bielik-1.5B base; typed-decision classifier (probabilities per option, no text generation) | Apache-2.0 (HF card YAML and HF API cardData); base Bielik-1.5B-v3.0-Instruct Apache-2.0 | https://huggingface.co/Remek/basal-1.5-mini ; https://huggingface.co/Remek/basal-2.0-mini | OK on card (self-declared; not legal review). Quality numbers are author-reported. See reports/model-basal.md |
| Basal-pico: basal-omni-pico (0.75B, 2026-10-22); base Qwen3.5-0.8B-Base; distilled from basal-omni-1.0-ultra (Gemma 4 31B teacher) | Apache-2.0 (HF card and HF API cardData); base Qwen3.5-0.8B-Base Apache-2.0 (HF API) | https://huggingface.co/Remek/basal-omni-pico | OK on card; RISK to check: Gemma-4 teacher licence not verified. See reports/model-basal.md |
| basal inference engine (rkinas/basal, needed to run typed decisions; pins transformers==5.17.0, torch>=2.11) | Apache-2.0 (pyproject.toml at v1.5.0; LICENSE text read) | https://github.com/rkinas/basal | OK (Python 3.13 wheels not verified) |
| basal-omni-1.0 / 1.1 / 2.0-mini-preview (Gemma 4 base: mini E4B, max 12B, ultra 31B) | HF cardData says apache-2.0, but base is google/gemma-4-*; Gemma licence not checked | https://huggingface.co/Remek/basal-omni-1.0-ultra | RISK until Gemma 4 licence is checked. Out of scope for CPU use |

## Questions asked in the brief

**CPU speed for 1.5-4B models (rough, not measured here):** no clean like-for-like benchmark found. Secondary sources:
Qwen2 3B Q4_K_M, 4 CPU threads: about 23 tokens/s generation, 67 tokens/s prompt (llama.cpp-style table; the source
does not name the CPU). A 1.5B Q4_K_M model: anecdotal 10 to 35 tokens/s on laptop CPUs. Expect tens of tokens/s
for 1.5B and about 20 for 3B on a modern laptop CPU; measure with `llama-bench -m <gguf> -p 512 -n 128 -t <cores>`
on the target machine. Sources: https://dev.to/ymir/how-i-tested-5-small-llms-on-a-weak-pc-intel-i5-no-gpu-and-found-a-winner-55cm
and https://itsfoss.com/testing-local-llms-without-gpu (both unverified in detail). Ollama runs on llama.cpp, so the
same ballpark applies.

**Free hosted APIs for open-weights models without our own GPU:** Hugging Face Inference Providers gives free users
under $0.10 of monthly credit, then pay-as-you-go (https://huggingface.co/docs/inference-providers/pricing, per search
summary; not fetched). Not a reliable free API. A hosted endpoint may also conflict with the brief's "runs locally
(on-premise)" requirement (spec.yaml rules). Other free-tier providers were not checked.

## Best CPU-friendly open model with an OK licence

**Bielik-1.5B-v3.0-Instruct (Apache-2.0)**: Polish-trained, instruct, about 1.6B parameters, fits CPU quantised
inference. Fallback with the same licence: Qwen2.5-1.5B-Instruct (Apache-2.0) or Qwen3 small (Apache-2.0 per README).
Bielik-4.5B-v3.0-Instruct (Apache-2.0) if CPU time allows. Quality on Polish legal text was not benchmarked here.

## Open points

- sgjp.pl (Morfeusz2 official page) did not load: confirm the BSD-2 claim there.
- docling-models: map each model file to its licence.
- PLLuM 2512 small variants and NuExtract-1.5 (larger) model cards: not read.
- Ghostscript licence taken from ghostscript.com search summary, not fetched directly.
- No legal review performed.
