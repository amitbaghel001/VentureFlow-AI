"""
VentureFlow AI — Core AI Engine
Handles all OpenAI / Gemini / Llama-3 integrations and prompt engineering.
"""

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

from core.config import load_config
from core.enrichment import (
    build_github_context_block,
    build_web_context_block,
    compute_confidence,
)

_client_openai: OpenAI | None = None
_gemini_configured = False


def get_openai_client() -> OpenAI:
    global _client_openai
    if _client_openai is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Please set it in your .env file."
            )
        _client_openai = OpenAI(api_key=api_key)
    return _client_openai

_client_groq: OpenAI | None = None

def get_groq_client() -> OpenAI:
    global _client_groq
    if _client_groq is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your .env file."
            )
        _client_groq = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    return _client_groq


_client_kimchi: OpenAI | None = None

def get_kimchi_client() -> OpenAI:
    global _client_kimchi
    if _client_kimchi is None:
        api_key = os.getenv("KIMCHI_API_KEY")
        if not api_key:
            raise ValueError(
                "KIMCHI_API_KEY not found. Please set it in your .env file."
            )
        _client_kimchi = OpenAI(api_key=api_key, base_url="https://llm.kimchi.dev/openai/v1")
    return _client_kimchi


_client_cerebras: OpenAI | None = None

def get_cerebras_client() -> OpenAI:
    global _client_cerebras
    if _client_cerebras is None:
        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            raise ValueError(
                "CEREBRAS_API_KEY not found. Please set it in your .env file."
            )
        _client_cerebras = OpenAI(api_key=api_key, base_url="https://api.cerebras.ai/v1")
    return _client_cerebras


_client_openrouter: OpenAI | None = None

def get_openrouter_client() -> OpenAI:
    global _client_openrouter
    if _client_openrouter is None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found. Please set it in your .env file."
            )
        _client_openrouter = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    return _client_openrouter


def configure_gemini():
    global _gemini_configured
    if not _gemini_configured:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in your .env file."
            )
        genai.configure(api_key=api_key)
        _gemini_configured = True


# ─── Provider fallback chain ───────────────────────────────────────────────
# If the active/primary provider is rate-limited or out of quota, retry on
# the next entry here (skipping whichever provider was already tried as
# primary) instead of surfacing the error — transparent to the end user, who
# never sees which backend actually answered.
#
# OpenAI (no key funded) and Kimchi (free-tier credits exhausted) are
# commented out rather than deleted — uncomment either the moment they're
# funded again, no other code change needed.
FALLBACK_CHAIN: list[tuple[str, str]] = [
    ("gemini", "gemini-2.5-flash"),
    ("groq", "llama-3.3-70b-versatile"),
    ("cerebras", "gpt-oss-120b"),
    ("openrouter", "openai/gpt-oss-20b:free"),
    # ("kimchi", "kimi-k2.7"),
    # ("openai", "gpt-4o"),
]

_PROVIDER_CLIENTS = {
    "groq": get_groq_client,
    "openai": get_openai_client,
    "kimchi": get_kimchi_client,
    "cerebras": get_cerebras_client,
    "openrouter": get_openrouter_client,
}

_PROVIDER_KEY_ENV = {
    "gemini": "GEMINI_API_KEY",
    "cerebras": "CEREBRAS_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "groq": "GROQ_API_KEY",
    "kimchi": "KIMCHI_API_KEY",
    "openai": "OPENAI_API_KEY",
}


# Single source of truth for every model selectable as the "active_model" in
# the admin System Intelligence page — (provider, model_id, display_label).
# The admin picker imports this directly so the UI can never drift out of
# sync with what's actually wired up in the fallback chain above. Only
# providers with a working, funded key belong here (gpt-4o/kimi-k2.7 are
# intentionally left out — see the commented FALLBACK_CHAIN entries).
MODEL_CATALOG: list[tuple[str, str, str]] = [
    ("gemini", "gemini-2.5-flash", "Gemini 2.5 Flash"),
    ("gemini", "gemini-2.5-pro", "Gemini 2.5 Pro"),
    ("groq", "llama-3.3-70b-versatile", "Llama 3.3 70B (Groq)"),
    ("cerebras", "gpt-oss-120b", "GPT-OSS 120B (Cerebras)"),
    ("openrouter", "openai/gpt-oss-20b:free", "GPT-OSS 20B (OpenRouter)"),
]

_MODEL_TO_PROVIDER = {model_id: provider for provider, model_id, _ in MODEL_CATALOG}


def _provider_of(model_name: str) -> str:
    return _MODEL_TO_PROVIDER.get(model_name, "groq")


def _provider_configured(provider: str) -> bool:
    return bool(os.getenv(_PROVIDER_KEY_ENV[provider]))


def _is_rate_limit_error(exc: Exception) -> bool:
    """True only for quota/rate-limit/out-of-credits errors — everything else
    (bad JSON, missing key, network failure) is a real problem and must
    surface, not be silently swallowed by trying every provider in turn."""
    if isinstance(exc, RateLimitError):
        return True
    try:
        from google.api_core.exceptions import ResourceExhausted
        if isinstance(exc, ResourceExhausted):
            return True
    except ImportError:
        pass
    if getattr(exc, "status_code", None) in (429, 402):
        return True
    msg = str(exc).lower()
    return any(
        kw in msg for kw in
        ("429", "402", "quota", "rate limit", "resource_exhausted", "credit", "exhausted")
    )


def _call_provider(provider: str, model_name: str, system_prompt: str, user_prompt: str) -> dict[str, Any]:
    if provider == "gemini":
        import google.generativeai as genai
        configure_gemini()
        model = genai.GenerativeModel(
            model_name,
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.4,
            )
        )
        response = model.generate_content(user_prompt)
        raw = response.text or "{}"
        return json.loads(raw)

    client = _PROVIDER_CLIENTS[provider]()
    response = client.chat.completions.create(
        model=model_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )
    raw = response.choices[0].message.content or "{}"
    return json.loads(raw)


def _call_llm(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    """Core LLM call with JSON mode enabled. Tries the configured active
    model first, then falls through FALLBACK_CHAIN on rate-limit/quota
    errors only — a misconfiguration or malformed response still raises
    immediately rather than being masked by a silent retry. Providers with
    no API key configured are skipped rather than attempted and failed."""
    config = load_config()
    primary_model = config.get("active_model", "gpt-4o")
    primary_provider = _provider_of(primary_model)

    chain = [(primary_provider, primary_model)] + [
        (p, m) for p, m in FALLBACK_CHAIN if p != primary_provider
    ]
    chain = [(p, m) for p, m in chain if _provider_configured(p)]

    if not chain:
        raise RuntimeError(
            "No AI provider is configured. Set at least one of GEMINI_API_KEY, "
            "GROQ_API_KEY, KIMCHI_API_KEY, or OPENAI_API_KEY."
        )

    last_error: Exception | None = None
    for provider, model_name in chain:
        try:
            return _call_provider(provider, model_name, system_prompt, user_prompt)
        except Exception as e:
            if not _is_rate_limit_error(e):
                raise
            last_error = e
            continue

    raise RuntimeError(
        f"All configured AI providers are currently rate-limited or unavailable. Last error: {last_error}"
    )


# ─── Startup Analysis ────────────────────────────────────────────────────────

STARTUP_SYSTEM_PROMPT = """
You are VentureFlow AI, an institutional-grade venture capital analyst.
Analyze the provided startup description/URL and output a highly structured JSON evaluation.
Your job is to produce a rigorous, institutional-quality analysis of a startup.

You MUST respond with a single valid JSON object matching this exact schema:
{
  "company_name": "string",
  "one_liner": "string — crisp, founder-style pitch in one sentence",
  "market_category": "string — e.g. AI Infrastructure, FinTech, Dev Tools",
  "business_model": "string — e.g. B2B SaaS, Marketplace, API, PLG",
  "target_customer": "string",
  "value_proposition": "string — 2-3 sentences, specific and compelling",
  "stage_fit": "string — e.g. Pre-Seed / Seed / Series A",
  "market_size_estimate": "string — TAM estimate with reasoning",
  "competitors": ["string", "string", "string"],
  "competitive_advantages": ["string", "string"],
  "key_risks": ["string", "string", "string"],
  "moat_analysis": "string — honest assessment of defensibility",
  "traction_signals": "string — what traction signals exist or are missing",
  "technology_assessment": "string — technical differentiation assessment",
  "investment_score": 72,
  "score_breakdown": {
    "market_opportunity": 80,
    "product_differentiation": 70,
    "team_signals": 65,
    "traction_quality": 55,
    "competitive_positioning": 75
  },
  "recommendation": "invest | monitor | pass",
  "recommendation_rationale": "string — 2-3 sentences explaining the recommendation",
  "key_diligence_questions": ["string", "string", "string"]
}

Rules:
- All scores are integers 0–100.
- investment_score is the weighted average of score_breakdown.
- recommendation must be exactly one of: "invest", "monitor", "pass".
- Be analytically rigorous. No generic platitudes.
- If a REAL-TIME WEB INTELLIGENCE block is provided, treat it as sourced fact (cite it implicitly
  in competitors/traction/moat) and prefer it over your own training-data guesses.
- If information is limited and no web intelligence is provided, state your assumptions clearly
  rather than presenting a guess as a verified fact.
- Think like a GP, not a generalist.
"""


def analyze_startup(
    company_name: str,
    website_url: str,
    description: str,
    website_content: str = "",
    web_intel: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the startup intelligence analysis pipeline.

    web_intel (optional): output of core.enrichment.gather_company_intel — live
    search results used to ground competitors/funding/traction in real sources
    instead of relying purely on LLM training-data recall.
    """
    context_parts = [f"Company Name: {company_name}"]
    if website_url:
        context_parts.append(f"Website: {website_url}")
    if description:
        context_parts.append(f"Description provided by user:\n{description}")
    if website_content:
        context_parts.append(
            f"Website content (scraped):\n{website_content[:4000]}"
        )
    web_block = build_web_context_block(web_intel) if web_intel else ""
    if web_block:
        context_parts.append(web_block)

    user_prompt = "\n\n".join(context_parts)
    user_prompt += "\n\nGenerate the complete startup intelligence analysis."

    result = _call_llm(STARTUP_SYSTEM_PROMPT, user_prompt)

    result["_meta"] = {
        "used_website_scrape": bool(website_content),
        "used_web_search": bool(web_intel and web_intel.get("used_web_search")),
        "web_sources": (web_intel or {}).get("sources", []),
        "confidence": compute_confidence(
            has_scrape=bool(website_content),
            has_web_search=bool(web_intel and web_intel.get("used_web_search")),
        ),
    }
    return result


# ─── Founder Analysis ─────────────────────────────────────────────────────────

FOUNDER_SYSTEM_PROMPT = """
You are VentureFlow AI, an institutional-grade venture capital analyst.
Profile the provided founder background (LinkedIn or raw text) and output a highly structured JSON evaluation.

You MUST respond with a single valid JSON object matching this exact schema:
{
  "founder_name": "string — inferred or 'Unknown' if not found",
  "inferred_title": "string — e.g. CEO & Co-Founder",
  "domain_expertise_score": 82,
  "execution_signal_score": 75,
  "founder_market_fit_score": 88,
  "network_quality_score": 65,
  "leadership_profile_score": 70,
  "overall_score": 76,
  "score_breakdown_notes": {
    "domain_expertise": "string — what drives this score",
    "execution_signal": "string — observable execution indicators",
    "founder_market_fit": "string — proximity to the problem",
    "network_quality": "string — investor / peer network assessment",
    "leadership_profile": "string — team-building and leadership signals"
  },
  "career_highlights": ["string", "string", "string"],
  "domain_expertise_areas": ["string", "string"],
  "strength_summary": "string — 2-3 sentences on core strengths",
  "risk_indicators": ["string", "string"],
  "risk_summary": "string — honest risk assessment",
  "founder_archetype": "string — e.g. Technical Builder, Domain Expert, Serial Operator",
  "comparable_founders": "string — 'This founder archetype is similar to...' (optional)",
  "overall_assessment": "string — 3-4 sentences, GP-level synthesis"
}

Rules:
- All scores are integers 0–100.
- overall_score = weighted mean of all five dimension scores.
- Be rigorous. Missing information should lower confidence, not inflate scores.
- If a GITHUB PROFILE or REAL-TIME WEB INTELLIGENCE block is provided, treat it as verified
  signal — real repos/stars/followers are stronger execution evidence than any prose bio claim.
- Identify what you can infer even from limited bio text, but do not present an inference as
  a verified fact when no sourced signal supports it.
"""


def analyze_founder(
    bio_text: str,
    github_data: dict[str, Any] | None = None,
    web_intel: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the founder intelligence analysis pipeline.

    github_data (optional): output of core.enrichment.fetch_github_profile — real,
    verified developer signal (repos, stars, followers).
    web_intel (optional): output of core.enrichment.gather_founder_intel — live
    public web mentions of the founder, cross-referenced with their company.
    """
    parts = [f"Founder background / LinkedIn bio / profile:\n\n{bio_text}"]

    github_block = build_github_context_block(github_data)
    if github_block:
        parts.append(github_block)

    web_block = build_web_context_block(web_intel, label="PUBLIC WEB MENTIONS") if web_intel else ""
    if web_block:
        parts.append(web_block)

    parts.append("Generate the complete founder intelligence card.")
    user_prompt = "\n\n".join(parts)

    result = _call_llm(FOUNDER_SYSTEM_PROMPT, user_prompt)

    result["_meta"] = {
        "used_github": bool(github_data),
        "used_web_search": bool(web_intel and web_intel.get("used_web_search")),
        "web_sources": (web_intel or {}).get("sources", []),
        "github_profile_url": (github_data or {}).get("profile_url"),
        "confidence": compute_confidence(
            has_github=bool(github_data),
            has_web_search=bool(web_intel and web_intel.get("used_web_search")),
        ),
    }
    return result


# ─── Investment Memo ──────────────────────────────────────────────────────────

MEMO_SYSTEM_PROMPT = """
You are VentureFlow AI, generating an institutional investment committee memo.
Synthesize the provided analysis into a polished markdown document.

You MUST respond with a single valid JSON object matching this exact schema:
{
  "company_name": "string",
  "memo_date": "string — today's date",
  "deal_stage": "string",
  "proposed_check_size": "string — e.g. $500K–$1M at Seed",
  "executive_summary": "string — 3-4 sentences. The complete argument for why this deal matters.",
  "market_opportunity": "string — 3-5 sentences. TAM/SAM/SOM framing with specifics.",
  "product_technology": "string — 3-4 sentences. Technical moat and product differentiation.",
  "team_assessment": "string — 3-4 sentences. Founder-market fit, domain depth, gaps.",
  "traction_metrics": "string — 3-4 sentences. What has been validated, what hasn't.",
  "competitive_landscape": "string — 3-4 sentences. Where they sit vs. competitors.",
  "bull_case": "string — 3-4 sentences. The best realistic outcome and why it's plausible.",
  "bear_case": "string — 3-4 sentences. The honest downside scenario.",
  "key_risks": ["string", "string", "string"],
  "risk_mitigants": ["string", "string"],
  "investment_recommendation": "string — one of: INVEST / MONITOR / PASS",
  "recommendation_rationale": "string — 3-5 sentences. The core investment argument or pass rationale.",
  "proposed_terms_notes": "string — e.g. Target: $X at $YM post, lead or follow, pro-rata rights",
  "key_diligence_questions": ["string", "string", "string", "string"],
  "next_steps": ["string", "string", "string"]
}

Rules:
- Sound like a GP. Not a consultant. Not a student.
- Avoid generic statements. Every claim must be specific.
- Bull and bear cases must be genuinely adversarial — not softened.
- investment_recommendation must be exactly: INVEST, MONITOR, or PASS.
"""


def generate_memo(
    startup_data: dict[str, Any],
    founder_data: dict[str, Any] | None = None,
    analyst_notes: str = "",
) -> dict[str, Any]:
    """Generate an institutional investment committee memo."""
    parts = [
        f"STARTUP ANALYSIS DATA:\n{json.dumps(startup_data, indent=2)}",
    ]
    if founder_data:
        parts.append(f"FOUNDER INTELLIGENCE DATA:\n{json.dumps(founder_data, indent=2)}")
    if analyst_notes:
        parts.append(f"ANALYST NOTES:\n{analyst_notes}")

    parts.append("Generate the complete investment committee memo.")
    user_prompt = "\n\n".join(parts)

    return _call_llm(MEMO_SYSTEM_PROMPT, user_prompt)


# ─── Market Graph Data ────────────────────────────────────────────────────────

GRAPH_SYSTEM_PROMPT = """You are a market intelligence analyst at a VC firm.
Generate a competitive market map for a startup as structured data for graph visualization.

You MUST respond with a single valid JSON object matching this schema:
{
  "company_name": "string",
  "sector": "string",
  "competitors": [
    {"name": "string", "type": "direct", "description": "string — one sentence", "stage": "string"},
    {"name": "string", "type": "direct", "description": "string", "stage": "string"},
    {"name": "string", "type": "adjacent", "description": "string", "stage": "string"},
    {"name": "string", "type": "adjacent", "description": "string", "stage": "string"},
    {"name": "string", "type": "adjacent", "description": "string", "stage": "string"}
  ],
  "sector_nodes": [
    {"name": "string", "category": "string"}
  ],
  "market_narrative": "string — 2-3 sentences on the competitive dynamics"
}

Rules:
- Include 2-4 direct competitors and 2-4 adjacent companies.
- Sector nodes are broader market categories or enabling technologies (2-3 nodes).
- Names must be real or realistic company names.
- Types must be exactly: "direct" or "adjacent" or "sector".
- If a REAL-TIME WEB INTELLIGENCE block is provided, prefer the real competitor names it
  surfaces over your own training-data guesses.
"""


def generate_graph_data(
    company_name: str,
    market_category: str,
    competitors: list[str],
    web_intel: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate structured data for the market graph visualization.

    web_intel (optional): output of core.enrichment.gather_company_intel — live
    search results used to ground the competitor map in real sources.
    """
    user_prompt = (
        f"Company: {company_name}\n"
        f"Market Category: {market_category}\n"
        f"Known competitors: {', '.join(competitors) if competitors else 'unknown'}\n\n"
        "Generate the complete market graph data."
    )
    web_block = build_web_context_block(web_intel) if web_intel else ""
    if web_block:
        user_prompt += f"\n\n{web_block}"

    result = _call_llm(GRAPH_SYSTEM_PROMPT, user_prompt)

    result["_meta"] = {
        "used_web_search": bool(web_intel and web_intel.get("used_web_search")),
        "web_sources": (web_intel or {}).get("sources", []),
        "confidence": compute_confidence(
            has_web_search=bool(web_intel and web_intel.get("used_web_search"))
        ),
    }
    return result


# ─── Website Scraper ──────────────────────────────────────────────────────────

def scrape_website(url: str) -> str:
    """Fetch and extract text content from a startup's website."""
    try:
        import trafilatura
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
            return (text or "")[:5000]
    except Exception:
        pass
    return ""
