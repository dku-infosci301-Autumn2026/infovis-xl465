---
title: VA Blueprint Task Explorer
emoji: 🔎
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---
# VA-Blueprint Task Explorer
An AI-assisted INFOSCI301 research prototype for Xinyuan Lan, NetID xl465. It extends the exploration task of VA-Blueprint (IEEE VIS 2025; TVCG 32(1), 2026, 1197–1207; DOI 10.1109/TVCG.2025.3634809).

**Status:** locally implemented and technically tested. Student argument, source/example mappings, photograph metadata and human verification require review. Course-organization deployment is not complete. No participant study is claimed.

## Project and website URLs
Course Project URL: NOT YET DEPLOYED. Live Website URL: NOT YET DEPLOYED. Required owner: `dku-infosci301-Autumn2026`. No accessible repository in that organization was returned by the connected GitHub account on 2026-09-13. A personal repository does not satisfy the course-owner requirement.

## Run locally
Python 3.12 recommended. Windows: double-click `start_windows.bat` (requires Python). Otherwise:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Open http://localhost:7860. The 23 MB package includes the pinned quantized model and tokenizer. Inference runs on the CPU; no API key, paid access, training or runtime model download is needed. Installing Python dependencies requires internet. Do not open index.html directly: retrieval uses the included Python server.

## Walkthrough
Enter “How can I see a value rise and fall over time?”; select a candidate. The graph highlights the component and its immediate recorded neighbors. The inspector shows upstream description, inputs, outputs and citation. Linked Vega-Lite examples are clearly marked as analogous reference implementations. Open the pinned specification locally or follow its external gallery link. Toggle method and example descriptions to compare four retrieval conditions. “Show all links” removes focus. A table exposes every graph dependency.

## Contribution and data
The current corpus is **2 systems, 27 components and 40 recorded dependencies**, selected from VA-Blueprint's 101-system corpus. Six pinned Vega-Lite specifications add public example descriptions and inspectable code. A proposed explicit mapping connects 8 components to examples; the other 19 remain unmatched rather than guessed. MiniLM embeds task text and descriptions for cosine retrieval. This is retrieval, not answer generation. `data/manifest.json` records pinned revisions and hashes; `DATA_CARD.md` states governance limits.

Base records: `urban-toolkit/va-blueprint`, commit b4b9bd7f7b46c49a44eb7306eafb72e7a0dad1b7, TaxiVis and Urban Pulse JSON. Additional data: `vega/vega-lite`, commit 831e308cf9feba791db0c279dea5f7983ca98445, six example JSON specifications. Model: `sentence-transformers/all-MiniLM-L6-v2`, revision 1110a243fdf4706b3f48f1d95db1a4f5529b4d41, `onnx/model_quint8_avx2.onnx`. Model vectors: masked mean pooling, L2 normalization, 256-token truncation, fixed 0.30 display cutoff (uncalibrated, not confidence).

## Reproduce evaluation
```sh
python tests/evaluate.py
```
Protocol and 12 AI-authored diagnostic queries were saved before the first run. `evidence/retrieval-results.json` contains every returned candidate, rank, elapsed time, environment and limitation. K0 source/BM25: 6/12 top-3 hits; K1 added examples/BM25: 7/12; S0 source/MiniLM: 8/12; S1 added examples/MiniLM: 9/12. These are illustrative fixtures, not independent relevance judgments or evidence of learning. Q02, Q03 and Q11 fail in S1; do not omit them. No inferential statistical claim is made.

`tests/HUMAN_TASKS.md` is an unperformed follow-up procedure. Do not fill it with invented participants. Browser checks, where available, are recorded separately. A keyword fallback is used and labeled when the local model cannot initialize; empty queries and malformed input return explicit messages. Missing examples are shown as missing coverage, not absent implementations.

## Earlier work and migration
Week 2 artifact: https://github.com/xinnylll/network-vis-emerging-tech-template at commit 798ba79c26874ce6221bd3941b570d47577d942f. Exact HF airport dataset: https://huggingface.co/datasets/anomalypoint/NEExT at 36114f8da77d4fe5b4700a7ff2673b15901a6caf, airports subset. Earlier financial-inclusion proposal used `electricsheepafrica/africa-financial-inclusion-all` at 5cbca17b8cd5bab7c43c0b17ff23701d5989bcb3. These are development evidence, not input to current retrieval. Node inspection, source labels, missingness and failure safeguards transfer; airport connectivity or financial inclusion claims do not.

## Deploy to the course organization
Use a Docker Hugging Face Space owned by `dku-infosci301-Autumn2026` (e.g. infovis-xl465 once actually created). Upload this folder's contents including model files; the Dockerfile serves port 7860. Alternatively store the repository in the course GitHub organization and deploy this Python/Docker app on a compatible host. GitHub Pages alone cannot run app.py. Copy actual Project and Website URLs into this README and Section 3; verify signed-out access and interaction. Do not substitute a placeholder URL for a deployed resource. No authentication credentials are included.

## Credits and limits
Original research, upstream JSON and annotations: Leonardo Ferreira, Gustavo Moreira and Fabio Miranda. Example specifications: Vega-Lite contributors / University of Washington Interactive Data Lab. MiniLM model: Sentence Transformers contributors; model card in models/README.md. Original UI/engine here was generated with Codex assistance; student review remains pending. Metabase and Gapminder/Vizabi are retained design precedents from the earlier proposal; none of their code is copied.

Original source annotations may contain adapted or inferred statements. The example mapping does not certify compatibility, factual source accuracy, or authors' intended implementation. Search scores are not probabilities. A small English-language subset cannot establish utility for all urban systems, Chinese queries, museum visitors or a Kunshan community. The technical test baseline is BM25 in this reconstruction, not a performance measurement of the original VA-Blueprint website.

See THIRD_PARTY_NOTICES.md and AI_ASSISTANCE.md. Field photos and private course material are excluded from this public-ready code package until permissions are confirmed.
