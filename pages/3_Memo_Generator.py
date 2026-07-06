"""
VentureFlow AI — Page 3: Memo Generator
Compiles existing analyses into a structured investment committee memo.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from datetime import datetime
from core.auth import require_login
from core.styles import inject_styles, render_top_nav, page_header, loading_indicator, esc, flatten_html
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
require_login()
render_top_nav()
page_header("AI Investment Memo Generator", "Institutional-quality IC memos generated from intelligence data")

# ── Source context panel ───────────────────────────────────────────────────────
st.markdown(
    """
    <div style="font-size: 0.82rem; color: #5B5A66; margin-bottom: 1.2rem; line-height: 1.65;">
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

gen_btn = st.button("Generate Investment Committee Memo", use_container_width=False)

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

    rec_color_map = {"INVEST": "#2F7D5C", "PASS": "#B23B3B", "MONITOR": "#A6791F"}
    rec_labels    = {"INVEST": "INVEST", "PASS": "PASS", "MONITOR": "MONITOR"}
    rec_color = rec_color_map.get(rec, "#A6791F")

    # ── Action bar ─────────────────────────────────────────────────────────────
    action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
    with action_col1:
        st.markdown(
            f"""
            <div style="font-family: 'Lora', serif; font-size: 1.2rem; line-height: 1.4; font-weight: 600; color: #1E1B4B; margin-top: 0.4rem; padding-top: 0.1rem;">
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
                    {rec_labels.get(rec, rec)}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_col3:
        try:
            pdf_bytes = generate_memo_pdf(memo, saved_startup)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"EXIMIUS_{company.replace(' ', '_')}_Memo.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as pdf_err:
            st.warning(f"PDF export unavailable: {pdf_err}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Memo body ──────────────────────────────────────────────────────────────
    def memo_section(title: str, content: str, color: str = "#86859A") -> str:
        if not content:
            return ""
        return flatten_html(f"""
        <div style="margin-bottom: 1.6rem;">
            <div style="font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em;
                        color: {color}; font-weight: 600; margin-bottom: 0.5rem;">
                {esc(title)}
            </div>
            <div style="font-size: 0.875rem; color: #5B5A66; line-height: 1.8;">
                {esc(content)}
            </div>
        </div>
        """)

    def bullet_list(items: list, color: str = "#86859A") -> str:
        if not items:
            return ""
        return "".join(
            f'<div style="display:flex;gap:0.6rem;margin-bottom:0.4rem;">'
            f'<span style="color:{color};flex-shrink:0;margin-top:3px;">•</span>'
            f'<span style="font-size:0.86rem;color:#5B5A66;line-height:1.65;">{esc(item)}</span>'
            f'</div>'
            for item in items
        )

    memo_html = f"""
    <div class="memo-container">

        <div class="memo-header">
            <div style="font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.06em;
                        color: #86859A; margin-bottom: 0.6rem;">EXIMIUS AI · Investment Intelligence</div>
            <div class="memo-title">{esc(company)}</div>
            <div class="memo-subtitle">{esc(memo.get('deal_stage', 'Early Stage'))} · {date_str}</div>
            <div style="margin-top: 0.8rem;">
                <span style="font-size: 1rem; font-weight: 700; color: {rec_color};">
                    {rec_labels.get(rec, rec)}
                </span>
            </div>
            {"<div style='font-size:0.75rem;color:#86859A;margin-top:0.4rem;'>" + esc(memo.get('proposed_check_size','')) + "</div>" if memo.get('proposed_check_size') else ""}
        </div>

        <div style="height: 1px; background: #E4E0D6; margin: 1.5rem 0;"></div>

        {memo_section("Executive Summary", memo.get("executive_summary", ""))}
        {memo_section("Market Opportunity", memo.get("market_opportunity", ""))}
        {memo_section("Product & Technology", memo.get("product_technology", ""))}
        {memo_section("Team Assessment", memo.get("team_assessment", ""))}
        {memo_section("Traction & Validation", memo.get("traction_metrics", ""))}
        {memo_section("Competitive Landscape", memo.get("competitive_landscape", ""))}

        <div style="height: 1px; background: #E4E0D6; margin: 1.5rem 0;"></div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.6rem;">
            <div>
                <div style="font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em;
                            color: #2F7D5C; font-weight: 600; margin-bottom: 0.5rem;">Bull Case</div>
                <div style="font-size: 0.875rem; color: #5B5A66; line-height: 1.8;
                            border-left: 2px solid #2F7D5C; padding-left: 0.8rem;">
                    {esc(memo.get("bull_case", "—"))}
                </div>
            </div>
            <div>
                <div style="font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em;
                            color: #B23B3B; font-weight: 600; margin-bottom: 0.5rem;">Bear Case</div>
                <div style="font-size: 0.875rem; color: #5B5A66; line-height: 1.8;
                            border-left: 2px solid #B23B3B; padding-left: 0.8rem;">
                    {esc(memo.get("bear_case", "—"))}
                </div>
            </div>
        </div>

        <div style="margin-bottom: 1.6rem;">
            <div style="font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em;
                        color: #B23B3B; font-weight: 600; margin-bottom: 0.6rem;">Key Risks</div>
            {bullet_list(memo.get("key_risks", []), "#B23B3B")}
        </div>

        {"<div style='margin-bottom:1.6rem;'><div style='font-size:0.66rem;text-transform:uppercase;letter-spacing:0.06em;color:#2F7D5C;font-weight:600;margin-bottom:0.6rem;'>Risk Mitigants</div>" + flatten_html(bullet_list(memo.get("risk_mitigants",[]),"#2F7D5C")) + "</div>" if memo.get("risk_mitigants") else ""}

        <div style="height: 1px; background: #E4E0D6; margin: 1.5rem 0;"></div>

        <div style="margin-bottom: 1.6rem;">
            <div style="font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em;
                        color: {rec_color}; font-weight: 600; margin-bottom: 0.5rem;">
                Investment Recommendation
            </div>
            <div style="font-size: 1.1rem; font-weight: 700; color: {rec_color}; margin-bottom: 0.6rem;">
                {rec_labels.get(rec, rec)}
            </div>
            <div style="font-size: 0.875rem; color: #5B5A66; line-height: 1.8;">
                {esc(memo.get("recommendation_rationale", ""))}
            </div>
        </div>

        {"<div style='margin-bottom:1.6rem;'><div style='font-size:0.66rem;text-transform:uppercase;letter-spacing:0.06em;color:#86859A;font-weight:600;margin-bottom:0.5rem;'>Proposed Terms</div><div style='font-size:0.85rem;color:#5B5A66;'>" + esc(memo.get("proposed_terms_notes","")) + "</div></div>" if memo.get("proposed_terms_notes") else ""}

        <div style="height: 1px; background: #E4E0D6; margin: 1.5rem 0;"></div>

        <div style="margin-bottom: 1.5rem;">
            <div style="font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em;
                        color: #A6791F; font-weight: 600; margin-bottom: 0.6rem;">Key Diligence Questions</div>
            {"".join(
                f'<div style="display:flex;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid #E4E0D6;">'
                f'<span style="font-size:0.7rem;color:#6C5CE0;font-family:JetBrains Mono,monospace;flex-shrink:0;margin-top:2px;">Q{i:02d}</span>'
                f'<span style="font-size:0.86rem;color:#5B5A66;line-height:1.65;">{esc(q)}</span>'
                f'</div>'
                for i, q in enumerate(memo.get("key_diligence_questions",[]), 1)
            )}
        </div>

        <div style="margin-bottom: 1rem;">
            <div style="font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em;
                        color: #6C5CE0; font-weight: 600; margin-bottom: 0.6rem;">Next Steps</div>
            {bullet_list(memo.get("next_steps",[]), "#6C5CE0")}
        </div>

        <div style="height: 1px; background: #E4E0D6; margin: 1.5rem 0;"></div>
        <div style="text-align: center; font-size: 0.65rem; color: #86859A; letter-spacing: 0.1em;">
            EXIMIUS AI · Generated {date_str} · Confidential — Internal Use Only
        </div>
    </div>
    """
    st.markdown(flatten_html(memo_html), unsafe_allow_html=True)

# ── Recent memos ──────────────────────────────────────────────────────────────────
recent_memos = get_all_memos()[:5]
if recent_memos:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Recent Memos", expanded=False):
        for m in recent_memos:
            rec_val = (m["recommendation"] or "—").upper()
            rc = {"INVEST": "#2F7D5C", "PASS": "#B23B3B", "MONITOR": "#A6791F"}.get(rec_val, "#86859A")
            st.markdown(
                f"""
                <div style="padding: 0.5rem 0; border-bottom: 1px solid #E4E0D6;">
                    <div style="font-size: 0.78rem; font-weight: 600; color: #1E1B4B;">{esc(m['company_name'])}</div>
                    <div style="font-size: 0.68rem;">
                        <span style="color:{rc};">{rec_val}</span>
                        <span style="color:#86859A;"> · {m['created_at']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if st.button("Load Last Memo", key="load_last_memo"):
            st.session_state["last_memo"] = recent_memos[0]["data"]
            st.rerun()
