"""
VentureFlow AI — Page 1: Startup Analyzer
Input a startup URL or description and get a structured intelligence analysis.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from core.styles import (
    inject_styles, render_sidebar_logo, page_header,
    score_bar, intel_tag, rec_banner, loading_indicator, glass_card,
)
from core.ai_engine import analyze_startup, scrape_website
from core.database import save_startup_analysis, get_all_startup_analyses

st.set_page_config(
    page_title="Startup Analyzer — VentureFlow AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()
render_sidebar_logo()
page_header("Startup Intelligence Analyzer", "AI-powered startup evaluation engine")

# ── Input panel ────────────────────────────────────────────────────────────────
with st.container():
    st.markdown(
        '<div class="glass-card">',
        unsafe_allow_html=True,
    )
    col_a, col_b = st.columns([1, 1], gap="large")
    with col_a:
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g. Substrate AI",
            help="The startup's legal or operating name.",
        )
        website_url = st.text_input(
            "Website URL",
            placeholder="e.g. https://substrate.ai",
            help="We'll scrape this for additional context.",
        )
    with col_b:
        description = st.text_area(
            "Startup Description / Pitch",
            placeholder=(
                "Paste the startup's pitch, description, or any context you have "
                "(e.g. from a deck, email, or notes)..."
            ),
            height=130,
        )
    st.markdown("</div>", unsafe_allow_html=True)

run_btn = st.button("⬡  Run Startup Intelligence Analysis", use_container_width=False)

# ── Analysis execution ─────────────────────────────────────────────────────────
if run_btn:
    if not company_name and not description:
        st.warning("Please enter at least a company name or description.")
        st.stop()

    loading_placeholder = st.empty()
    loading_placeholder.markdown(
        loading_indicator("Intelligence agents initialising... scraping → analysing → scoring"),
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        # Step 1: Scrape website
        website_content = ""
        if website_url:
            with st.spinner("Fetching website content..."):
                website_content = scrape_website(website_url)

        # Step 2: Run AI analysis
        try:
            data = analyze_startup(
                company_name=company_name or "Unknown",
                website_url=website_url,
                description=description,
                website_content=website_content,
            )
        except ValueError as e:
            loading_placeholder.empty()
            st.error(f"API Error: {e}")
            st.stop()
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Analysis failed: {e}")
            st.stop()

        # Step 3: Save to DB
        save_startup_analysis(data, website_url=website_url)

    loading_placeholder.empty()
    st.session_state["last_startup_analysis"] = data
    st.success("Analysis complete.")

# ── Render analysis if available ───────────────────────────────────────────────
data = st.session_state.get("last_startup_analysis")

if data:
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Header row ─────────────────────────────────────────────────────────────
    score = int(data.get("investment_score", 0))
    rec   = (data.get("recommendation") or "monitor").lower()
    rec_color_map = {"invest": "#10B981", "pass": "#F43F5E", "monitor": "#F59E0B"}
    rec_color = rec_color_map.get(rec, "#F59E0B")

    col_name, col_score = st.columns([3, 1])
    with col_name:
        st.markdown(
            f"""
            <div style="margin-bottom: 0.3rem;">
                <span style="font-size: 1.5rem; font-weight: 800; color: #F0F4FF;
                             letter-spacing: -0.03em;">{data.get('company_name', company_name)}</span>
            </div>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.5rem;">
                {intel_tag(data.get('market_category', '—'), 'neutral')}
                {intel_tag(data.get('business_model', '—'), 'neutral')}
                {intel_tag(data.get('stage_fit', '—'), 'warning')}
            </div>
            <div style="font-size: 0.875rem; color: #8892B0; line-height: 1.6; max-width: 700px;">
                {data.get('value_proposition', '')}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_score:
        st.markdown(
            f"""
            <div style="text-align: center; background: var(--bg-card); border: 1px solid #1A2744;
                        border-radius: 10px; padding: 1.2rem;">
                <div style="font-size: 3rem; font-weight: 900; color: #4F6EF7;
                             letter-spacing: -0.04em; line-height: 1;">{score}</div>
                <div style="font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.18em;
                             color: #4A5568; margin-top: 0.3rem;">Investment Score</div>
                <div style="margin-top: 0.8rem; font-size: 0.75rem; font-weight: 700;
                             color: {rec_color}; text-transform: uppercase; letter-spacing: 0.1em;">
                    {rec.upper()}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "Intelligence Overview",
        "Competitive Analysis",
        "Investment Scoring",
        "Diligence Checklist",
    ])

    # ── Tab 1: Overview ────────────────────────────────────────────────────────
    with tab1:
        r1c1, r1c2 = st.columns(2, gap="medium")

        with r1c1:
            # Market & Business
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="intel-section-header">Market & Business Model</div>
                    <div style="font-size: 0.82rem; color: #8892B0; line-height: 1.7; margin-bottom: 0.8rem;">
                        {data.get('market_size_estimate', '—')}
                    </div>
                    <div class="intel-section-header" style="margin-top:1rem;">Target Customer</div>
                    <div style="font-size: 0.82rem; color: #8892B0;">{data.get('target_customer', '—')}</div>
                    <div class="intel-section-header" style="margin-top:1rem;">Technology Assessment</div>
                    <div style="font-size: 0.82rem; color: #8892B0; line-height: 1.65;">
                        {data.get('technology_assessment', '—')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with r1c2:
            # Moat
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="intel-section-header">Moat Analysis</div>
                    <div style="font-size: 0.82rem; color: #8892B0; line-height: 1.7; margin-bottom: 1rem;">
                        {data.get('moat_analysis', '—')}
                    </div>
                    <div class="intel-section-header" style="margin-top:1rem;">Traction Signals</div>
                    <div style="font-size: 0.82rem; color: #8892B0; line-height: 1.65;">
                        {data.get('traction_signals', '—')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Strengths + Risks
        r2c1, r2c2 = st.columns(2, gap="medium")
        with r2c1:
            strengths = data.get("competitive_advantages", [])
            tags_html = " ".join(
                intel_tag(s[:60], "positive") for s in strengths
            )
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="intel-section-header">Competitive Advantages</div>
                    <div style="margin-top: 0.3rem;">{tags_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with r2c2:
            risks = data.get("key_risks", [])
            tags_html = " ".join(
                intel_tag(r[:60], "negative") for r in risks
            )
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="intel-section-header">Key Risk Signals</div>
                    <div style="margin-top: 0.3rem;">{tags_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Recommendation
        rec_text = data.get("recommendation_rationale", "")
        st.markdown(rec_banner(rec_text, rec), unsafe_allow_html=True)

    # ── Tab 2: Competitive ─────────────────────────────────────────────────────
    with tab2:
        competitors = data.get("competitors", [])
        st.markdown(
            '<div class="glass-card"><div class="intel-section-header">Identified Competitors</div>',
            unsafe_allow_html=True,
        )
        if competitors:
            comp_html = ""
            for i, comp in enumerate(competitors):
                comp_html += f"""
                <div class="competitor-row">
                    <div class="competitor-dot"></div>
                    <div class="competitor-name">{comp}</div>
                </div>
                """
            st.markdown(comp_html + "</div>", unsafe_allow_html=True)
        else:
            st.markdown("No competitors identified.</div>", unsafe_allow_html=True)

    # ── Tab 3: Scoring ─────────────────────────────────────────────────────────
    with tab3:
        sb = data.get("score_breakdown", {})
        color_map = [
            ("market_opportunity",    "Market Opportunity",      "indigo"),
            ("product_differentiation","Product Differentiation", "cyan"),
            ("team_signals",          "Team Signals",            "emerald"),
            ("traction_quality",      "Traction Quality",        "amber"),
            ("competitive_positioning","Competitive Positioning", "indigo"),
        ]

        bars_html = "".join(
            score_bar(label, sb.get(key, 50), color)
            for key, label, color in color_map
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="intel-section-header">Investment Score Breakdown</div>
                <div style="margin-top: 1rem;">{bars_html}</div>
                <div style="margin-top: 1.2rem; font-size: 2rem; font-weight: 900;
                             color: #4F6EF7; letter-spacing: -0.04em;">
                    {score}<span style="font-size: 1rem; color: #4A5568; font-weight: 400;">/100</span>
                </div>
                <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.18em;
                             color: #4A5568; margin-top: 0.2rem;">Composite Investment Score</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Tab 4: Diligence ───────────────────────────────────────────────────────
    with tab4:
        questions = data.get("key_diligence_questions", [])
        items_html = "".join(
            f"""<div style="display: flex; gap: 0.8rem; padding: 0.65rem 0; border-bottom: 1px solid #1A2744; align-items: flex-start;">
<span style="font-size: 0.7rem; color: #4F6EF7; font-family: 'JetBrains Mono', monospace; margin-top: 2px; flex-shrink: 0;">Q{i:02d}</span>
<span style="font-size: 0.85rem; color: #8892B0; line-height: 1.6;">{q}</span>
</div>"""
            for i, q in enumerate(questions, 1)
        )
        st.markdown(
            f'<div class="glass-card">'
            f'<div class="intel-section-header">Diligence Question Queue</div>'
            f'<div style="margin-top: 0.5rem;">{items_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Recent analyses (sidebar) ──────────────────────────────────────────────────
recent = get_all_startup_analyses()[:5]
if recent:
    st.sidebar.markdown(
        """
        <div style="padding: 1rem 1.5rem 0.3rem; font-size: 0.65rem; text-transform: uppercase;
                    letter-spacing: 0.18em; color: #4A5568; font-weight: 600; margin-top: 1rem;">
            Recent Analyses
        </div>
        """,
        unsafe_allow_html=True,
    )
    for r in recent:
        score_val = int(r["investment_score"] or 0)
        rec_val   = (r["recommendation"] or "—").upper()
        colors    = {"INVEST": "#10B981", "PASS": "#F43F5E", "MONITOR": "#F59E0B"}
        c = colors.get(rec_val, "#4A5568")
        st.sidebar.markdown(
            f"""
            <div style="padding: 0.5rem 1.5rem; border-bottom: 1px solid #1A2744;
                        cursor: pointer; transition: background 0.15s;">
                <div style="font-size: 0.78rem; font-weight: 600; color: #F0F4FF;">{r['company_name']}</div>
                <div style="font-size: 0.68rem; color: #4A5568; font-family: 'JetBrains Mono', monospace;">
                    {score_val}/100 · <span style="color:{c};">{rec_val}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    if st.sidebar.button("Load Last Analysis", key="load_last"):
        st.session_state["last_startup_analysis"] = recent[0]["data"]
        st.rerun()
