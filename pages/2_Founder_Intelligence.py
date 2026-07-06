"""
VentureFlow AI — Page 2: Founder Intelligence
Profile a founder from their LinkedIn bio or raw text.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from core.auth import require_login
from core.styles import (
    inject_styles, render_top_nav, page_header,
    score_bar, intel_tag, loading_indicator, data_source_badge,
    esc, flatten_html,
)
from core.ai_engine import analyze_founder
from core.database import save_founder_profile, get_all_founder_profiles
from core.enrichment import fetch_github_profile, gather_founder_intel, web_search_enabled

st.set_page_config(
    page_title="Founder Engine — VentureFlow AI",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()
require_login()
render_top_nav()
page_header("Founder Intelligence Engine", "Multi-signal founder evaluation & risk profiling")

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="font-size: 0.82rem; color: #5B5A66; margin-bottom: 1rem; line-height: 1.65;">
        Paste a founder's LinkedIn bio, profile summary, or any background text.
        The engine extracts domain depth, execution signals, and founder-market fit.
    </div>
    """,
    unsafe_allow_html=True,
)

bio_text = st.text_area(
    "Founder Bio / LinkedIn Profile",
    placeholder=(
        "Paste the founder's LinkedIn bio, Twitter bio, 'About' section, "
        "or any background text here...\n\n"
        "Example:\n"
        "Jane Smith is the CEO and Co-Founder of NeuralStack. Previously, "
        "she spent 6 years at Stripe as a Senior Engineer leading the ML Infrastructure team. "
        "Before that, she received her BS/MS in CS from MIT..."
    ),
    height=220,
    label_visibility="collapsed",
)

# ── Optional real-signal enrichment ─────────────────────────────────────────────
col_name, col_gh, col_co = st.columns(3)
with col_name:
    founder_name_input = st.text_input(
        "Founder Name (optional)",
        placeholder="e.g. Jane Smith",
        help="Improves web search accuracy — without this, name is guessed from the bio's "
             "first sentence, which often fails and returns irrelevant generic results.",
    )
with col_gh:
    github_username = st.text_input(
        "GitHub Username (optional)",
        placeholder="e.g. janesmith",
        help="Pulls real public repos, stars, and followers — verified execution signal.",
    )
with col_co:
    founder_company = st.text_input(
        "Company Name (optional)",
        placeholder="e.g. NeuralStack",
        help="Used to cross-reference the founder's name against live web search results.",
    )

if not web_search_enabled():
    st.caption(
        "⚠ Live web verification is off — add `TAVILY_API_KEY` to `.env` to cross-reference "
        "this founder against real public mentions instead of bio text alone."
    )

run_btn = st.button("Run Founder Intelligence Analysis", use_container_width=False)

# ── Execution ──────────────────────────────────────────────────────────────────
if run_btn:
    if not bio_text.strip():
        st.warning("Please paste a founder bio or profile text.")
        st.stop()

    loading_placeholder = st.empty()
    loading_placeholder.markdown(
        loading_indicator("Analysing domain expertise · execution signals · network quality..."),
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        github_data = fetch_github_profile(github_username) if github_username else None

        # Prefer the explicit name field; only fall back to a heuristic guess from the bio's
        # first sentence if the user didn't provide one (the heuristic fails silently on bios
        # that don't start with "Name is ...", producing irrelevant generic search results).
        search_name = founder_name_input.strip() or bio_text.strip().split("\n")[0].split(" is ")[0][:60]
        web_intel = None
        if web_search_enabled():
            web_intel = gather_founder_intel(search_name, founder_company)

        try:
            data = analyze_founder(bio_text, github_data=github_data, web_intel=web_intel)
        except ValueError as e:
            loading_placeholder.empty()
            st.error(f"API Error: {e}")
            st.stop()
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Analysis failed: {e}")
            st.stop()

        save_founder_profile(data)

    loading_placeholder.empty()
    st.session_state["last_founder_analysis"] = data
    st.success("Founder intelligence card generated.")

# ── Render ─────────────────────────────────────────────────────────────────────
data = st.session_state.get("last_founder_analysis")

if data:
    st.markdown("<br>", unsafe_allow_html=True)

    overall = int(data.get("overall_score", 0))
    name    = data.get("founder_name", "Unknown Founder")
    title   = data.get("inferred_title", "Founder")
    archetype = data.get("founder_archetype", "—")

    # Score colour
    if overall >= 80:
        score_color = "#2F7D5C"
    elif overall >= 60:
        score_color = "#A6791F"
    else:
        score_color = "#B23B3B"

    # ── Header card ────────────────────────────────────────────────────────────
    initial = name[0].upper() if name else "?"
    st.markdown(
        flatten_html(f"""
        <div class="glass-card" style="margin-bottom: 1.5rem;">
            <div class="founder-header">
                <div class="founder-avatar">{esc(initial)}</div>
                <div>
                    <div class="founder-name">{esc(name)}</div>
                    <div class="founder-role">{esc(title)} · {esc(archetype)}</div>
                </div>
                <div style="margin-left: auto; text-align: center;">
                    <div style="font-size: 2.8rem; font-weight: 900; color: {score_color};
                                 letter-spacing: -0.04em; line-height: 1;">{overall}</div>
                    <div style="font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.06em;
                                 color: #86859A;">Overall Score</div>
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown(data_source_badge(data.get("_meta", {})), unsafe_allow_html=True)

    # ── Two-column layout ──────────────────────────────────────────────────────
    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        # Signal scores
        dims = [
            ("domain_expertise_score",    "Domain Expertise",     "indigo"),
            ("execution_signal_score",    "Execution Signal",     "cyan"),
            ("founder_market_fit_score",  "Founder-Market Fit",   "emerald"),
            ("network_quality_score",     "Network Quality",      "amber"),
            ("leadership_profile_score",  "Leadership Profile",   "indigo"),
        ]
        bars_html = "".join(
            score_bar(label, int(data.get(key, 50)), color)
            for key, label, color in dims
        )
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="intel-section-header">Signal Dimension Scores</div>
                <div style="margin-top: 0.8rem;">{bars_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Score notes
        notes = data.get("score_breakdown_notes", {})
        if notes:
            st.markdown("<br>", unsafe_allow_html=True)
            notes_html = ""
            label_map = {
                "domain_expertise": "Domain Expertise",
                "execution_signal": "Execution Signal",
                "founder_market_fit": "Founder-Market Fit",
                "network_quality": "Network Quality",
                "leadership_profile": "Leadership Profile",
            }
            for key, label in label_map.items():
                note = notes.get(key, "")
                if note:
                    notes_html += f"""
                    <div style="margin-bottom: 0.8rem;">
                        <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.06em;
                                    color: #6C5CE0; font-weight: 600; margin-bottom: 0.3rem;">{esc(label)}</div>
                        <div style="font-size: 0.8rem; color: #5B5A66; line-height: 1.6;">{esc(note)}</div>
                    </div>
                    """
            st.markdown(
                flatten_html(
                    f'<div class="glass-card">'
                    f'<div class="intel-section-header">Score Rationale</div>'
                    f'<div style="margin-top: 0.8rem;">{notes_html}</div>'
                    f'</div>'
                ),
                unsafe_allow_html=True,
            )

    with right_col:
        # Strength summary
        strength = data.get("strength_summary", "")
        st.markdown(
            flatten_html(f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div class="intel-section-header">Strength Profile</div>
                <div style="font-size: 0.85rem; color: #5B5A66; line-height: 1.7; margin-top: 0.5rem;">
                    {esc(strength)}
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

        # Career highlights
        highlights = data.get("career_highlights", [])
        if highlights:
            hl_html = "".join(
                f"""
                <div style="display:flex;gap:0.7rem;padding:0.5rem 0;
                            border-bottom:1px solid #E4E0D6;align-items:flex-start;">
                    <span style="color:#2F7D5C;font-size:0.75rem;margin-top:2px;flex-shrink:0;">▸</span>
                    <span style="font-size:0.8rem;color:#5B5A66;line-height:1.55;">{esc(h)}</span>
                </div>
                """
                for h in highlights
            )
            st.markdown(
                flatten_html(f"""
                <div class="glass-card" style="margin-bottom: 1rem;">
                    <div class="intel-section-header">Career Highlights</div>
                    <div style="margin-top: 0.4rem;">{hl_html}</div>
                </div>
                """),
                unsafe_allow_html=True,
            )

        # Domain expertise areas
        areas = data.get("domain_expertise_areas", [])
        if areas:
            areas_html = " ".join(intel_tag(esc(a), "neutral") for a in areas)
            st.markdown(
                flatten_html(f"""
                <div class="glass-card" style="margin-bottom: 1rem;">
                    <div class="intel-section-header">Domain Expertise Areas</div>
                    <div style="margin-top: 0.5rem;">{areas_html}</div>
                </div>
                """),
                unsafe_allow_html=True,
            )

        # Risk indicators
        risks = data.get("risk_indicators", [])
        risk_summary = data.get("risk_summary", "")
        if risks or risk_summary:
            risk_tags = " ".join(intel_tag(esc(r[:60]), "negative") for r in risks)
            st.markdown(
                flatten_html(f"""
                <div class="glass-card">
                    <div class="intel-section-header">Risk Indicators</div>
                    <div style="margin-top: 0.5rem;">{risk_tags}</div>
                    <div style="font-size: 0.8rem; color: #5B5A66; line-height: 1.6; margin-top: 0.7rem;">
                        {esc(risk_summary)}
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )

    # Overall assessment
    assessment = data.get("overall_assessment", "")
    if assessment:
        st.markdown("<br>", unsafe_allow_html=True)
        comparable = data.get("comparable_founders", "")
        st.markdown(
            flatten_html(f"""
            <div class="glass-card">
                <div class="intel-section-header">GP-Level Assessment</div>
                <div style="font-size: 0.875rem; color: #5B5A66; line-height: 1.75; margin-top: 0.5rem;">
                    {esc(assessment)}
                </div>
                {"<div style='margin-top:0.8rem;font-size:0.8rem;color:#86859A;font-style:italic;'>" + esc(comparable) + "</div>" if comparable else ""}
            </div>
            """),
            unsafe_allow_html=True,
        )

# ── Recent profiles ──────────────────────────────────────────────────────────────
recent = get_all_founder_profiles()[:5]
if recent:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Recent Profiles", expanded=False):
        for r in recent:
            sc = int(r["overall_score"] or 0)
            sc_color = "#2F7D5C" if sc >= 80 else "#A6791F" if sc >= 60 else "#B23B3B"
            st.markdown(
                f"""
                <div style="padding: 0.5rem 0; border-bottom: 1px solid #E4E0D6;">
                    <div style="font-size: 0.78rem; font-weight: 600; color: #1E1B4B;">{esc(r['founder_name'])}</div>
                    <div style="font-size: 0.68rem; color: #86859A;">
                        Score: <span style="color:{sc_color};">{sc}/100</span>
                        · {esc(r['founder_archetype'] or '—')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if st.button("Load Last Profile", key="load_last_founder"):
            st.session_state["last_founder_analysis"] = recent[0]["data"]
            st.rerun()
