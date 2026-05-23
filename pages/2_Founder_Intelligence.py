"""
VentureFlow AI — Page 2: Founder Intelligence
Profile a founder from their LinkedIn bio or raw text.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from core.styles import (
    inject_styles, render_sidebar_logo, page_header,
    score_bar, intel_tag, loading_indicator,
)
from core.ai_engine import analyze_founder
from core.database import save_founder_profile, get_all_founder_profiles

st.set_page_config(
    page_title="Founder Engine — VentureFlow AI",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()
render_sidebar_logo()
page_header("Founder Intelligence Engine", "Multi-signal founder evaluation & risk profiling")

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="font-size: 0.82rem; color: #8892B0; margin-bottom: 1rem; line-height: 1.65;">
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

run_btn = st.button("⬡  Run Founder Intelligence Analysis", use_container_width=False)

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
        try:
            data = analyze_founder(bio_text)
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
        score_color = "#10B981"
    elif overall >= 60:
        score_color = "#F59E0B"
    else:
        score_color = "#F43F5E"

    # ── Header card ────────────────────────────────────────────────────────────
    initial = name[0].upper() if name else "?"
    st.markdown(
        f"""
        <div class="glass-card" style="margin-bottom: 1.5rem;">
            <div class="founder-header">
                <div class="founder-avatar">{initial}</div>
                <div>
                    <div class="founder-name">{name}</div>
                    <div class="founder-role">{title} · {archetype}</div>
                </div>
                <div style="margin-left: auto; text-align: center;">
                    <div style="font-size: 2.8rem; font-weight: 900; color: {score_color};
                                 letter-spacing: -0.04em; line-height: 1;">{overall}</div>
                    <div style="font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.15em;
                                 color: #4A5568;">Overall Score</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
                        <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em;
                                    color: #4F6EF7; font-weight: 600; margin-bottom: 0.3rem;">{label}</div>
                        <div style="font-size: 0.8rem; color: #8892B0; line-height: 1.6;">{note}</div>
                    </div>
                    """
            st.markdown(
                f'<div class="glass-card">'
                f'<div class="intel-section-header">Score Rationale</div>'
                f'<div style="margin-top: 0.8rem;">{notes_html}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with right_col:
        # Strength summary
        strength = data.get("strength_summary", "")
        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div class="intel-section-header">Strength Profile</div>
                <div style="font-size: 0.85rem; color: #8892B0; line-height: 1.7; margin-top: 0.5rem;">
                    {strength}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Career highlights
        highlights = data.get("career_highlights", [])
        if highlights:
            hl_html = "".join(
                f"""
                <div style="display:flex;gap:0.7rem;padding:0.5rem 0;
                            border-bottom:1px solid #1A2744;align-items:flex-start;">
                    <span style="color:#10B981;font-size:0.75rem;margin-top:2px;flex-shrink:0;">▸</span>
                    <span style="font-size:0.8rem;color:#8892B0;line-height:1.55;">{h}</span>
                </div>
                """
                for h in highlights
            )
            st.markdown(
                f"""
                <div class="glass-card" style="margin-bottom: 1rem;">
                    <div class="intel-section-header">Career Highlights</div>
                    <div style="margin-top: 0.4rem;">{hl_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Domain expertise areas
        areas = data.get("domain_expertise_areas", [])
        if areas:
            areas_html = " ".join(intel_tag(a, "neutral") for a in areas)
            st.markdown(
                f"""
                <div class="glass-card" style="margin-bottom: 1rem;">
                    <div class="intel-section-header">Domain Expertise Areas</div>
                    <div style="margin-top: 0.5rem;">{areas_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Risk indicators
        risks = data.get("risk_indicators", [])
        risk_summary = data.get("risk_summary", "")
        if risks or risk_summary:
            risk_tags = " ".join(intel_tag(r[:60], "negative") for r in risks)
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="intel-section-header">Risk Indicators</div>
                    <div style="margin-top: 0.5rem;">{risk_tags}</div>
                    <div style="font-size: 0.8rem; color: #8892B0; line-height: 1.6; margin-top: 0.7rem;">
                        {risk_summary}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Overall assessment
    assessment = data.get("overall_assessment", "")
    if assessment:
        st.markdown("<br>", unsafe_allow_html=True)
        comparable = data.get("comparable_founders", "")
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="intel-section-header">GP-Level Assessment</div>
                <div style="font-size: 0.875rem; color: #8892B0; line-height: 1.75; margin-top: 0.5rem;">
                    {assessment}
                </div>
                {"<div style='margin-top:0.8rem;font-size:0.8rem;color:#4A5568;font-style:italic;'>" + comparable + "</div>" if comparable else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Sidebar: recent profiles ───────────────────────────────────────────────────
recent = get_all_founder_profiles()[:5]
if recent:
    st.sidebar.markdown(
        """
        <div style="padding: 1rem 1.5rem 0.3rem; font-size: 0.65rem; text-transform: uppercase;
                    letter-spacing: 0.18em; color: #4A5568; font-weight: 600; margin-top: 1rem;">
            Recent Profiles
        </div>
        """,
        unsafe_allow_html=True,
    )
    for r in recent:
        sc = int(r["overall_score"] or 0)
        sc_color = "#10B981" if sc >= 80 else "#F59E0B" if sc >= 60 else "#F43F5E"
        st.sidebar.markdown(
            f"""
            <div style="padding: 0.5rem 1.5rem; border-bottom: 1px solid #1A2744;">
                <div style="font-size: 0.78rem; font-weight: 600; color: #F0F4FF;">{r['founder_name']}</div>
                <div style="font-size: 0.68rem; color: #4A5568;">
                    Score: <span style="color:{sc_color};">{sc}/100</span>
                    · {r['founder_archetype'] or '—'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    if st.sidebar.button("Load Last Profile", key="load_last_founder"):
        st.session_state["last_founder_analysis"] = recent[0]["data"]
        st.rerun()
