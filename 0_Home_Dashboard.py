"""
EXIMIUS AI — Home Dashboard
Entry point. Shows platform overview and recent activity.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from core.styles import inject_styles, render_sidebar_logo, page_header
from core.database import get_all_startup_analyses, get_all_memos, get_all_founder_profiles, init_db

st.set_page_config(
    page_title="EXIMIUS AI — Venture Intelligence OS",
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
page_header("EXIMIUS AI", "Venture Intelligence Operating System")

# Hero statement
st.markdown(
    """
    <div style="max-width: 700px; margin: 0 0 2.5rem;">
        <p style="font-size: 1.05rem; color: #8892B0; line-height: 1.75; font-weight: 400;">
            AI-native workflow infrastructure for early-stage venture firms.
            Analyze startups, profile founders, generate institutional memos,
            and map competitive markets — in minutes, not days.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Stats row ──────────────────────────────────────────────────────────────────
startups = get_all_startup_analyses()
founders = get_all_founder_profiles()
memos    = get_all_memos()

c1, c2, c3, c4 = st.columns(4)
for col, val, label in [
    (c1, len(startups), "Startups Analyzed"),
    (c2, len(founders), "Founders Profiled"),
    (c3, len(memos),    "Memos Generated"),
    (c4, len(startups) + len(founders) + len(memos), "Total Analyses"),
]:
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
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
            <div style="margin-top: 0.8rem; font-size: 0.7rem; color: #4A5568;">
                ← Navigate via sidebar
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
            <div style="margin-top: 0.8rem; font-size: 0.7rem; color: #4A5568;">
                ← Navigate via sidebar
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
            <div style="margin-top: 0.8rem; font-size: 0.7rem; color: #4A5568;">
                ← Navigate via sidebar
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
            <div style="margin-top: 0.8rem; font-size: 0.7rem; color: #4A5568;">
                ← Navigate via sidebar
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Recent Activity ────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.18em;
                color: #4A5568; font-weight: 600; margin-bottom: 1rem;">
        Recent Activity
    </div>
    """,
    unsafe_allow_html=True,
)

all_activity = []
for s in startups[:5]:
    all_activity.append({
        "type": "startup",
        "label": f"Startup analyzed: <strong style='color:#F0F4FF'>{s['company_name']}</strong>",
        "sub": f"Score: {int(s['investment_score'] or 0)}/100 · {s['recommendation'] or '—'} · {s['market_category'] or '—'}",
        "time": s["created_at"],
        "color": "#4F6EF7",
    })
for f in founders[:3]:
    all_activity.append({
        "type": "founder",
        "label": f"Founder profiled: <strong style='color:#F0F4FF'>{f['founder_name']}</strong>",
        "sub": f"Score: {int(f['overall_score'] or 0)}/100 · {f['founder_archetype'] or '—'}",
        "time": f["created_at"],
        "color": "#00D4FF",
    })
for m in memos[:3]:
    all_activity.append({
        "type": "memo",
        "label": f"Memo generated: <strong style='color:#F0F4FF'>{m['company_name']}</strong>",
        "sub": f"Recommendation: {m['recommendation'] or '—'}",
        "time": m["created_at"],
        "color": "#10B981",
    })

# Sort by time descending
all_activity.sort(key=lambda x: x["time"], reverse=True)

if all_activity:
    activity_html = ""
    for act in all_activity[:8]:
        activity_html += f"""
        <div class="activity-item">
            <div class="activity-dot" style="background:{act['color']};box-shadow:0 0 6px {act['color']};"></div>
            <div>
                <div class="activity-content">{act['label']}</div>
                <div class="activity-content" style="margin-top:2px;color:#4A5568;">{act['sub']}</div>
                <div class="activity-time">{act['time']}</div>
            </div>
        </div>
        """
    st.markdown(
        f'<div class="glass-card" style="padding: 1rem 1.4rem;">{activity_html}</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 2.5rem;">
            <div style="font-size: 0.82rem; color: #4A5568;">
                No analyses yet. Use the sidebar to run your first startup intelligence workflow.
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
        EXIMIUS AI · Venture Intelligence OS · For Internal Use Only
    </div>
    """,
    unsafe_allow_html=True,
)
