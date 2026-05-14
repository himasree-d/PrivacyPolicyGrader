# 🔒 Privacy Policy Grader

> **CS5202 · GenAI and LLM · Spring 2026 · Group 22**

An AI-powered web application that automatically analyses, grades, and explains privacy policies. Paste any URL or raw policy text and get an instant A–F grade with a full breakdown — what data is collected, who it's shared with, your rights, dark patterns, and GDPR compliance.

**Live Demo → [privacy-policy-grader.onrender.com](https://privacy-policy-grader.onrender.com)**

---

## What It Does

Privacy policies average 18–30 minutes to read and require post-graduate reading comprehension. Nobody reads them. This tool fixes that — it reads the policy, grades it, and tells you exactly what to worry about in under 30 seconds.

- **Analyse by URL** — paste any privacy policy URL and the scraper extracts the text
- **Analyse by text** — paste raw policy text directly (works offline with the sample files)
- **Letter grade A–F** — weighted across 5 dimensions with full sub-score breakdown
- **Trust Score** — composite 0–100 score penalising dark patterns and unverified LLM claims
- **Red flags** — severity-ranked issues with exact quotes from the policy
- **Dark pattern detection** — 15 manipulation categories detected by pure regex, no LLM
- **GDPR lawful basis classifier** — maps stated data purposes to GDPR Article 6 bases
- **Hallucination verification** — every LLM claim cross-referenced against original text
- **Compare mode** — side-by-side radar chart comparison of two policies
- **Version history** — tracks grade changes over time for the same domain
- **Industry benchmarks** — positions each policy against Technology, Social Media, E-Commerce averages
- **Export report** — download a full text or HTML report

---

## Architecture

```
                        ┌─────────────────────────────────────────┐
                        │              User Request                │
                        └───────────────────┬─────────────────────┘
                                            │
                        ┌───────────────────▼─────────────────────┐
                        │           Flask Backend (Python)         │
                        │                                          │
                        │  ┌──────────┐    ┌────────────────────┐ │
                        │  │ Scraper  │    │  Paste-text mode   │ │
                        │  │(BS4+lxml)│    │  (skip scraper)    │ │
                        │  └────┬─────┘    └─────────┬──────────┘ │
                        │       └──────────┬──────────┘            │
                        │                  │                        │
                        │  ┌───────────────▼───────────────────┐   │
                        │  │     PolicyPreprocessor (OUR CODE)  │   │
                        │  │  18+ NLP metrics · NLTK · textstat │   │
                        │  │  ReadabilityAnalyzer (from scratch) │   │
                        │  │  JargonDetector (150+ terms)        │   │
                        │  │  DarkPatternDetector (15 categories)│   │
                        │  │  GDPRLawfulBasisClassifier          │   │
                        │  └───────────────┬───────────────────┘   │
                        │                  │ metrics injected       │
                        │  ┌───────────────▼───────────────────┐   │
                        │  │    llm_service.py  ◄── ONLY LLM   │   │
                        │  │    Gemini 1.5 Flash · JSON mode    │   │
                        │  │    Chain-of-thought prompt         │   │
                        │  └───────────────┬───────────────────┘   │
                        │                  │                        │
                        │  ┌───────────────▼───────────────────┐   │
                        │  │   ClaimVerifier  (OUR CODE)        │   │
                        │  │   difflib fuzzy match · citations  │   │
                        │  │   Hallucination detection          │   │
                        │  │   Cross-signal fusion (3 sources)  │   │
                        │  └───────────────┬───────────────────┘   │
                        │                  │                        │
                        │  ┌───────────────▼───────────────────┐   │
                        │  │   GradingEngine  (OUR CODE)        │   │
                        │  │   5-dimension weighted scoring     │   │
                        │  │   Trust Score composite formula    │   │
                        │  └───────────────┬───────────────────┘   │
                        │                  │                        │
                        │        SQLite · SQLAlchemy ORM            │
                        └───────────────────┬─────────────────────┘
                                            │
                        ┌───────────────────▼─────────────────────┐
                        │    Frontend (HTML · CSS · Vanilla JS)    │
                        │  Radar chart (pure Canvas) · Grade card  │
                        │  Dark mode · Paste tabs · Export · Diff  │
                        └─────────────────────────────────────────┘
```

---

## Our Code vs LLM — What We Built

This is the most important table for understanding the project. The LLM does one thing: semantic comprehension of legal text. Everything else is our custom Python.

| Component | Our Code | LLM (Gemini) |
|---|---|---|
| Web scraping + content extraction | ✅ BeautifulSoup + lxml | — |
| Flesch-Kincaid readability (from scratch) | ✅ Custom syllable counter | — |
| 150+ legal jargon detection | ✅ Categorised dictionary | — |
| 15-category dark pattern detector | ✅ Regex + PatternSpec dataclass | — |
| GDPR Article 6 lawful basis classifier | ✅ Keyword mapping | — |
| 18+ NLP preprocessing metrics | ✅ NLTK + textstat | — |
| 5-dimension weighted grading engine | ✅ Custom scoring | — |
| Trust Score composite formula | ✅ Custom formula | — |
| Claim verification + hallucination detection | ✅ difflib fuzzy match | — |
| Cross-signal fusion (3 sources) | ✅ Escalation logic | — |
| Semantic comprehension of legal text | — | ✅ Single prompt |
| Entity extraction (data types, recipients) | — | ✅ JSON mode |
| User rights identification | — | ✅ Structured output |
| Red flag generation | — | ✅ With verification |

**Line count breakdown:** ~3,200 lines of custom Python · ~800 lines of Vanilla JS · ~1,800 lines of CSS · 1 LLM service file (220 lines)

---

## Grading Methodology

Each policy is scored across 5 weighted dimensions:

| Dimension | Weight | What It Measures |
|---|---|---|
| Data Collection Transparency | 25% | Are all data types named? Is purpose stated per type? |
| Sharing & Disclosure | 25% | Are third parties named? Is opt-out available? |
| User Rights | 20% | Access, deletion, portability, correction mechanisms |
| Readability | 15% | Flesch-Kincaid grade, jargon density, section structure |
| Compliance | 15% | GDPR alignment, CCPA alignment, COPPA consideration |

**Grade thresholds:** A ≥ 90 · B ≥ 80 · C ≥ 70 · D ≥ 60 · F < 60

**Trust Score** = `overall_score − dark_pattern_penalty (0–25) + verification_bonus (0–10) − red_flag_penalty (2pts each, capped at 20)`

---

## Prompt Engineering Evolution

The `prompt_experiments.ipynb` notebook documents 5 prompt versions:

| Version | Approach | Key Improvement |
|---|---|---|
| V1 | Naive — "analyse this policy" | Baseline, unstructured output |
| V2 | Structured JSON output | Consistent parseable response |
| V3 | Chain-of-thought | Better reasoning, fewer hallucinations |
| V4 | Few-shot examples | Improved sensitivity classification |
| V5 | Pre-computed metrics injection | LLM focuses only on semantic comprehension |

The production prompt (V5) injects 18+ pre-computed metrics — word count, Flesch score, dark pattern score, jargon density — so Gemini doesn't waste tokens re-counting things our NLP already computed precisely.

---

## Project Structure

```
privacy-policy-grader/
├── Procfile                        # Render/gunicorn start command
├── render.yaml                     # Render deployment config
├── runtime.txt                     # Python 3.11.9
├── prompt_experiments.ipynb        # Prompt engineering evolution (V1→V5)
│
├── backend/
│   ├── app.py                      # Flask app factory + blueprints
│   ├── config.py                   # All configuration + grade thresholds
│   ├── requirements.txt
│   │
│   ├── services/
│   │   ├── scraper.py              # BS4 + lxml policy extraction
│   │   ├── preprocessor.py         # 18+ NLP metrics pipeline
│   │   ├── llm_service.py          # ← ONLY file that calls Gemini
│   │   ├── grading_engine.py       # 5-dimension weighted scoring
│   │   └── verifier.py             # Hallucination detection + cross-signal fusion
│   │
│   ├── analyzers/
│   │   ├── readability.py          # Flesch-Kincaid from scratch
│   │   ├── jargon_detector.py      # 150+ legal terms
│   │   ├── dark_patterns.py        # 15 manipulation categories
│   │   ├── gdpr_classifier.py      # GDPR Article 6 lawful basis mapper
│   │   └── text_metrics.py         # Type-token ratio, sentiment, structure
│   │
│   ├── routes/
│   │   ├── analyze.py              # POST /api/analyze, POST /api/analyze/text, GET /api/history
│   │   ├── compare.py              # POST /api/compare
│   │   ├── benchmarks.py           # GET /api/benchmarks
│   │   └── export.py               # GET /api/export
│   │
│   ├── database/
│   │   ├── models.py               # SQLAlchemy models (Analysis, Benchmark)
│   │   ├── db_manager.py           # CRUD + auto-seed on first boot
│   │   └── seed_data.py            # 12 pre-analysed companies, 4 industries
│   │
│   ├── utils/
│   │   ├── text_cleaner.py         # HTML → clean plain text
│   │   └── url_validator.py        # URL validation + privacy page detection
│   │
│   └── scripts/
│       ├── analyze_batch.py        # CLI: analyse multiple URLs → CSV
│       └── evaluate_ground_truth.py # Compare grades vs expert annotations
│
├── frontend/
│   ├── templates/index.html        # Jinja2 — full single-page UI
│   └── static/
│       ├── css/style.css           # Design system · dark mode · animations
│       └── js/
│           ├── app.js              # Main controller + paste-text + history
│           ├── gradeCard.js        # Animated canvas grade display
│           ├── radarChart.js       # Pure Canvas radar (no Chart.js)
│           ├── redFlags.js         # Severity-ranked expandable flags
│           └── comparison.js       # Side-by-side diff + radar overlay
│
├── samples/
│   ├── google_privacy.txt
│   ├── facebook_privacy.txt
│   ├── amazon_privacy.txt
│   ├── simple_privacy.txt
│   └── ground_truth.csv            # Expert-annotated grades for evaluation
│
└── tests/
    ├── conftest.py                 # Fixtures + mocked LLM
    ├── test_readability.py         # 12 tests
    ├── test_jargon_detector.py     # 9 tests
    ├── test_dark_patterns.py       # 9 tests
    ├── test_grading_engine.py      # 9 tests
    ├── test_verifier.py            # 9 tests
    └── test_routes.py              # 5 endpoint tests
```

---

## API Reference

### `POST /api/analyze`
Analyse a policy by URL.
```json
Request:  { "url": "https://example.com/privacy" }
Response: { "success": true, "data": { "grade": "B", "overall_score": 82.4, "trust_score": 76.1, "dimension_scores": {...}, "red_flags": [...], "metrics": {...} } }
```

### `POST /api/analyze/text`
Analyse pasted policy text directly — no internet required.
```json
Request:  { "text": "Full policy text...", "company_name": "Acme", "source_url": "https://acme.com" }
Response: { "success": true, "data": { ... } }
```

### `POST /api/compare`
Side-by-side comparison of two policies.
```json
Request:  { "url_a": "https://google.com/privacy", "url_b": "https://apple.com/privacy" }
Response: { "success": true, "data": { "policy_a": {...}, "policy_b": {...}, "comparison": {...} } }
```

### `GET /api/history/<domain>`
Version diff tracker — grade changes over time.
```
GET /api/history/google.com
Response: { "versions": [{ "grade": "B", "delta": { "summary": "Grade improved from C to B (+8.3 pts)" } }] }
```

### `GET /api/benchmarks`
Industry average grades and dimension scores.

### `GET /api/export?url=<url>&format=text|html`
Download full analysis report.

---

## Setup — Run Locally

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/privacy-policy-grader.git
cd privacy-policy-grader

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Set up environment
cp backend/.env.example backend/.env
# Edit backend/.env and add your Gemini API key
# Get a free key at: aistudio.google.com

# 4. Run
cd backend
python app.py

# 5. Open http://localhost:5000
```

**Demo mode:** If no API key is set, the app runs in demo mode with realistic mock responses — all custom NLP features still work.

---

## Running Tests

```bash
cd privacy-policy-grader
pytest tests/ -v
```

Expected: 53 tests across 6 files, all passing.

---

## Batch CLI

Analyse multiple URLs from the command line:

```bash
cd backend
python scripts/analyze_batch.py --urls https://google.com/privacy https://apple.com/privacy --output results.csv
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 · Flask 3.0 · SQLAlchemy 2.0 |
| NLP | NLTK 3.8 · textstat 0.7 · custom analyzers |
| Scraping | BeautifulSoup4 · lxml · requests |
| LLM | Google Gemini 1.5 Flash (JSON mode) |
| Database | SQLite (auto-seeded) |
| Frontend | HTML5 · CSS3 · Vanilla JS · Canvas API |
| Testing | pytest 7.4 |
| Deployment | Gunicorn · Render |

---

## Team

**Group 22 — CS5202 GenAI and LLM, Spring 2026**
