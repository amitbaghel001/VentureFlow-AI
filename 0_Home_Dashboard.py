"""
VentureFlow AI — Home Dashboard
Entry point. Shows platform overview and recent activity.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from core.auth import require_login
from core.styles import inject_styles, render_top_nav, page_header
from core.database import get_all_startup_analyses, get_all_memos, get_all_founder_profiles, init_db

st.set_page_config(
    page_title="VentureFlow AI — Workflow Infrastructure",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_styles()
require_login()
render_top_nav()

# ── Init DB ────────────────────────────────────────────────────────────────────
init_db()

# ── Main content ───────────────────────────────────────────────────────────────
page_header("VentureFlow AI", "AI-native workflow infrastructure for modern venture teams.")

hero_col, visual_col = st.columns([3, 2], gap="large")

with hero_col:
    st.markdown(
        """
        <div style="max-width: 620px; margin: 0 0 1rem;">
            <p style="font-size: 1rem; color: #5B5A66; line-height: 1.65; font-weight: 400;">
                AI-native workflow infrastructure for early-stage venture firms.
                Analyze startups, profile founders, generate institutional memos,
                and map competitive markets — in minutes, not days.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Startup Search Input ───────────────────────────────────────────────────
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        st.text_input("Analyze startup", placeholder="Analyze startup or paste company URL", label_visibility="collapsed")
    with col_btn:
        if st.button("Analyze", use_container_width=True):
            st.switch_page("pages/1_Startup_Analyzer.py")

with visual_col:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #6C5CE0 0%, #4A3FB8 100%); border-radius: 12px;
                    padding: 1.4rem 1.5rem; position: relative; min-height: 190px; overflow: hidden;">
            <div style="position:absolute; top:-30px; right:-30px; width:140px; height:140px;
                        border-radius:50%; background:rgba(255,255,255,0.08);"></div>
            <div style="position:absolute; bottom:-40px; left:-20px; width:120px; height:120px;
                        border-radius:50%; background:rgba(255,255,255,0.06);"></div>
            <div style="font-family:'Lora',serif; font-size:1.05rem; line-height:1.5; color:#FFFFFF;
                        font-weight:600; margin-bottom:0.9rem; position:relative;">
                At VentureFlow, we go beyond just dashboards
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:0.5rem; position:relative;">
                <span style="background:rgba(255,255,255,0.16); color:#FFFFFF; font-size:0.7rem;
                            font-weight:600; padding:4px 10px; border-radius:999px;">#grounded_in_data</span>
                <span style="background:rgba(255,255,255,0.16); color:#FFFFFF; font-size:0.7rem;
                            font-weight:600; padding:4px 10px; border-radius:999px;">#multi_llm</span>
                <span style="background:rgba(255,255,255,0.16); color:#FFFFFF; font-size:0.7rem;
                            font-weight:600; padding:4px 10px; border-radius:999px;">#institutional_grade</span>
                <span style="background:rgba(255,255,255,0.16); color:#FFFFFF; font-size:0.7rem;
                            font-weight:600; padding:4px 10px; border-radius:999px;">#real_time_search</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Live Market Signals ────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display: flex; gap: 1.5rem; margin-top: 0.5rem; margin-bottom: 1.4rem; padding: 0.7rem 1.1rem; background: #FFFFFF; border: 1px solid #E4E0D6; border-left: 3px solid #6C5CE0; border-radius: 5px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #5B5A66;">
        <span style="color: #6C5CE0; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;">Live Market Signals</span>
        <span style="color: #2F7D5C; font-weight: 600;">AI Lending ↑</span>
        <span style="color: #2F7D5C; font-weight: 600;">Voice Infrastructure ↑</span>
        <span style="color: #A6791F; font-weight: 600;">Healthcare Ops ↑</span>
        <span style="color: #2F7D5C; font-weight: 600;">SMB Automation ↑</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ── Operational States ─────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
for col, val, label, color in [
    (c1, "Active", "Intelligence Layer", "#2F7D5C"),
    (c2, "12", "Market Signals Indexed", "#6C5CE0"),
    (c3, "5", "Sectors Tracked", "#A6791F"),
    (c4, "Online", "Research Pipeline", "#2F7D5C"),
]:
    with col:
        st.markdown(
            f"""
            <div class="metric-card" style="border-top: 3px solid {color};">
                <div class="metric-value" style="font-size: 1.4rem; color: {color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Feature cards ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em;
                color: #86859A; font-weight: 600; margin: 1.4rem 0 1rem;">
        Intelligence Modules
    </div>
    """,
    unsafe_allow_html=True,
)

def module_card(number: str, label: str, title: str, description: str, color: str, badge_bg: str, icon: str) -> str:
    return f"""
    <div class="glass-card" style="margin-bottom: 0.7rem; border-left: 3px solid {color};
                min-height: 220px; display: flex; flex-direction: column;">
        <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom: 0.8rem;">
            <div style="width:34px; height:34px; border-radius:7px; background:{badge_bg};
                        display:flex; align-items:center; justify-content:center;
                        font-size:1rem; color:{color}; flex-shrink:0;">{icon}</div>
            <div style="font-size: 0.64rem; text-transform: uppercase; letter-spacing: 0.06em;
                        color: {color}; font-weight: 700;">
                Module {number} — {label}
            </div>
        </div>
        <div style="font-family: 'Lora', serif; font-size: 1.15rem; line-height: 1.5; font-weight: 600; color: #1E1B4B; margin-bottom: 0.5rem;">
            {title}
        </div>
        <div style="font-size: 0.82rem; color: #5B5A66; line-height: 1.65; flex-grow: 1;">
            {description}
        </div>
    </div>
    """

modules = [
    ("01", "Startup Intelligence", "Startup Analyzer",
     "Input a startup website or description. The AI extracts the business model, "
     "identifies competitors, evaluates the moat, and generates an investment score "
     "with dimensional breakdown.",
     "#6C5CE0", "#E9E6F9", "&#9679;", "pages/1_Startup_Analyzer.py", "Open Startup Analyzer"),
    ("02", "Founder Intelligence", "Founder Engine",
     "Paste a founder's LinkedIn bio or profile text. Generates domain expertise "
     "scores, execution signal analysis, founder-market fit, risk indicators, "
     "and an overall founder intelligence card.",
     "#2C6E8F", "#DFEBF1", "&#9632;", "pages/2_Founder_Intelligence.py", "Open Founder Engine"),
    ("03", "AI Memo Engine", "Investment Memo Generator",
     "Converts startup analysis, founder profiles, and analyst notes into "
     "a full investment committee memo with bull/bear cases, risk matrix, "
     "and recommendation. Downloadable as PDF.",
     "#2F7D5C", "#DEEFE6", "&#9670;", "pages/3_Memo_Generator.py", "Open Memo Generator"),
    ("04", "Market Graph", "Startup Intelligence Graph",
     "Visualizes the competitive landscape as an interactive network graph. "
     "Maps direct competitors, adjacent companies, and sector clusters "
     "with hover interactions and relationship edges.",
     "#A6791F", "#F3E9D3", "&#9650;", "pages/4_Market_Graph.py", "Open Market Graph"),
]

mod_cols = st.columns(2)
for i, (number, label, title, description, color, badge_bg, icon, page_path, btn_label) in enumerate(modules):
    with mod_cols[i % 2]:
        st.markdown(
            module_card(number, label, title, description, color, badge_bg, icon),
            unsafe_allow_html=True,
        )
        if st.button(btn_label, key=f"open_module_{number}", use_container_width=True):
            st.switch_page(page_path)

# ── Why VentureFlow AI ──────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em;
                color: #86859A; font-weight: 600; margin: 0.4rem 0 1rem;">
        Why VentureFlow AI
    </div>
    """,
    unsafe_allow_html=True,
)

wc1, wc2, wc3 = st.columns(3, gap="medium")

def pillar(icon: str, badge_bg: str, title: str, description: str) -> str:
    return f"""
    <div class="glass-card" style="text-align:left; min-height: 200px; display: flex; flex-direction: column;">
        <div style="width:38px; height:38px; border-radius:8px; background:{badge_bg};
                    display:flex; align-items:center; justify-content:center;
                    font-size:1.1rem; margin-bottom:0.9rem; flex-shrink:0;">{icon}</div>
        <div style="font-family:'Lora',serif; font-size:1.05rem; line-height:1.5; font-weight:600;
                    color:#1E1B4B; margin-bottom:0.5rem;">{title}</div>
        <div style="font-size:0.82rem; color:#5B5A66; line-height:1.6; flex-grow:1;">{description}</div>
    </div>
    """

with wc1:
    st.markdown(
        pillar(
            "&#9679;", "#E9E6F9", "Grounded, Not Guessed",
            "Every analysis is tagged GROUNDED, PARTIAL, or AI-INFERRED based on what live "
            "web search and GitHub data actually verified — not just what the model recalls.",
        ),
        unsafe_allow_html=True,
    )
with wc2:
    st.markdown(
        pillar(
            "&#9632;", "#DFEBF1", "Multi-Provider Intelligence",
            "Switch between Llama 3.3, GPT-4o, and Gemini Flash from one settings panel — "
            "pick the model that fits your budget or reasoning depth per task.",
        ),
        unsafe_allow_html=True,
    )
with wc3:
    st.markdown(
        pillar(
            "&#9650;", "#F3E9D3", "Built for Speed",
            "Startup analysis, founder profiling, memo drafting, and market mapping — "
            "workflows that used to take an analyst days now take minutes.",
        ),
        unsafe_allow_html=True,
    )

# ── System Activity & Recent Analyses ──────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)

col_act, col_recent = st.columns([2, 1])

with col_act:
    st.markdown(
        """
        <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em;
                    color: #86859A; font-weight: 600; margin-bottom: 1rem;">
            System Activity
        </div>
        <div class="glass-card" style="padding: 1rem 1.4rem;">
            <div class="activity-item">
                <div class="activity-dot" style="background:#6C5CE0;"></div>
                <div><div class="activity-content">Founder profile generated: <strong style="color:#1E1B4B">Aman Gupta</strong></div><div class="activity-time">Just now</div></div>
            </div>
            <div class="activity-item">
                <div class="activity-dot" style="background:#6C5CE0;"></div>
                <div><div class="activity-content">Fintech sector scan completed</div><div class="activity-time">2 mins ago</div></div>
            </div>
            <div class="activity-item">
                <div class="activity-dot" style="background:#2F7D5C;"></div>
                <div><div class="activity-content">Investment memo compiled: <strong style="color:#1E1B4B">Zepto</strong></div><div class="activity-time">15 mins ago</div></div>
            </div>
            <div class="activity-item">
                <div class="activity-dot" style="background:#A6791F;"></div>
                <div><div class="activity-content">Competitive map updated: <strong style="color:#1E1B4B">Healthcare Ops</strong></div><div class="activity-time">1 hour ago</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_recent:
    st.markdown(
        """
        <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em;
                    color: #86859A; font-weight: 600; margin-bottom: 1rem;">
            Recent Analyses
        </div>
        <div class="glass-card" style="padding: 1rem 1.4rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #E4E0D6;">
                <span style="color: #1E1B4B; font-weight: 500;">Razorpay</span>
                <span style="color: #5B5A66; font-size: 0.7rem; letter-spacing: 0.05em;">Fintech Infrastructure</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #E4E0D6;">
                <span style="color: #1E1B4B; font-weight: 500;">Zepto</span>
                <span style="color: #5B5A66; font-size: 0.7rem; letter-spacing: 0.05em;">Quick Commerce</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #E4E0D6;">
                <span style="color: #1E1B4B; font-weight: 500;">Sarvam AI</span>
                <span style="color: #5B5A66; font-size: 0.7rem; letter-spacing: 0.05em;">Foundation Models</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.85rem; padding: 0.5rem 0;">
                <span style="color: #1E1B4B; font-weight: 500;">Perfios</span>
                <span style="color: #5B5A66; font-size: 0.7rem; letter-spacing: 0.05em;">Fintech Data</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #E4E0D6;
                font-size: 0.68rem; color: #86859A; text-align: center; letter-spacing: 0.06em;">
        VentureFlow AI · AI-native workflow infrastructure
    </div>
    """,
    unsafe_allow_html=True,
)
