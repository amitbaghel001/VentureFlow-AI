"""
VentureFlow AI — Home Dashboard
Entry point. Shows platform overview and recent activity.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from core.styles import inject_styles, render_sidebar_logo, page_header
from core.database import get_all_startup_analyses, get_all_memos, get_all_founder_profiles, init_db

st.set_page_config(
    page_title="VentureFlow AI — Workflow Infrastructure",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()
render_sidebar_logo()

# ── Sidebar nav hints ──────────────────────────────────────────────────────────
st.sidebar.markdown(
    """
    <div style="padding: 1rem 1.5rem 0.5rem; font-size: 0.65rem; text-transform: uppercase;
                letter-spacing: 0.18em; color: #4A5568; font-weight: 600;">
        Intelligence Modules
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Init DB ────────────────────────────────────────────────────────────────────
init_db()

# ── Main content ───────────────────────────────────────────────────────────────
page_header("VentureFlow AI", "AI-native workflow infrastructure for modern venture teams.")

# Hero statement
st.markdown(
    """
    <div style="max-width: 700px; margin: 0 0 1.5rem;">
        <p style="font-size: 1.05rem; color: #8892B0; line-height: 1.75; font-weight: 400;">
            AI-native workflow infrastructure for early-stage venture firms.
            Analyze startups, profile founders, generate institutional memos,
            and map competitive markets — in minutes, not days.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Startup Search Input ───────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 2])
with col_input:
    st.text_input("Analyze startup", placeholder="[ Analyze startup or paste company URL ]", label_visibility="collapsed")
with col_btn:
    if st.button("Initialize Intelligence", use_container_width=True):
        st.switch_page("pages/1_Startup_Analyzer.py")

# ── Live Market Signals ────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display: flex; gap: 1.5rem; margin-top: 0.5rem; margin-bottom: 2.5rem; padding: 0.8rem 1.2rem; background: rgba(13, 17, 23, 0.6); border: 1px solid rgba(255,255,255,0.05); border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #8892B0;">
        <span style="color: #4A5568; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;">LIVE MARKET SIGNALS</span>
        <span style="color: #10B981;">• AI Lending ↑</span>
        <span style="color: #10B981;">• Voice Infrastructure ↑</span>
        <span style="color: #10B981;">• Healthcare Ops ↑</span>
        <span style="color: #10B981;">• SMB Automation ↑</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ── Operational States ─────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
for col, val, label in [
    (c1, "Active", "Intelligence Layer"),
    (c2, "12", "Market Signals Indexed"),
    (c3, "5", "Sectors Tracked"),
    (c4, "Online", "Research Pipeline"),
]:
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value" style="font-size: 1.4rem;">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Feature cards ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.18em;
                color: #4A5568; font-weight: 600; margin-bottom: 1rem;">
        Intelligence Modules
    </div>
    """,
    unsafe_allow_html=True,
)

fc1, fc2 = st.columns(2)

with fc1:
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 1rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em;
                        color: #4F6EF7; font-weight: 600; margin-bottom: 0.5rem;">
                Module 01 — Startup Intelligence
            </div>
            <div style="font-size: 1rem; font-weight: 700; color: #F0F4FF; margin-bottom: 0.5rem;">
                Startup Analyzer
            </div>
            <div style="font-size: 0.82rem; color: #8892B0; line-height: 1.65;">
                Input a startup website or description. The AI extracts the business model,
                identifies competitors, evaluates the moat, and generates an investment score
                with dimensional breakdown.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with fc2:
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 1rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em;
                        color: #00D4FF; font-weight: 600; margin-bottom: 0.5rem;">
                Module 02 — Founder Intelligence
            </div>
            <div style="font-size: 1rem; font-weight: 700; color: #F0F4FF; margin-bottom: 0.5rem;">
                Founder Engine
            </div>
            <div style="font-size: 0.82rem; color: #8892B0; line-height: 1.65;">
                Paste a founder's LinkedIn bio or profile text. Generates domain expertise
                scores, execution signal analysis, founder-market fit, risk indicators,
                and an overall founder intelligence card.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

fc3, fc4 = st.columns(2)

with fc3:
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 1rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em;
                        color: #10B981; font-weight: 600; margin-bottom: 0.5rem;">
                Module 03 — AI Memo Engine
            </div>
            <div style="font-size: 1rem; font-weight: 700; color: #F0F4FF; margin-bottom: 0.5rem;">
                Investment Memo Generator
            </div>
            <div style="font-size: 0.82rem; color: #8892B0; line-height: 1.65;">
                Converts startup analysis, founder profiles, and analyst notes into
                a full investment committee memo with bull/bear cases, risk matrix,
                and recommendation. Downloadable as PDF.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with fc4:
    st.markdown(
        """
        <div class="glass-card" style="margin-bottom: 1rem;">
            <div style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em;
                        color: #F59E0B; font-weight: 600; margin-bottom: 0.5rem;">
                Module 04 — Market Graph
            </div>
            <div style="font-size: 1rem; font-weight: 700; color: #F0F4FF; margin-bottom: 0.5rem;">
                Startup Intelligence Graph
            </div>
            <div style="font-size: 0.82rem; color: #8892B0; line-height: 1.65;">
                Visualizes the competitive landscape as an interactive network graph.
                Maps direct competitors, adjacent companies, and sector clusters
                with hover interactions and relationship edges.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── System Activity & Recent Analyses ──────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)

col_act, col_recent = st.columns([2, 1])

with col_act:
    st.markdown(
        """
        <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.18em;
                    color: #4A5568; font-weight: 600; margin-bottom: 1rem;">
            System Activity
        </div>
        <div class="glass-card" style="padding: 1rem 1.4rem;">
            <div class="activity-item">
                <div class="activity-dot" style="background:#4F6EF7;box-shadow:0 0 6px #4F6EF7;"></div>
                <div><div class="activity-content">Founder profile generated: <strong style="color:#F0F4FF">Aman Gupta</strong></div><div class="activity-time">Just now</div></div>
            </div>
            <div class="activity-item">
                <div class="activity-dot" style="background:#00D4FF;box-shadow:0 0 6px #00D4FF;"></div>
                <div><div class="activity-content">Fintech sector scan completed</div><div class="activity-time">2 mins ago</div></div>
            </div>
            <div class="activity-item">
                <div class="activity-dot" style="background:#10B981;box-shadow:0 0 6px #10B981;"></div>
                <div><div class="activity-content">Investment memo compiled: <strong style="color:#F0F4FF">Zepto</strong></div><div class="activity-time">15 mins ago</div></div>
            </div>
            <div class="activity-item">
                <div class="activity-dot" style="background:#F59E0B;box-shadow:0 0 6px #F59E0B;"></div>
                <div><div class="activity-content">Competitive map updated: <strong style="color:#F0F4FF">Healthcare Ops</strong></div><div class="activity-time">1 hour ago</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_recent:
    st.markdown(
        """
        <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.18em;
                    color: #4A5568; font-weight: 600; margin-bottom: 1rem;">
            Recent Analyses
        </div>
        <div class="glass-card" style="padding: 1rem 1.4rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #1A2744;">
                <span style="color: #F0F4FF; font-weight: 500;">Razorpay</span>
                <span style="color: #8892B0; font-size: 0.7rem; letter-spacing: 0.05em;">Fintech Infrastructure</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #1A2744;">
                <span style="color: #F0F4FF; font-weight: 500;">Zepto</span>
                <span style="color: #8892B0; font-size: 0.7rem; letter-spacing: 0.05em;">Quick Commerce</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.85rem; padding: 0.5rem 0; border-bottom: 1px solid #1A2744;">
                <span style="color: #F0F4FF; font-weight: 500;">Sarvam AI</span>
                <span style="color: #8892B0; font-size: 0.7rem; letter-spacing: 0.05em;">Foundation Models</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.85rem; padding: 0.5rem 0;">
                <span style="color: #F0F4FF; font-weight: 500;">Perfios</span>
                <span style="color: #8892B0; font-size: 0.7rem; letter-spacing: 0.05em;">Fintech Data</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #1A2744;
                font-size: 0.68rem; color: #4A5568; text-align: center; letter-spacing: 0.06em;">
        VentureFlow AI · AI-native workflow infrastructure
    </div>
    """,
    unsafe_allow_html=True,
)
