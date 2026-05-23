# EXIMIUS AI — Venture Intelligence Operating System

> *AI-native workflow infrastructure for early-stage venture capital firms.*

EXIMIUS AI is a production-ready MVP that gives venture analysts and GPs an AI-powered intelligence layer for startup evaluation, founder profiling, market mapping, and investment memo generation.

---

## What It Does

| Module | Description |
|--------|-------------|
| **Startup Analyzer** | Input a startup URL + description → AI extracts business model, competitors, moat, traction, and generates an investment score with dimensional breakdown |
| **Founder Intelligence** | Paste a founder bio → AI scores domain expertise, execution signal, founder-market fit, and generates a risk profile |
| **Memo Generator** | Pulls context from saved analyses → generates a full IC-ready investment memo with bull/bear cases, downloadable as PDF |
| **Market Graph** | Interactive PyVis network graph showing the startup's competitive landscape with colour-coded nodes |

---

## Architecture & Workflow

```mermaid
graph TD
    A[User Input] -->|URL & Pitch| B[Startup Analyzer]
    A -->|LinkedIn Bio| C[Founder Intelligence]
    
    B -- Evaluates Moat & Traction --> D[(Local SQLite Database)]
    C -- Scores Domain & Execution --> D
    
    D --> E[Memo Generator]
    E -- Compiles --> F[Investment Committee PDF]
    
    D --> G[Market Graph]
    G -- Visualizes --> H[Interactive PyVis Network]
    
    I[Settings Panel] -- Routes to --> J((AI Engine))
    J -. Powers .-> B
    J -. Powers .-> C
    J -. Powers .-> E
    J -. Powers .-> G
```

---

## Setup (5 minutes)

### 1. Clone / download the project

```bash
cd path/to/eximius-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
# Copy the template
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-...
```

> **Note:** The app uses `gpt-4o` by default. You can change the model in `core/ai_engine.py` → `_call_llm()`.

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` automatically.

---

## Project Structure

```
eximius-ai/
├── app.py                          # Home dashboard (entry point)
├── pages/
│   ├── 1_Startup_Analyzer.py       # Startup intelligence engine
│   ├── 2_Founder_Intelligence.py   # Founder profiling engine
│   ├── 3_Memo_Generator.py         # Investment memo generator
│   └── 4_Market_Graph.py           # PyVis network graph
├── core/
│   ├── styles.py                   # CSS design system (dark theme)
│   ├── ai_engine.py                # OpenAI API calls + prompts
│   ├── database.py                 # SQLite via SQLAlchemy
│   └── pdf_export.py               # ReportLab PDF generation
├── data/
│   └── eximius.db                  # Auto-created SQLite database
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
├── requirements.txt
├── .env.example
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit + custom CSS (glassmorphism, dark mode) |
| **AI** | OpenAI GPT-4o with JSON mode structured outputs |
| **Database** | SQLite via SQLAlchemy (auto-created) |
| **Graph** | PyVis (force-directed network visualization) |
| **PDF** | ReportLab (institutional memo PDF generation) |
| **Scraping** | Trafilatura (startup website content extraction) |

---

## Demo Workflow

### Recommended demo sequence:

**Step 1 — Startup Analysis**
1. Navigate to **Startup Analyzer**
2. Enter: `Figma` + `https://figma.com` + "collaborative design tool for teams"
3. Click **Run Startup Intelligence Analysis**
4. Review the investment score, competitive analysis, and diligence questions

**Step 2 — Founder Intelligence**
1. Navigate to **Founder Intelligence**
2. Paste a LinkedIn bio (real or synthetic)
3. Review the dimensional score card and risk indicators

**Step 3 — Investment Memo**
1. Navigate to **Memo Generator**
2. Load the Figma analysis from the dropdown
3. Click **Generate Investment Committee Memo**
4. Download the PDF

**Step 4 — Market Graph**
1. Navigate to **Market Graph**
2. Load the Figma analysis
3. Click **Generate Market Intelligence Graph**
4. Interact with the force-directed network

---

## API Key Notes

- Requires an **OpenAI API key** with access to `gpt-4o`
- Estimated cost per full analysis workflow: ~$0.08–$0.15 (gpt-4o pricing)
- You can switch to `gpt-4o-mini` in `core/ai_engine.py` for ~10x lower cost

---

## Customization

### Change the AI model
In `core/ai_engine.py`, modify the `_call_llm` default parameter:
```python
def _call_llm(..., model: str = "gpt-4o-mini"):  # cheaper alternative
```

### Add your firm's scoring rubric
In `core/ai_engine.py`, modify the `STARTUP_SYSTEM_PROMPT` to adjust scoring dimensions and weights.

### Extend the database
In `core/database.py`, add new SQLAlchemy models and CRUD functions following the existing pattern.

---

## Deployment (Free)

The easiest way to deploy EXIMIUS AI to the web is via **Streamlit Community Cloud**:

1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New app**.
3. Fill in the details:
   - **Repository:** `amitbaghel001/VentureFlow-AI`
   - **Branch:** `main`
   - **Main file path:** `0_Home_Dashboard.py`
4. **CRITICAL STEP:** Click on **Advanced settings** (before deploying) and paste your API keys into the "Secrets" box exactly like your `.env` file:
   ```toml
   GROQ_API_KEY="gsk_your_key_here"
   GEMINI_API_KEY="AIzaSy..."
   ```
5. Click **Deploy!** Your app will be live globally in about 2 minutes.

---

## License

Internal use only. Not for distribution.

---

*Built with EXIMIUS AI · Venture Intelligence OS*
