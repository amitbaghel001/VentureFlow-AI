"""
EXIMIUS AI — External Enrichment Layer
Grounds AI analysis in real, sourced data: live web search (Tavily) and
public developer signal (GitHub). Falls back gracefully when keys are absent —
callers always get a well-formed dict back, never an exception.
"""

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_URL = "https://api.tavily.com/search"
GITHUB_API = "https://api.github.com"


def web_search_enabled() -> bool:
    return bool(os.getenv("TAVILY_API_KEY"))


def tavily_search(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Run a live web search via Tavily. Returns [] if no key configured or on failure."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return []
    try:
        resp = requests.post(
            TAVILY_URL,
            json={
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": max_results,
                "include_answer": False,
            },
            timeout=15,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": (r.get("content") or "")[:800],
            }
            for r in results
        ]
    except Exception:
        return []


def gather_company_intel(company_name: str, website_url: str = "") -> dict[str, Any]:
    """Live web search for funding, news, and real competitors — sourced, not inferred."""
    if not company_name:
        return {"web_results": [], "sources": [], "used_web_search": False}

    queries = [
        f"{company_name} startup funding round investors",
        f"{company_name} competitors alternatives",
    ]
    all_results: list[dict[str, Any]] = []
    for q in queries:
        all_results.extend(tavily_search(q, max_results=4))

    seen: set[str] = set()
    deduped = []
    for r in all_results:
        if r["url"] and r["url"] not in seen:
            seen.add(r["url"])
            deduped.append(r)

    return {
        "web_results": deduped,
        "sources": [r["url"] for r in deduped],
        "used_web_search": len(deduped) > 0,
    }


def _is_relevant(result: dict[str, Any], name_tokens: list[str]) -> bool:
    """A search result only counts as grounding if the founder's actual name
    appears in it — otherwise a generic query returns generic top-ranked pages
    (forum threads, listicles) that have nothing to do with this specific person."""
    haystack = f"{result.get('title', '')} {result.get('content', '')}".lower()
    return any(tok in haystack for tok in name_tokens if len(tok) > 2)


def gather_founder_intel(founder_name: str, company_name: str = "") -> dict[str, Any]:
    """Live web search for public mentions of a founder, cross-referenced with their company.
    Results are filtered to those that actually mention the founder's name — an unfiltered
    search on a generic/short name returns irrelevant generic pages, which is worse than no
    grounding at all because it would be labeled as if it were verified signal."""
    founder_name = (founder_name or "").strip()
    if not founder_name or founder_name.lower() == "unknown":
        return {"web_results": [], "sources": [], "used_web_search": False}

    query = f'"{founder_name}" {company_name} founder'.strip()
    raw_results = tavily_search(query, max_results=6)

    name_tokens = [t.lower() for t in founder_name.split()]
    relevant = [r for r in raw_results if _is_relevant(r, name_tokens)]

    return {
        "web_results": relevant,
        "sources": [r["url"] for r in relevant],
        "used_web_search": len(relevant) > 0,
    }


def fetch_github_profile(username: str) -> dict[str, Any] | None:
    """Fetch public GitHub signal for a founder: repos, stars, followers, bio. No key required."""
    username = (username or "").strip().lstrip("@")
    if not username:
        return None
    try:
        user_resp = requests.get(f"{GITHUB_API}/users/{username}", timeout=10)
        if user_resp.status_code != 200:
            return None
        user = user_resp.json()

        repos_resp = requests.get(
            f"{GITHUB_API}/users/{username}/repos",
            params={"sort": "pushed", "per_page": 10},
            timeout=10,
        )
        repos = repos_resp.json() if repos_resp.status_code == 200 else []
        top_repos = sorted(
            (r for r in repos if isinstance(r, dict)),
            key=lambda r: r.get("stargazers_count", 0),
            reverse=True,
        )[:5]

        return {
            "username": user.get("login", username),
            "name": user.get("name", ""),
            "bio": user.get("bio", ""),
            "company": user.get("company", ""),
            "public_repos": user.get("public_repos", 0),
            "followers": user.get("followers", 0),
            "profile_url": user.get("html_url", f"https://github.com/{username}"),
            "top_repos": [
                {
                    "name": r.get("name", ""),
                    "stars": r.get("stargazers_count", 0),
                    "language": r.get("language", ""),
                    "description": r.get("description", ""),
                }
                for r in top_repos
            ],
        }
    except Exception:
        return None


def build_web_context_block(intel: dict[str, Any], label: str = "REAL-TIME WEB INTELLIGENCE") -> str:
    """Format live search results as a citeable context block for the LLM prompt."""
    results = intel.get("web_results", [])
    if not results:
        return ""
    lines = [f"{label} (sourced from live web search — treat as grounded fact, not assumption):"]
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']} — {r['url']}\n{r['content']}")
    return "\n\n".join(lines)


def build_github_context_block(github_data: dict[str, Any] | None) -> str:
    """Format a GitHub profile as a citeable context block for the LLM prompt."""
    if not github_data:
        return ""
    repos_str = ", ".join(
        f"{r['name']} ({r['stars']}★, {r['language'] or 'n/a'})"
        for r in github_data.get("top_repos", [])
    ) or "none public"
    return (
        "GITHUB PROFILE (sourced from live GitHub API — real, verified developer signal):\n"
        f"Username: {github_data.get('username')}\n"
        f"Bio: {github_data.get('bio') or '—'}\n"
        f"Public repos: {github_data.get('public_repos')} · Followers: {github_data.get('followers')}\n"
        f"Top repositories: {repos_str}"
    )


def compute_confidence(*, has_scrape: bool = False, has_web_search: bool = False, has_github: bool = False) -> str:
    """Deterministic confidence label — computed in code from what was actually fetched,
    not self-reported by the LLM (which cannot be trusted to grade its own grounding)."""
    grounded_signals = sum([has_scrape, has_web_search, has_github])
    if grounded_signals >= 2:
        return "grounded"
    if grounded_signals == 1:
        return "partial"
    return "inferred"
