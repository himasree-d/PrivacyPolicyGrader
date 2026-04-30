# Project Roadmap: Privacy Policy Grader

This document tracks the progress from **Milestone 1 (Current)** to the **Final Project Submission**.

##  Milestone 1: Core Foundation (COMPLETED)
- [x] **Modular Pipeline**: Created `scraper`, `preprocess`, `model`, and `grader` modules in `src/`.
- [x] **LLM Integration**: Successfully connected to Gemini 2.0 Flash for semantic analysis.
- [x] **API Layer**: Developed a FastAPI backend (`api.py`) to serve analysis results.
- [x] **Web Interface**: Built a premium React frontend with a polished green/gold aesthetic.
- [x] **Domain Research**: Documented the problem statement and research justification in `domain_note.md`.
- [x] **Environment Setup**: Implemented `.env` support and dependency management.

##  Final Project: Enhanced Robustness & Features (TO-DO)

### 1. Analysis & Accuracy
- [ ] **Multi-Agent Evaluation**: Use a "Critique Agent" to double-check the first agent's findings for hallucinations.
- [ ] **Evidence Mapping**: Link every "Red Flag" directly to a quote from the source text.
- [ ] **Categorized Scoring**: Break down the 0-100 score into sub-categories (Transparency, Retention, Third-Party Sharing).

### 2. Technical Features
- [ ] **PDF Support**: Enable analysis for policies provided as `.pdf` files.
- [ ] **Caching Layer**: Integrate SQLite or a simple JSON cache to avoid re-analyzing the same URL multiple times.
- [ ] **Robust Scraping**: Implement `Playwright` to handle sites that require JavaScript or have bot-protection.

### 3. UI/UX Refinement
- [ ] **History Dashboard**: Allow users to see a list of previously analyzed sites.
- [ ] **Side-by-Side Comparison**: Feature to compare two policies (e.g., WhatsApp vs. Signal).
- [ ] **Export to PDF**: Generate a downloadable, professional PDF report of the analysis.

### 4. Validation
- [ ] **Benchmark Study**: Create a `tests/benchmark/` folder comparing AI grades against human-verified data (e.g., from ToS;DR).
- [ ] **Unit Testing**: Add `pytest` for core utility functions (text cleaning, score calculations).
