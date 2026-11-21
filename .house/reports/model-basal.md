# Basal models (Basal-mini / Basal-pico): research for ODWOLANIA2JSON

Researcher, 2026-11-21. Scope: the owner asked about "Basal-mini" and "Basal-pico" as a fast first-pass classifier.

## Answer first

- **Found.** "Basal" is a family of Polish/English "typed-decision" models by Remigiusz (Remek) Kinas, an individual developer, published on Hugging Face from late Sep 2026. "Basal-mini" maps to `Remek/basal-1.5-mini` (1.5B, Oct 2026) and its newer sibling `Remek/basal-2.0-mini` (1.5B, 2026-10-12). "Basal-pico" maps to `Remek/basal-omni-pico` (0.75B, 2026-10-22). No other model named "basal-pico" was found on Hugging Face, GitHub or the web. The mapping is my inference from names; the owner should confirm.
- **Licence.** Apache-2.0 on the model cards and in the inference-engine repo. Base models are Apache-2.0 too (Bielik-1.5B-v3.0-Instruct; Qwen3.5-0.8B-Base). This is an OSI licence, so it passes our licence rule on the card, pending UZP legal review. Caveat: the larger "basal-omni" models are built on Google Gemma 4, and Gemma's licence was not checked; they are out of scope for us.
- **Size and speed.** Mini: 1.6B parameters, about 3.2 GB in BF16, about 1.7 GB as a Q8 GGUF. Pico: 0.75B, about 1.5 GB in BF16. No CPU speed for mini is published. The only CPU number is the author's: pico Q8 GGUF, one request with two questions, about 0.5 s on 16 CPU threads (author's machine, unverified).
- **Recommendation: use for classification only, and only as an optional extra.** Reason: the licence is clean and the model fits a 16 GB CPU box, but its quality claims are self-reported on the author's private benchmark, it does not extract fields, and it adds a second model dependency. Build and measure the TF-IDF + logistic-regression baseline first; try basal-2.0-mini (or pico) zero-shot on our 60 cases with a reject class, and keep it only if it beats the baseline on F1.

## What "typed decisions" means (how the model is used)

Primary source: the model card of `Remek/basal-1.5-mini`, https://huggingface.co/Remek/basal-1.5-mini (raw README read via curl).

- The model reads a "state" (text, a document, passages) and answers a typed question (`choice`, yes/no `noul`, `score`, `multi`, `act`) by returning a calibrated probability for each option you supply, "in one forward pass, without generating text".
- The classes are described in the request, so no retraining is needed to add a class. This fits the reject class and the "new classes via config" criterion in our spec. It does not fit field extraction: the output is a choice among given options, not extracted spans or values.
- Serving is via the `basal` package (`basal-serve`), https://github.com/rkinas/basal, README v2.8.1 (raw read). Plain `transformers` loading gives a causal LM; the typed readout lives in the basal engine (the HF file list for 1.5-mini includes `evidence_head.pt`, `basal.json`, `CALIBRATION.json`). So we would depend on that package, not only on the weights.

## Model 1: basal-1.5-mini ("Basal-mini", older)

| item | value | source |
|---|---|---|
| Publisher | Remigiusz Kinas (HF "Remek"), individual developer | HF card citation; Bezprawnik article https://bezprawnik.pl/basal-ai/ (article dated 25.10.2026, author Jakub Bilski) |
| Created / last modified | 2026-10-03 / 2026-11-05 | HF API https://huggingface.co/api/models/Remek/basal-1.5-mini |
| Architecture | `LlamaForCausalLM`, 32 layers, 32k Polish vocab; fine-tuned from Bielik-1.5B-v3.0-Instruct (not Gemma; the card says so) | HF config and card |
| Parameters | 1,596,507,648 (BF16). Card text says 1.5B; HF widget says 2B | HF API `safetensors.total`; card |
| Task type | Generative-architecture LM used as a classifier: probability per allowed option, one forward pass | card |
| Licence | `apache-2.0` (YAML and text); base `speakleash/Bielik-1.5B-v3.0-Instruct` also Apache-2.0 | card; HF API cardData |
| Polish claims | Werdykt (author's hidden PL+EN benchmark, 20 cells): 0.607 (PL 0.619, EN 0.594). PL sealed test 0.910; PL decisions held-out 0.877; PL general knowledge 0.667; EN external panel 0.581. Card: "Polish world knowledge of a small model is limited". | card table |
| Speed claim | 14.2 ms per decision on one H100 (basal engine, bf16). No CPU figure. | card |
| Formats | Safetensors BF16, GGUF (`Remek/basal-1.5-mini-GGUF`), MLX, FP8 | HF API listing |

Independent verification: none. The benchmark is the author's own ("our hidden Polish–English benchmark"). Bezprawnik reports a JevBench ranking (17 Oct) for the larger models; the author's ranking claims were not verified.

## Model 2: basal-2.0-mini (newer mini, same family)

| item | value | source |
|---|---|---|
| Created / modified | 2026-10-12 / 2026-11-15 | HF API https://huggingface.co/api/models/Remek/basal-2.0-mini |
| Architecture | Built on Bielik-1.5B-v3.0-Instruct, "trained further ... with basal-2.0-max as the teacher" | https://huggingface.co/Remek/basal-2.0-mini (card header read via curl) |
| Parameters | 1,596,507,648 (BF16) | HF API |
| Licence | `apache-2.0` | HF API cardData |
| Polish claims | Werdykt number not extracted (the card and README were not read in full). The GitHub README lists it as "fastest; high-volume routing, laptops and small GPUs; context 8,192 tokens". | https://github.com/rkinas/basal README |

This is the newer "mini" on the same engine; I would test this one first if we go ahead.

## Model 3: basal-omni-pico ("Basal-pico")

| item | value | source |
|---|---|---|
| Created / modified | 2026-10-22 / 2026-11-15 | HF API https://huggingface.co/api/models/Remek/basal-omni-pico |
| Architecture | `qwen3_5_text`, built on Qwen/Qwen3.5-0.8B-Base, text only; trained with basal-omni-1.0-ultra (31B, Gemma 4) as teacher | https://huggingface.co/Remek/basal-omni-pico (raw README) |
| Parameters | 752,393,024 (BF16) | HF API |
| Task type | Typed-decision model, same as above | card |
| Licence | Model `apache-2.0`; base `Qwen/Qwen3.5-0.8B-Base` `apache-2.0` (HF API tag and card licence_link) | HF API; https://huggingface.co/Qwen/Qwen3.5-0.8B-Base |
| Polish claims | Werdykt 0.660 (PL 0.661, EN 0.659); routing 0.912, retrieval 0.886, real documents 0.848, rules 0.316, contracts 0.542. Card: not for "rule checks" or "facts not in the state". | card |
| CPU | GGUF Q8_0 on 16 CPU threads: about 0.5 s for the card's example request (two questions); GGUF agrees with the transformers model in 99.29% of cases on CPU (author's dev set) | card, GGUF section |
| Formats | BF16, GGUF Q8_0 (`Remek/basal-omni-pico-GGUF`), ONNX-web (community) | HF API |

Licence risk to check: the teacher was a Gemma 4 model. Distillation from a teacher's outputs can carry the teacher's terms; I did not verify Gemma's licence or whether it matters for the weights. Mark as an open point for UZP legal.

## Other searched names (not Basal)

- `Bielik Guard` (arXiv 2602.07954, Wróbel et al.): a Polish safety classifier family, 0.1B and 0.5B RoBERTa-based. It is not "Basal". Its weights licence is not stated on the page (only the paper is CC BY 4.0). https://arxiv.org/abs/2602.07954 (summary read via WebFetch, not verbatim).
- `pico-lm/*` and `LucidityAI/pico-mini`: English research models, unrelated.
- A Hugging Face substring search for "basal" returns many unrelated projects (for example "Basalt" and "Basalam"); those were excluded.

## Python 3.13 and dependency check

- `basal` 1.5.0 (`pyproject.toml`, https://raw.githubusercontent.com/rkinas/basal/v1.5.0/pyproject.toml): `requires-python = ">=3.10"`, `torch>=2.11`, `transformers==5.17.0` (pinned), `accelerate`, `safetensors`, `starlette`, `uvicorn`, `httpx`. Optional: `vllm`, `torchao`, `llama-cpp-python` (gguf mode).
- The model card's install example uses Python 3.12 and torch 2.11 from the CUDA 12.8 index; the GitHub README uses `uv venv --python 3.12`. Python 3.13 was not tested by the author. Whether `torch>=2.11` and `transformers==5.17.0` have cp313 wheels for Windows was not verified.
- `llama-cpp-python` (for GGUF on CPU) needs a compiler or a wheel for 3.13; not verified.
- Our machine constraint (no GPU, 16 GB) is covered by the CPU path (`--mode eager` or `gguf`), per the GitHub README and the pico card. Note that the README says the `fast` mode is for H100 and `fp8`/`nvfp4` need Hopper or Blackwell, so those are not for us.

## Quality and fit for our two jobs (estimates, not measured)

1. **Document classification with a reject class (odwolanie / pelnomocnictwo / przelew / reject).** Zero-shot typed decision is the designed use case. A `choice` question with four options gives a probability per class; the reject class is an ordinary option. Unknown: performance on our synthetic and real PDFs. Our 60 cases are not enough to trust a self-reported 0.6-0.7 benchmark. A TF-IDF + logistic regression baseline on the PDF text layer is very cheap and likely strong on this split; the LLM is only worth it for scanned or noisy inputs after OCR.
2. **Field extraction / repair.** Not a good fit. The models choose among options or give a score; they do not return values. For "repair" (e.g. picking the right candidate among regex hits), a typed `choice` over candidates could work, but that is a different design from what our spec asks.

Comparison against the other options named by the owner:
- **TF-IDF + logistic regression:** no LLM, runs in seconds on CPU, no licence issue, sklearn BSD-3. Expected to be the baseline to beat.
- **HerBERT / Polish RoBERTa encoders:** not researched in this session (no sources fetched). For a 4-to-5-class classifier they are the standard fine-tuned option and would need GPU-free training on 180 docs; treat as unverified.
- **Bielik-1.5B-v3.0-Instruct (Apache-2.0):** the base of basal-1.5-mini and basal-2.0-mini. The basal models are Bielik with a typed-decision fine-tune; a plain Bielik prompt would be the comparison to run to see what the fine-tune adds. Not measured here.

## Fine-tuning on CPU

- Zero-shot use needs no fine-tuning.
- Full fine-tuning of pico (0.75B) in fp32 with Adam needs roughly 12 GB just for weights, gradients and optimizer state, too tight on 16 GB. LoRA (or training only the head) is the only realistic CPU option. Timing: a 0.75B forward/backward over long documents (thousands of tokens) on CPU is likely seconds per example, so 180 documents for several epochs is probably many hours (estimate, not measured). A text-truncation to the first page or two would make it feasible.
- Mini (1.5B) is about twice as slow again; LoRA on CPU in a few hours is doubtful.

## CPU speed and RAM estimate (16 GB, no GPU)

- RAM: mini BF16 about 3.2 GB; fp32 about 6.4 GB; Q8 GGUF about 1.7 GB. Pico BF16 about 1.5 GB; fp32 about 3 GB; Q8 GGUF under 1 GB. All fit.
- Speed: no published mini CPU figure. From the pico author number (about 0.5 s for a short request on 16 threads), mini should be roughly 1-2 s per short request and several seconds for a long document (prompt processing dominates). These are estimates. Measure with the basal `--mode gguf` or `eager` on the target machine.

## Open points

1. Confirm with the owner that "Basal-mini" = `Remek/basal-1.5-mini` or `basal-2.0-mini`, and "Basal-pico" = `Remek/basal-omni-pico`.
2. Licence: Apache-2.0 on the cards and engine. Not a legal opinion. Open: whether the Gemma-4 teacher used for pico's distillation affects the weights; whether the basal engine's own dependencies (torch, transformers, llama-cpp) pass our licence rule (all are standard OSI licences, not checked here).
3. Independent evaluation: all Werdykt numbers are the author's; no independent replication found.
4. Python 3.13 wheels: not verified.
5. The Bezprawnik article (25.10.2026) describes the same author and claims a JevBench ranking; not verified.
6. Our own eval (the 60 training cases, F1) is the only test that matters for the decision.

## Sources

- https://huggingface.co/Remek/basal-1.5-mini (card, raw README)
- https://huggingface.co/api/models/Remek/basal-1.5-mini (metadata)
- https://huggingface.co/Remek/basal-2.0-mini (card header; metadata https://huggingface.co/api/models/Remek/basal-2.0-mini)
- https://huggingface.co/Remek/basal-omni-pico (raw README; metadata https://huggingface.co/api/models/Remek/basal-omni-pico)
- https://huggingface.co/Qwen/Qwen3.5-0.8B-Base (licence in card)
- https://github.com/rkinas/basal (README v2.8.1; LICENSE Apache-2.0 text)
- https://raw.githubusercontent.com/rkinas/basal/v1.5.0/pyproject.toml
- https://bezprawnik.pl/basal-ai/ (secondary, Polish press)
- https://arxiv.org/abs/2602.07954 (Bielik Guard, unrelated; WebFetch summary)
- Search lists: "Basal-mini Basal-pico Polish language model", "Basal mini pico model Hugging Face Polish", "Basal Polish AI model 2026 classifier small" (WebSearch, 2026-11-21); HF API author listing for Remek and substring search for "basal" and "basal-pico".
- Not found: "Basal-pico" under any other name; ollama.com/pdurlej/basal-1.0 returned 404.
