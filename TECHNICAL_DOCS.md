I’ll open your Hugging Face Space code, extract the exact workflow/entrypoints/env vars/output schema, then draft two concise but complete READMEs: one GitHub-style and one Notion-friendly technical doc, both aligned to your repo.


Below are two ready-to-paste docs (1) **GitHub `README.md`** and (2) **Notion Technical Doc** for your Hugging Face codebase.

---

## 1) GitHub README (`README.md`)

# Financial Statements Classifier (PDF → Statement Page Ranges)

Classifier for **financial reports in PDF** that segments the three primary financial statements:

* **Balance Sheet** (Statement of Financial Position)
* **Profit & Loss** (Income / Earnings / Operations)
* **Cash Flow Statement**

It supports **both** **consolidated** and **standalone** (when present), returning **page blocks** with explicit `pages` lists (not just single-page hits). ([Hugging Face][1])

---

## How it works (high-level)

1. **Extract text per page**

   * If the PDF is digital → use extracted text.
   * If a page is likely scanned / low-text → OCR using Tesseract. ([Hugging Face][2])

2. **Heuristic candidate discovery**

   * Finds statement pages using:

     * title variants (incl. consolidated/standalone)
     * signature table terms (line items)
     * table-likeness features (numbers/years/currency/parentheses)
   * Builds **blocks** and extends multi-page statements using continuation scoring. ([Hugging Face][3])

3. **Select pages to send to the LLM (image budgeted)**

   * Prefer heuristic blocks and try to include **both scopes** (consolidated + standalone) when detected.
   * Adds neighbors (`start-1`, `end+1`) to reduce boundary misses. ([Hugging Face][3])

4. **Render selected pages to images + send to OpenRouter vision model**

   * Sends **page images + OCR/native snippets** with a strict JSON schema request. ([Hugging Face][1])

5. **Normalize/validate output**

   * Ensures each block includes `pages`, clamps page numbers, and derives `start_page/end_page` from `pages`. ([Hugging Face][1])

---

## Output format (JSON)

Each statement is a **LIST of blocks** (empty list if not present). Pages are **1-indexed**. ([Hugging Face][1])

Example (both consolidated + standalone):

```json
{
  "balance_sheet": [
    {
      "scope": "standalone",
      "start_page": 90,
      "end_page": 92,
      "pages": [90, 91, 92],
      "confidence": 0.86,
      "title": "Standalone Balance Sheets",
      "evidence_pages": [90, 91]
    },
    {
      "scope": "consolidated",
      "start_page": 133,
      "end_page": 135,
      "pages": [133, 134, 135],
      "confidence": 0.89,
      "title": "Consolidated Balance Sheets",
      "evidence_pages": [133, 134]
    }
  ],
  "profit_and_loss": [],
  "cash_flow": [],
  "notes": []
}
```

---

## Repo structure

* `main.py` — CLI entry + end-to-end `analyze_pdf()` pipeline; prompt + schema + output normalization ([Hugging Face][1])
* `pdf_io.py` — text extraction + selective OCR + PDF page rendering to PNG bytes ([Hugging Face][2])
* `statement_candidates.py` — heuristic scoring, block building, scope detection, and page selection for LLM ([Hugging Face][3])
* `openrouter_client.py` — OpenRouter chat/vision call helpers + JSON repair/parsing (used by `main.py`) ([Hugging Face][1])
* `config.py` — env + defaults (image budget, DPI, OCR lang, model selection list) ([Hugging Face][4])
* `app.py` — FastAPI server for Hugging Face Space (`/analyze`, `/pdf/page/{page_num}`) ([Hugging Face][5])
* `index.html` — simple UI to upload PDF + view outputs/pages

---

## Requirements

Python deps are in `requirements.txt` (FastAPI, Uvicorn, PyMuPDF, pytesseract, etc.). ([Hugging Face][6])
System dependency: **Tesseract OCR** (installed in Dockerfile for HF Spaces). ([Hugging Face][7])

---

## Setup

### 1) Install system OCR (Tesseract)

* Debian/Ubuntu:

  ```bash
  sudo apt-get update
  sudo apt-get install -y tesseract-ocr
  ```

### 2) Install Python deps

```bash
pip install -r requirements.txt
```

### 3) Configure environment

Create `.env`:

```bash
OPENROUTER_API_KEY="YOUR_KEY"
# optional:
OPENROUTER_MODEL=""        # if empty, auto-picks a free vision model
MAX_IMAGES="12"
PDF_RENDER_DPI="200"
OCR_LANG="eng"
MIN_TEXT_CHARS_FOR_DIGITAL="80"
TOPK_PER_STATEMENT="3"
MAX_BLOCKS_PER_STATEMENT="2"
CONTINUATION_MAX_FORWARD="6"
```

These settings and defaults are defined in `config.py`. ([Hugging Face][4])

---

## Run (CLI)

```bash
python main.py --pdf "/path/to/report.pdf" --out "ranges.json"
```

`main.py` uses a strict JSON schema where each statement is a list of blocks and must include `pages`. ([Hugging Face][1])

---

## Run (API / Hugging Face Space)

Start locally:

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

Endpoints:

* `POST /analyze` — upload a PDF and get JSON result
* `GET /pdf/page/{page_num}` — returns PNG of a page (for UI viewing)

Implemented in `app.py`. ([Hugging Face][5])

---

## Model selection (free vision)

If `OPENROUTER_MODEL` is not set, the code auto-selects from a list of free vision-capable models in `config.py`. ([Hugging Face][4])

---

## Future work

* Add segmentation for **Notes to Financial Statements** (currently only mentioned as a future target; not fully implemented). ([Hugging Face][3])

---

## References

[1] `main.py` (prompt/schema/output normalization) ([Hugging Face][1])
[2] `statement_candidates.py` (title variants, signature terms, block building, selection) ([Hugging Face][3])
[3] `pdf_io.py` (extraction/OCR/render) ([Hugging Face][2])
[4] `config.py` (env vars + defaults + free model list) ([Hugging Face][4])
[5] `app.py` (API endpoints + upload handling) ([Hugging Face][5])
[6] `requirements.txt` + `Dockerfile` (deps + Tesseract install) ([Hugging Face][6])

---

---

## 2) Notion Technical Doc (paste into Notion)

# Financial Statements Classifier — Technical Documentation

## Goal

Given a company’s financial report PDF, return **page blocks** for the three primary financial statements:

1. Balance Sheet / Statement of Financial Position
2. Profit & Loss / Income / Earnings / Operations
3. Cash Flow Statement

The system is designed to return **both** **standalone** and **consolidated** blocks when present, and each block must include an explicit `pages` list. ([Hugging Face][1])

---

## System overview

### Core pipeline (end-to-end)

**Entry:** `analyze_pdf()` in `main.py` ([Hugging Face][1])

1. **Text extraction + OCR**

   * Extract per-page text.
   * If a page is scanned / low text, run Tesseract OCR.
   * Mixed PDFs are supported (some pages digital, some scanned). ([Hugging Face][2])

2. **Heuristic discovery (fast + explainable)**

   * `statement_candidates.py` identifies statement pages using:

     * **Title variants** (example: “Consolidated Balance Sheets”, “Standalone Statements of Operations”, etc.) ([Hugging Face][3])
     * **Signature terms** (table line-items & structure cues)

       * Balance sheet: “total assets”, “total liabilities”, “total equity”, “current assets”, etc.
       * P&L: “revenue”, “gross profit”, “profit before tax”, “earnings per share”, etc.
       * Cash flow: “cash flows from operating/investing/financing activities”, etc. ([Hugging Face][3])
     * Table-likeness stats (numbers ratio, year count, currency cues, parentheses count) and penalties (TOC dot-leaders, note headings). ([Hugging Face][3])

3. **Block building (multi-page statements)**

   * If a statement title is detected, build a block and **expand forward**:

     * Continuation pages may not repeat titles; expansion uses signature signals and “continued” patterns. ([Hugging Face][3])
   * Title hits are clustered, then blocks are deduped/merged by overlap. ([Hugging Face][3])

4. **Scope handling (standalone vs consolidated)**

   * Scope is inferred from matched title variants (“consolidated”, “standalone”) and stored per block. ([Hugging Face][3])
   * Selection tries to keep **distinct scopes** when possible (so a report like Britannia can return both standalone and consolidated blocks). ([Hugging Face][3])

5. **LLM page selection (budget-aware)**

   * Convert blocks → pick pages for the vision LLM:

     * prioritize blocks across statements
     * include neighbors to tighten range boundaries
     * cap by `MAX_IMAGES` ([Hugging Face][3])

6. **Render selected pages → images**

   * Render chosen pages to PNG bytes at configured DPI. ([Hugging Face][2])

7. **Vision LLM verification & final range extraction**

   * `main.py` sends:

     * selected page images
     * OCR/native snippets per page
     * heuristic blocks for reference
   * LLM must return **strict JSON only** using list-of-blocks schema. ([Hugging Face][1])
   * Post-processing normalizes output so every block has `pages` and correct `start_page/end_page`. ([Hugging Face][1])

---

## Output contract

* Pages are **1-indexed**
* Each statement key is a **list of blocks**
* Each block must include:

  * `scope`: `consolidated | standalone | unknown`
  * `pages`: full explicit page list
  * `start_page/end_page`: derived from `pages` (or expanded if only start/end given)
  * `confidence`, `title`, `evidence_pages` ([Hugging Face][1])

---

## Configuration (env vars)

Defined in `config.py`: ([Hugging Face][4])

* `OPENROUTER_API_KEY` (required)
* `OPENROUTER_MODEL` (optional; if unset, auto-select free vision model)
* `MAX_IMAGES` (default 12)
* `PDF_RENDER_DPI` (default 200)
* `OCR_LANG` (default `eng`)
* `MIN_TEXT_CHARS_FOR_DIGITAL` (default 80)
* `TOPK_PER_STATEMENT` (default 3)
* `MAX_BLOCKS_PER_STATEMENT` (default 2)
* `CONTINUATION_MAX_FORWARD` (default 6)

Default free vision model list includes `google/gemma-3-12b-it:free`, `nvidia/nemotron-nano-12b-v2-vl:free`, `amazon/nova-2-lite-v1:free`. ([Hugging Face][4])

---

## API (Hugging Face Space)

Implemented via FastAPI in `app.py`: ([Hugging Face][5])

* `POST /analyze`

  * Upload a PDF
  * Returns JSON result from `analyze_pdf()`
* `GET /pdf/page/{page_num}`

  * Renders and returns a PNG for viewing in the UI

Note: uploaded file is saved to `/tmp/latest_upload.pdf` (simple demo approach, not multi-user safe). ([Hugging Face][5])

---

## Deployment notes (HF Space)

* Docker uses `python:3.10-slim`
* Installs `tesseract-ocr` and `libtesseract-dev`
* Runs `uvicorn app:app --port 7860` ([Hugging Face][7])
* Python dependencies are in `requirements.txt` (FastAPI/Uvicorn/PyMuPDF/pytesseract/etc.) ([Hugging Face][6])

---

## Code map

* `main.py` — orchestrates pipeline + LLM prompt/schema + output normalization ([Hugging Face][1])
* `pdf_io.py` — extract/OCR/render helpers ([Hugging Face][2])
* `statement_candidates.py` — statement detection logic + page picking ([Hugging Face][3])
* `config.py` — settings ([Hugging Face][4])
* `app.py` — Space API + UI integration ([Hugging Face][5])

---

## References

[1] Pipeline + JSON schema contract (`main.py`) ([Hugging Face][1])
[2] Heuristics + blocks + scope logic (`statement_candidates.py`) ([Hugging Face][3])
[3] OCR/text/render (`pdf_io.py`) ([Hugging Face][2])
[4] Settings + defaults (`config.py`) ([Hugging Face][4])
[5] API endpoints (`app.py`) ([Hugging Face][5])
[6] HF Docker + deps (`Dockerfile`, `requirements.txt`) ([Hugging Face][7])

[1]: https://huggingface.co/spaces/FridayCodehhr/finalyze/blob/main/main.py "main.py · FridayCodehhr/finalyze at main"
[2]: https://huggingface.co/spaces/FridayCodehhr/finalyze/blob/main/index.html "index.html · FridayCodehhr/finalyze at main"
[3]: https://huggingface.co/spaces/FridayCodehhr/finalyze/blob/main/statement_candidates.py "statement_candidates.py · FridayCodehhr/finalyze at main"
[4]: https://huggingface.co/spaces/FridayCodehhr/finalyze/blob/main/config.py "config.py · FridayCodehhr/finalyze at main"
[5]: https://huggingface.co/spaces/FridayCodehhr/finalyze/blob/main/app.py "app.py · FridayCodehhr/finalyze at main"
[6]: https://huggingface.co/spaces/FridayCodehhr/finalyze/blob/main/requirements.txt "requirements.txt · FridayCodehhr/finalyze at main"
[7]: https://huggingface.co/spaces/FridayCodehhr/finalyze/blob/main/Dockerfile "Dockerfile · FridayCodehhr/finalyze at main"
