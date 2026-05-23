"""
VentureFlow AI — Page 3: Memo Generator
Compiles existing analyses into a structured investment committee memo.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from datetime import datetime
from core.styles import inject_styles, render_sidebar_logo, page_header, loading_indicator
from core.ai_engine import generate_memo
from core.database import (
    save_memo, get_all_memos,
    get_all_startup_analyses, get_all_founder_profiles,
)
from core.pdf_export import generate_memo_pdf

st.set_page_config(
    page_title="Memo Engine — VentureFlow AI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()
render_sidebar_logo()
page_header("AI Investment Memo Generator", "Institutional-quality IC memos generated from intelligence data")

# ── Source context panel ───────────────────────────────────────────────────────
st.markdown(
    """
    <div style="font-size: 0.82rem; color: #8892B0; margin-bottom: 1.2rem; line-height: 1.65;">
        Pull context from saved analyses below, or enter details manually.
        The engine synthesises all available intelligence into a GP-ready investment memo.
    </div>
    """,
    unsafe_allow_html=True,
)

# Source selectors
col_src1, col_src2 = st.columns(2, gap="large")

startup_analyses = get_all_startup_analyses()
founder_profiles = get_all_founder_profiles()

with col_src1:
    startup_options = {
        f"{s['company_name']} (Score: {int(s['investment_score'] or 0)})": s["data"]
        for s in startup_analyses
    }
    startup_options = {"-- None (enter manually) --": None, **startup_options}
    selected_startup_key = st.selectbox(
        "Load Startup Analysis", options=list(startup_options.keys())
    )
    startup_data = startup_options[selected_startup_key]

with col_src2:
    founder_options = {
        f"{f['founder_name']} (Score: {int(f['overall_score'] or 0)})": f["data"]
        for f in founder_profiles
    }
    founder_options = {"-- None --": None, **founder_options}
    selected_founder_key = st.selectbox(
        "Load Founder Profile", options=list(founder_options.keys())
    )
    founder_data = founder_options[selected_founder_key]

# Manual company name override
if not startup_data:
    company_name_manual = st.text_input(
        "Company Name (manual entry)",
        placeholder="e.g. Substrate AI",
        key="memo_company_manual",
    )
else:
    company_name_manual = startup_data.get("company_name", "")

# Analyst notes
analyst_notes = st.text_area(
    "Analyst Notes (optional)",
    placeholder=(
        "Add any additional context, meeting notes, product impressions, "
        "or specific questions you want the memo to address..."
    ),
    height=120,
)

gen_btn = st.button("⬡  Generate Investment Committee Memo", use_container_width=False)

# ── Generation ─────────────────────────────────────────────────────────────────
if gen_btn:
    if not startup_data and not company_name_manual.strip():
        st.warning("Please select a startup analysis or enter a company name.")
        st.stop()

    # Build synthetic startup data if none selected
    if not startup_data:
        startup_data = {"company_name": company_name_manual}

    loading_placeholder = st.empty()
    loading_placeholder.markdown(
        loading_indicator("Assembling context → drafting sections → generating bull/bear cases..."),
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        try:
            memo = generate_memo(
                startup_data=startup_data,
                founder_data=founder_data,
                analyst_notes=analyst_notes,
            )
        except ValueError as e:
            loading_placeholder.empty()
            st.error(f"API Error: {e}")
            st.stop()
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Memo generation failed: {e}")
            st.stop()

        save_memo(memo)

    loading_placeholder.empty()
    st.session_state["last_memo"] = memo
    st.session_state["last_memo_startup_data"] = startup_data
    st.success("Investment memo generated and saved.")

# ── Render memo ────────────────────────────────────────────────────────────────
memo = st.session_state.get("last_memo")

if memo:
    saved_startup = st.session_state.get("last_memo_startup_data", {})
    company = memo.get("company_name", "Unknown Company")
    rec = (memo.get("investment_recommendation") or "MONITOR").upper()
    date_str = datetime.now().strftime("%B %d, %Y")

    rec_color_map = {"INVEST": "#10B981", "PASS": "#F43F5E", "MONITOR": "#F59E0B"}
    rec_icons     = {"INVEST": "▲ INVEST", "PASS": "▼ PASS", "MONITOR": "◈ MONITOR"}
    rec_color = rec_color_map.get(rec, "#F59E0B")

    # ── Action bar ─────────────────────────────────────────────────────────────
    action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
    with action_col1:
        st.markdown(
            f"""
            <div style="font-size: 1.1rem; font-weight: 700; color: #F0F4FF; margin-top: 0.4rem;">
                {company} — Investment Committee Memo
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_col2:
        st.markdown(
            f"""
            <div style="text-align:center; margin-top:0.3rem;">
                <span style="font-size: 0.9rem; font-weight: 700; color: {rec_color};">
                    {rec_icons.get(rec, rec)}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_col3:
        try:
            pdf_bytes = generate_memo_pdf(memo, saved_startup)
            st.download_button(
                label="⬇ Download PDF",
                data=pdf_bytes,
                file_name=f"EXIMIUS_{company.replace(' ', '_')}_Memo.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as pdf_err:
            st.warning(f"PDF export unavailable: {pdf_err}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Memo body ──────────────────────────────────────────────────────────────
    def memo_section(icon: str, title: str, content: str, color: str = "#4F6EF7") -> str:
        if not content:
            return ""
        return f"""
        <div style="margin-bottom: 1.8rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.2em;
                        color: {color}; font-weight: 600; margin-bottom: 0.5rem;">
                {icon}  {title}
            </div>
            <div style="font-size: 0.875rem; color: #8892B0; line-height: 1.8;">
                {content}
            </div>
        </div>
        """

    def bullet_list(items: list, color: str = "#4A5568") -> str:
        if not items:
            return ""
        return "".join(
            f'<div style="display:flex;gap:0.6rem;margin-bottom:0.4rem;">'
            f'<span style="color:{color};flex-shrink:0;margin-top:3px;">•</span>'
            f'<span style="font-size:0.86rem;color:#8892B0;line-height:1.65;">{item}</span>'
            f'</div>'
            for item in items
        )

    memo_html = f"""
    <div class="memo-container">

        <div class="memo-header">
            <div style="font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.25em;
                        color: #4A5568; margin-bottom: 0.6rem;">EXIMIUS AI · Investment Intelligence</div>
            <div class="memo-title">{company}</div>
            <div class="memo-subtitle">{memo.get('deal_stage', 'Early Stage')} · {date_str}</div>
            <div style="margin-top: 0.8rem;">
                <span style="font-size: 1rem; font-weight: 700; color: {rec_color};">
                    {rec_icons.get(rec, rec)}
                </span>
            </div>
            {"<div style='font-size:0.75rem;color:#4A5568;margin-top:0.4rem;'>" + memo.get('proposed_check_size','') + "</div>" if memo.get('proposed_check_size') else ""}
        </div>

        <div style="height: 1px; background: #1A2744; margin: 1.5rem 0;"></div>

        {memo_section("⬡", "Executive Summary", memo.get("executive_summary", ""), "#4F6EF7")}
        {memo_section("◈", "Market Opportunity", memo.get("market_opportunity", ""), "#00D4FF")}
        {memo_section("◈", "Product & Technology", memo.get("product_technology", ""), "#00D4FF")}
        {memo_section("◈", "Team Assessment", memo.get("team_assessment", ""), "#4F6EF7")}
        {memo_section("◈", "Traction & Validation", memo.get("traction_metrics", ""), "#4F6EF7")}
        {memo_section("◈", "Competitive Landscape", memo.get("competitive_landscape", ""), "#4F6EF7")}

        <div style="height: 1px; background: #1A2744; margin: 1.5rem 0;"></div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.8rem;">
            <div>
                <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.2em;
                            color: #10B981; font-weight: 600; margin-bottom: 0.5rem;">▲  Bull Case</div>
                <div style="font-size: 0.875rem; color: #8892B0; line-height: 1.8;
                            border-left: 2px solid #10B981; padding-left: 0.8rem;">
                    {memo.get("bull_case", "—")}
                </div>
            </div>
            <div>
                <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.2em;
                            color: #F43F5E; font-weight: 600; margin-bottom: 0.5rem;">▼  Bear Case</div>
                <div style="font-size: 0.875rem; color: #8892B0; line-height: 1.8;
                            border-left: 2px solid #F43F5E; padding-left: 0.8rem;">
                    {memo.get("bear_case", "—")}
                </div>
            </div>
        </div>

        <div style="margin-bottom: 1.8rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.2em;
                        color: #F43F5E; font-weight: 600; margin-bottom: 0.6rem;">◈  Key Risks</div>
            {bullet_list(memo.get("key_risks", []), "#F43F5E")}
        </div>

        {"<div style='margin-bottom:1.8rem;'><div style='font-size:0.65rem;text-transform:uppercase;letter-spacing:0.2em;color:#10B981;font-weight:600;margin-bottom:0.6rem;'>◈  Risk Mitigants</div>" + bullet_list(memo.get("risk_mitigants",[]),"#10B981") + "</div>" if memo.get("risk_mitigants") else ""}

        <div style="height: 1px; background: #1A2744; margin: 1.5rem 0;"></div>

        <div style="margin-bottom: 1.8rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.2em;
                        color: {rec_color}; font-weight: 600; margin-bottom: 0.5rem;">
                ⬡  Investment Recommendation
            </div>
            <div style="font-size: 1.1rem; font-weight: 700; color: {rec_color}; margin-bottom: 0.6rem;">
                {rec_icons.get(rec, rec)}
            </div>
            <div style="font-size: 0.875rem; color: #8892B0; line-height: 1.8;">
                {memo.get("recommendation_rationale", "")}
            </div>
        </div>

        {"<div style='margin-bottom:1.8rem;'><div style='font-size:0.65rem;text-transform:uppercase;letter-spacing:0.2em;color:#4A5568;font-weight:600;margin-bottom:0.5rem;'>◈  Proposed Terms</div><div style='font-size:0.85rem;color:#8892B0;'>" + memo.get("proposed_terms_notes","") + "</div></div>" if memo.get("proposed_terms_notes") else ""}

        <div style="height: 1px; background: #1A2744; margin: 1.5rem 0;"></div>

        <div style="margin-bottom: 1.5rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.2em;
                        color: #F59E0B; font-weight: 600; margin-bottom: 0.6rem;">◈  Key Diligence Questions</div>
            {"".join(
                f'<div style="display:flex;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid #1A2744;">'
                f'<span style="font-size:0.7rem;color:#4F6EF7;font-family:JetBrains Mono,monospace;flex-shrink:0;margin-top:2px;">Q{i:02d}</span>'
                f'<span style="font-size:0.86rem;color:#8892B0;line-height:1.65;">{q}</span>'
                f'</div>'
                for i, q in enumerate(memo.get("key_diligence_questions",[]), 1)
            )}
        </div>

        <div style="margin-bottom: 1rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.2em;
                        color: #4F6EF7; font-weight: 600; margin-bottom: 0.6rem;">◈  Next Steps</div>
            {bullet_list(memo.get("next_steps",[]), "#4F6EF7")}
        </div>

        <div style="height: 1px; background: #1A2744; margin: 1.5rem 0;"></div>
        <div style="text-align: center; font-size: 0.65rem; color: #4A5568; letter-spacing: 0.1em;">
            EXIMIUS AI · Generated {date_str} · Confidential — Internal Use Only
        </div>
    </div>
    """
    st.markdown(memo_html, unsafe_allow_html=True)

# ── Sidebar: recent memos ──────────────────────────────────────────────────────
recent_memos = get_all_memos()[:5]
if recent_memos:
    st.sidebar.markdown(
        """
        <div style="padding: 1rem 1.5rem 0.3rem; font-size: 0.65rem; text-transform: uppercase;
                    letter-spacing: 0.18em; color: #4A5568; font-weight: 600; margin-top: 1rem;">
            Recent Memos
        </div>
        """,
        unsafe_allow_html=True,
    )
    for m in recent_memos:
        rec_val = (m["recommendation"] or "—").upper()
        rc = {"INVEST": "#10B981", "PASS": "#F43F5E", "MONITOR": "#F59E0B"}.get(rec_val, "#4A5568")
        st.sidebar.markdown(
            f"""
            <div style="padding: 0.5rem 1.5rem; border-bottom: 1px solid #1A2744;">
                <div style="font-size: 0.78rem; font-weight: 600; color: #F0F4FF;">{m['company_name']}</div>
                <div style="font-size: 0.68rem;">
                    <span style="color:{rc};">{rec_val}</span>
                    <span style="color:#4A5568;"> · {m['created_at']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    if st.sidebar.button("Load Last Memo", key="load_last_memo"):
        st.session_state["last_memo"] = recent_memos[0]["data"]
        st.rerun()
