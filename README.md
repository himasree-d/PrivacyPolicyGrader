# Privacy Policy Grader

A GenAI-powered pipeline that scrapes, analyzes, and grades website privacy policies using LLMs (Gemini).

---

##  Full Application Run (Frontend + Backend)

To run the complete application with the web interface, follow these steps in two separate terminal windows:

### Window 1: Backend API
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Gemini API Key to .env
echo "GOOGLE_API_KEY=your_key_here" > .env

# 3. Start the API server
python api.py
```
*API will be live at http://localhost:8000*

### Window 2: Frontend UI
```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Start the web app
npm run dev
```
*Web app will be live at http://localhost:5173*

---

## 🛠️ Project Structure

```
privacy-policy-grader/
├── src/
│   ├── scraper.py        # URL scraping via BeautifulSoup
│   ├── preprocess.py     # Text cleaning and chunking
│   ├── model.py          # Gemini LLM extraction
│   └── grader.py         # Rule-based risk grading
├── data/                 # Preprocessed text chunks (JSON)
├── results/              # Graded output JSONs
├── notebooks/
│   └── eda_analysis.ipynb # Exploratory analysis notebook
├── frontend/             # React UI
│   ├── index.html        # Entry point
│   ├── vite.config.js    # Vite configuration
│   └── src/
│       ├── App.jsx
│       └── main.jsx
├── pipeline.py           # END-TO-END RUNNABLE SCRIPT
├── api.py                # FastAPI server
├── requirements.txt
└── .env                  # Environment variables (API Key)
```

---

## 📝 Pipeline Overview

```
URL / Text
    ↓
[scraper.py]      → raw HTML text
    ↓
[preprocess.py]   → cleaned + chunked text → saved to data/
    ↓
[model.py]        → Gemini LLM extracts structured JSON
    ↓
[grader.py]       → risk score + letter grade (A–F)
    ↓
results/*.json
```

**Grading scale:**

| Score  | Grade | Meaning                    |
|--------|-------|----------------------------|
| 0–20   | A     | Excellent privacy practices |
| 21–40  | B     | Generally good             |
| 41–60  | C     | Moderate concerns          |
| 61–80  | D     | Significant issues         |
| 81–100 | F     | Major privacy violations   |

---

## 🎓 Academic Requirements

| Requirement | Status | Evidence |
|---|---|---|
| Domain research note | ✅ | `domain_note.md` |
| Runnable pipeline script | ✅ | `python pipeline.py` |
| Data download script | ✅ | `python download_data.py` |
| Data loaded (data/ folder) | ✅ | `data/*_data.json` |
| Model with preliminary results | ✅ | `results/*.json` |
| Notebook | ✅ | `notebooks/eda_analysis.ipynb` |
| Clean repo (no node_modules) | ✅ | `.gitignore` excludes it |

---

## 💡 Troubleshooting
- **404 Page Not Found**: Ensure you are running `npm run dev` inside the `frontend/` directory. I have added `index.html` and `vite.config.js` to fix this issue.
- **API Key Error**: Make sure your `.env` file contains a valid `GOOGLE_API_KEY`.
- **Backend Connection**: The frontend expects the backend to be running on port 8000. If you change the backend port, update `App.jsx`.

---

## 🔗 Credits
Built with Gemini 2.0 Flash and React.
