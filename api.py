"""
EXIMIUS AI — FastAPI Backend
Exposes the core AI engine and database as a REST API.
"""

from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.ai_engine import (
    analyze_startup,
    analyze_founder,
    generate_memo,
    generate_graph_data,
    scrape_website
)
from core.database import (
    init_db,
    save_startup_analysis,
    get_all_startup_analyses,
    get_startup_analysis,
    save_founder_profile,
    get_all_founder_profiles,
    save_memo,
    get_all_memos
)
from core.enrichment import (
    fetch_github_profile,
    gather_company_intel,
    gather_founder_intel,
    web_search_enabled,
)

app = FastAPI(
    title="EXIMIUS AI Engine",
    description="Backend API for the EXIMIUS OS Venture Intelligence Platform",
    version="1.0.0"
)

# ─── Initialization ────────────────────────────────────────────────────────────

@app.on_event("startup")
def on_startup():
    init_db()

# ─── Pydantic Models ─────────────────────────────────────────────────────────

class StartupRequest(BaseModel):
    company_name: str
    website_url: Optional[str] = ""
    description: Optional[str] = ""

class FounderRequest(BaseModel):
    bio_text: str
    founder_name: Optional[str] = None
    github_username: Optional[str] = None
    company_name: Optional[str] = None

class MemoRequest(BaseModel):
    startup_data: Dict[str, Any]
    founder_data: Optional[Dict[str, Any]] = None
    analyst_notes: Optional[str] = ""

class GraphRequest(BaseModel):
    company_name: str
    market_category: str
    competitors: List[str]

# ─── Endpoints: Startup Analysis ─────────────────────────────────────────────

@app.post("/api/v1/analyze/startup")
def api_analyze_startup(req: StartupRequest):
    """Run the startup intelligence analysis pipeline and save to DB."""
    website_content = ""
    if req.website_url:
        website_content = scrape_website(req.website_url)

    web_intel = gather_company_intel(req.company_name, req.website_url) if web_search_enabled() else None

    try:
        data = analyze_startup(
            company_name=req.company_name,
            website_url=req.website_url,
            description=req.description,
            website_content=website_content,
            web_intel=web_intel,
        )
        record_id = save_startup_analysis(data, req.website_url)
        return {"status": "success", "record_id": record_id, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/startups")
def api_get_startups():
    """Get all saved startup analyses."""
    return get_all_startup_analyses()

@app.get("/api/v1/startups/{record_id}")
def api_get_startup(record_id: int):
    """Get a specific startup analysis by ID."""
    data = get_startup_analysis(record_id)
    if not data:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return data

# ─── Endpoints: Founder Analysis ─────────────────────────────────────────────

@app.post("/api/v1/analyze/founder")
def api_analyze_founder(req: FounderRequest):
    """Run the founder intelligence pipeline (optionally grounded in a real GitHub
    profile and live web mentions) and save to DB."""
    github_data = fetch_github_profile(req.github_username) if req.github_username else None
    web_intel = None
    if web_search_enabled():
        name_for_search = req.founder_name or req.bio_text.strip().split("\n")[0][:60]
        web_intel = gather_founder_intel(name_for_search, req.company_name or "")

    try:
        data = analyze_founder(req.bio_text, github_data=github_data, web_intel=web_intel)
        record_id = save_founder_profile(data)
        return {"status": "success", "record_id": record_id, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/founders")
def api_get_founders():
    """Get all saved founder profiles."""
    return get_all_founder_profiles()

@app.get("/api/v1/enrichment/github/{username}")
def api_github_profile(username: str):
    """Fetch a real, live public GitHub profile (repos, stars, followers) for a founder."""
    data = fetch_github_profile(username)
    if not data:
        raise HTTPException(status_code=404, detail="GitHub profile not found or unreachable")
    return data

# ─── Endpoints: Memo Generation ──────────────────────────────────────────────

@app.post("/api/v1/generate/memo")
def api_generate_memo(req: MemoRequest):
    """Generate an institutional investment memo and save to DB."""
    try:
        memo = generate_memo(
            startup_data=req.startup_data,
            founder_data=req.founder_data,
            analyst_notes=req.analyst_notes
        )
        record_id = save_memo(memo)
        return {"status": "success", "record_id": record_id, "data": memo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/memos")
def api_get_memos():
    """Get all saved investment memos."""
    return get_all_memos()

# ─── Endpoints: Market Graph ─────────────────────────────────────────────────

@app.post("/api/v1/generate/graph")
def api_generate_graph(req: GraphRequest):
    """Generate structured market graph data, grounded in live search results when available."""
    web_intel = gather_company_intel(req.company_name) if web_search_enabled() else None
    try:
        data = generate_graph_data(
            company_name=req.company_name,
            market_category=req.market_category,
            competitors=req.competitors,
            web_intel=web_intel,
        )
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Endpoints: System Status ─────────────────────────────────────────────────

@app.get("/api/v1/status")
def api_status():
    """Report which enrichment sources are live vs. dormant for this deployment."""
    return {
        "web_search_enabled": web_search_enabled(),
        "github_enrichment_enabled": True,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
