# 🔍 Privacy Policy Grader

> **AI + Custom NLP** — Grade any privacy policy for transparency, readability, user rights, and legal compliance in seconds.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Note on Stack Evolution**: The project stack evolved from the initially planned FastAPI+React to Flask+Jinja2. This decision was made to maximize Python-dominant backend engineering and simplify the architecture for a robust, production-ready demonstration.

---

## 🗂️ Table of Contents
1. [Overview](#overview)
2. [OUR CODE vs LLM — Contribution Breakdown](#our-code-vs-llm)
3. [Architecture](#architecture)
4. [Grading Methodology](#grading-methodology)
5. [API Documentation](#api-documentation)
6. [Getting Started](#getting-started)
7. [Project Structure](#project-structure)
8. [Running Tests](#running-tests)

---

## Overview

Privacy Policy Grader analyses privacy policies on **5 dimensions**, computing a weighted 0–100 score and letter grade (A–F). It combines a **custom NLP pipeline** (readability formulas, legal jargon detection, dark pattern recognition, fuzzy-match claim verification) with **Google Gemini** for semantic text comprehension.

### Key Features
- 🔬 **18+ NLP metrics** computed via pure Python — no LLM
- 🕷️ **Smart web scraper** with multi-strategy policy URL discovery and Selenium fallback
- 🤖 **Single-file LLM boundary** — Gemini is called in exactly one file (`llm_service.py`)
- 🛡️ **Hallucination guard** — `ClaimVerifier` fuzzy-matches every AI claim against source text
- 📊 **Pure Canvas charts** — radar chart and grade arc, no Chart.js dependency
- 🏭 **Industry benchmarks** — seeded data for 12 companies across 4 industries
- ⚖️ **Side-by-side comparison** — compare any two policies
- ⚡ **Demo Mode** — fully functional without a Gemini API key

---

## OUR CODE vs LLM

This table explicitly separates what our team engineered versus what the LLM provides. This is the core value proposition for a GenAI course project.

| Component | OUR CODE (Python) | LLM (Gemini) |
|:----------|:------------------|:-------------|
| **Readability** | Flesch-Kincaid, SMOG, ARI, Coleman-Liau — implemented from scratch with custom syllable counter | ❌ Not used |
| **Jargon Detection** | Dictionary of 150+ legal/privacy/technical terms with regex word-boundary matching and density calculation | ❌ Not used |
| **Dark Pattern Detection** | 15+ categories with `@dataclass PatternSpec`, severity scores, regex rules | ❌ Not used |
| **Text Metrics** | VADER sentiment, passive voice %, type-token ratio, clause completeness, paragraph structure | ❌ Not used |
| **Web Scraping** | BeautifulSoup4 boilerplate removal (nav/cookie banners/ads), section splitting by headings, Selenium fallback | ❌ Not used |
| **URL Discovery** | Multi-strategy: path heuristics → homepage crawling → robots.txt scanning | ❌ Not used |
| **Grading Engine** | 5-dimension weighted scoring, 9 sub-scorers per dimension, grade boundary mapping | ❌ Not used |
| **Claim Verification** | `difflib.SequenceMatcher` fuzzy matching with confidence scores and hallucination flagging | ❌ Not used |
| **Database** | SQLAlchemy ORM, CRUD, benchmarks, grade distribution, export | ❌ Not used |
| **Frontend Charts** | Pure HTML5 Canvas radar chart + animated arc grade card | ❌ Not used |
| **Data Extraction** | ❌ Not used | ✅ Identifies specific data types, sharing recipients, user rights, and red flags from raw text |
| **Plain-English Summary** | ❌ Not used | ✅ Synthesises a human-readable verdict paragraph |

---

## Architecture

```
URL Input
    │
    ▼
┌─────────────────┐
│  Scraper Service │  ← OUR CODE: BeautifulSoup + Selenium + URL heuristics
│  scraper.py      │
└────────┬────────┘
         │ clean policy text + sections
         ▼
┌─────────────────────┐
│  Preprocessor        │  ← OUR CODE: 18+ NLP metrics (NLTK, textstat, regex)
│  preprocessor.py     │
└────────┬────────────┘
         │ metrics dict
         ├──────────────────────────────────────────────┐
         ▼                                              ▼
┌──────────────────┐                        ┌──────────────────────┐
│  LLM Service      │  ← GEMINI API ONLY    │  Grading Engine       │  ← OUR CODE
│  llm_service.py   │                        │  grading_engine.py    │
└────────┬─────────┘                        └──────────┬───────────┘
         │ structured findings                          │ dimension scores
         │                                              │
         ▼                                              │
┌──────────────────┐                                   │
│  Claim Verifier   │  ← OUR CODE: difflib fuzzy match  │
│  verifier.py      │                                   │
└────────┬─────────┘                                   │
         │ verification confidence                       │
         └──────────────────┬────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Database        │  ← OUR CODE: SQLAlchemy ORM
                   │  db_manager.py   │
                   └────────┬────────┘
                            │ JSON response
                            ▼
                   ┌─────────────────┐
                   │  Flask API       │  ← OUR CODE: /api/analyze
                   │  routes/         │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Frontend        │  ← OUR CODE: Canvas charts, vanilla JS
                   │  static/ + tmpl/ │
                   └─────────────────┘
```

---

## Grading Methodology

The overall score is a **weighted average** of 5 dimensions:

| Dimension | Weight | What We Measure |
|:----------|:------:|:----------------|
| Data Collection Transparency | **25%** | Types enumerated, purpose stated, clear categorisation |
| Sharing Disclosure | **25%** | Recipients named, opt-out availability, per-recipient purposes |
| User Rights | **20%** | Access, deletion, portability, correction mechanisms |
| Readability | **15%** | Flesch Reading Ease, section structure, jargon density |
| Compliance | **15%** | GDPR alignment, CCPA alignment, COPPA consideration |

Each dimension has **3 sub-scorers** (0–10 each), averaged to a 0–100 dimension score. The overall score is the weighted sum of all dimension scores.

**Grade Thresholds:**

| Grade | Score Range | Interpretation |
|:-----:|:-----------:|:---------------|
| **A** | 90–100 | Excellent — transparent and user-friendly |
| **B** | 80–89 | Good — meets most modern standards |
| **C** | 70–79 | Adequate — significant room for improvement |
| **D** | 60–69 | Poor — several major issues |
| **F** | 0–59 | Very Poor — fails basic privacy standards |

---

## API Documentation

All endpoints return JSON with envelope `{"success": bool, "data": ..., "error": ...}`.

### `POST /api/analyze`
Analyse a single privacy policy URL.

**Request Body:**
```json
{ "url": "https://example.com/privacy", "force_refresh": false }
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "url": "https://example.com/privacy",
    "company_name": "Example",
    "grade": "B",
    "overall_score": 84.2,
    "dimension_scores": {
      "data_collection_transparency": 88,
      "sharing_disclosure": 82,
      "user_rights": 90,
      "readability": 72,
      "compliance": 88
    },
    "findings": { "data_collected": [...], "data_shared": [...], "user_rights": {...}, "red_flags": [...] },
    "metrics": { "word_count": 3200, "flesch_reading_ease": 42.1, "jargon_density": 8.4, ... },
    "red_flags": [...],
    "dark_pattern_score": 28.5,
    "verification": { "overall_confidence": 0.87, "hallucination_count": 1 },
    "processing_time_seconds": 6.2,
    "cached": false
  }
}
```

**Errors:**
| Code | Reason |
|------|--------|
| 400 | Missing or invalid `url` field |
| 422 | Policy text could not be scraped |
| 429 | Rate limit exceeded (60 req/min) |
| 500 | Internal server error |

---

### `POST /api/compare`
Compare two policies side by side.

**Request Body:**
```json
{ "urls": ["https://a.com/privacy", "https://b.com/privacy"] }
```

**Response:** Returns `policy_a`, `policy_b`, `winner`, `score_delta`, `key_differences[]`, `benchmark_comparison`.

---

### `GET /api/benchmarks`
Returns all industry benchmarks, grade distribution, and recent analyses.

### `GET /api/benchmarks/<industry>`
Returns benchmark data for a specific industry (e.g. `Technology`, `Social Media`).

### `GET /api/health`
Health check. Returns `{"status": "ok", "demo_mode": bool}`.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Google Chrome (for Selenium JS-rendering fallback)

### 1 — Install
```bash
cd privacy-policy-grader/backend
pip install -r requirements.txt
```

### 2 — Configure
```bash
cp .env.example .env
# Add your GEMINI_API_KEY to .env
# Leave it blank to run in Demo Mode (mock responses, no API needed)
```

### 3 — Download NLTK data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

### 4 — Seed the database
```bash
python -c "from database.seed_data import seed_all; seed_all()"
```

### 5 — Run
```bash
python app.py
# Open http://localhost:5000
```

### Offline Demo (no internet required)
Use the sample files in `samples/`:
```bash
# Paste the content of samples/simple_privacy.txt into the text area
# or use the URL: file:///path/to/samples/google_privacy.txt
```

---

## Project Structure

```
privacy-policy-grader/
├── backend/
│   ├── app.py                  # Flask app factory (CORS, blueprints, middleware)
│   ├── config.py               # Config from .env (grading weights, demo mode)
│   ├── requirements.txt
│   ├── .env.example
│   ├── analyzers/              # OUR CODE — pure NLP, zero LLM
│   │   ├── readability.py      # 5 readability formulas from scratch
│   │   ├── jargon_detector.py  # 150+ term dictionary, density analysis
│   │   ├── dark_patterns.py    # 15+ regex pattern categories
│   │   └── text_metrics.py     # VADER sentiment, clause checks, structure score
│   ├── database/
│   │   ├── models.py           # SQLAlchemy ORM (Analysis, Benchmark)
│   │   ├── db_manager.py       # All CRUD operations
│   │   └── seed_data.py        # 12 companies × 4 industries
│   ├── routes/
│   │   ├── analyze.py          # POST /api/analyze — full pipeline
│   │   ├── compare.py          # POST /api/compare
│   │   └── benchmarks.py       # GET /api/benchmarks
│   ├── services/
│   │   ├── scraper.py          # BeautifulSoup + Selenium scraper
│   │   ├── preprocessor.py     # 18+ NLP metrics aggregator
│   │   ├── llm_service.py      # ← ONLY file that calls Gemini
│   │   ├── grading_engine.py   # Weighted 5-dimension scoring
│   │   └── verifier.py         # difflib fuzzy-match hallucination guard
│   └── utils/
│       ├── text_cleaner.py     # HTML → clean text pipeline
│       └── url_validator.py    # URL validation + policy discovery
├── frontend/
│   ├── templates/index.html    # Jinja2 single-page app
│   └── static/
│       ├── css/style.css       # Full dark-mode design system
│       └── js/
│           ├── app.js          # Main controller
│           ├── radarChart.js   # Pure Canvas radar chart
│           ├── gradeCard.js    # Animated arc grade display
│           ├── redFlags.js     # Accordion renderer
│           └── comparison.js   # Side-by-side comparison renderer
├── tests/
│   ├── test_readability.py
│   ├── test_jargon_detector.py
│   ├── test_dark_patterns.py
│   ├── test_grading_engine.py
│   └── test_verifier.py
├── samples/
│   ├── google_privacy.txt
│   ├── facebook_privacy.txt
│   ├── amazon_privacy.txt
│   └── simple_privacy.txt      # Model A-grade policy for comparison
├── prompt_experiments.ipynb    # Prompt engineering iteration (V1→V5)
└── README.md
```

---

## Running Tests

```bash
cd backend
pytest ../tests/ -v
```

Expected output: **23 tests passed** across 5 test files covering all custom NLP modules.

### Test Coverage Summary
| File | Tests | What's Covered |
|------|------:|----------------|
| `test_readability.py` | 8 | FRE, FKGL, syllable counter, all 5 formulas |
| `test_jargon_detector.py` | 9 | Dictionary matching, density, per-section |
| `test_dark_patterns.py` | 9 | 15+ pattern categories, severity, structural checks |
| `test_grading_engine.py` | 9 | Grade boundaries, dimension scores, edge cases |
| `test_verifier.py` | 9 | Fuzzy matching, hallucination detection, confidence |
