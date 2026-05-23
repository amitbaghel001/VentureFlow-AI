"""
VentureFlow AI — Global Styles & CSS Injection
Cinematic dark-mode institutional UI.
"""

import streamlit as st


VENTUREFLOW_CSS = """
<style>
/* ═══════════════════════════════════════════════
   FONTS & ROOT VARIABLES
═══════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-void:        #050810;
    --bg-surface:     #0D1117;
    --bg-card:        #0F1629;
    --bg-elevated:    #111827;
    --border-subtle:  #1A2744;
    --border-active:  #2D3A6B;
    --accent-indigo:  #4F6EF7;
    --accent-cyan:    #00D4FF;
    --accent-emerald: #10B981;
    --accent-amber:   #F59E0B;
    --accent-rose:    #F43F5E;
    --text-primary:   #F0F4FF;
    --text-secondary: #8892B0;
    --text-tertiary:  #4A5568;
    --glow-indigo:    rgba(79, 110, 247, 0.15);
    --glow-cyan:      rgba(0, 212, 255, 0.12);
}

/* ═══════════════════════════════════════════════
   BASE RESET
═══════════════════════════════════════════════ */
html, body, .stApp {
    background-color: var(--bg-void) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                radial-gradient(ellipse at 20% 0%, rgba(79,110,247,0.04) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 10%, rgba(0,212,255,0.03) 0%, transparent 50%),
                var(--bg-void) !important;
    background-size: 32px 32px, 32px 32px, 100% 100%, 100% 100%, 100% 100%;
}

/* Hide Streamlit branding */
#MainMenu, footer {visibility: hidden;}
header {background: transparent !important;}
.stDeployButton, .stAppDeployButton, [data-testid="stToolbar"] {display: none !important;}

/* ═══════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border-subtle) !important;
    padding-top: 0 !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

.sidebar-logo {
    padding: 1.2rem 1.5rem 1rem;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 0.5rem;
}

.sidebar-logo .logo-text {
    font-size: 1.3rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-logo .logo-sub {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-tertiary);
    margin-top: 2px;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0.5rem 1.5rem;
    font-size: 0.72rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-emerald);
    box-shadow: 0 0 6px var(--accent-emerald);
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; box-shadow: 0 0 6px var(--accent-emerald); }
    50% { opacity: 0.6; box-shadow: 0 0 12px var(--accent-emerald); }
}

/* ═══════════════════════════════════════════════
   MAIN CONTENT AREA
═══════════════════════════════════════════════ */
.main .block-container {
    padding: 1.5rem 2.5rem 2.5rem !important;
    max-width: 1200px !important;
}

/* ═══════════════════════════════════════════════
   PAGE HEADER
═══════════════════════════════════════════════ */
.page-header {
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border-subtle);
}

.page-header h1 {
    font-size: 1.65rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin: 0 0 0.3rem;
}

.page-header .page-subtitle {
    font-size: 0.82rem;
    color: var(--text-secondary);
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

.gradient-text {
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ═══════════════════════════════════════════════
   GLASS CARDS
═══════════════════════════════════════════════ */
.glass-card {
    background: rgba(13, 17, 23, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 1.5rem 1.7rem;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
    border-color: rgba(79, 110, 247, 0.4);
    box-shadow: 0 8px 32px var(--glow-indigo), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-indigo), transparent);
    opacity: 0.4;
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1.1rem 1.3rem;
    text-align: center;
    transition: all 0.2s ease;
}

.metric-card:hover {
    border-color: var(--border-active);
    transform: translateY(-1px);
}

.metric-card .metric-value {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--accent-indigo);
    line-height: 1;
}

.metric-card .metric-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

/* ═══════════════════════════════════════════════
   SCORE VISUALIZATION
═══════════════════════════════════════════════ */
.score-ring-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem;
}

.score-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: conic-gradient(
        var(--accent-indigo) calc(var(--score) * 1%),
        var(--border-subtle) 0
    );
    position: relative;
}

.score-badge::after {
    content: attr(data-score);
    position: absolute;
    inset: 6px;
    border-radius: 50%;
    background: var(--bg-void);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text-primary);
}

.score-bar-container {
    margin: 0.5rem 0;
}

.score-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-bottom: 4px;
    font-family: 'JetBrains Mono', monospace;
}

.score-bar-track {
    height: 5px;
    background: var(--border-subtle);
    border-radius: 3px;
    overflow: hidden;
}

.score-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.score-bar-fill.indigo { background: linear-gradient(90deg, #3B4FD4, var(--accent-indigo)); }
.score-bar-fill.cyan   { background: linear-gradient(90deg, #0099CC, var(--accent-cyan)); }
.score-bar-fill.emerald{ background: linear-gradient(90deg, #059669, var(--accent-emerald)); }
.score-bar-fill.amber  { background: linear-gradient(90deg, #D97706, var(--accent-amber)); }
.score-bar-fill.rose   { background: linear-gradient(90deg, #C0102A, var(--accent-rose)); }

/* ═══════════════════════════════════════════════
   INTELLIGENCE SECTIONS
═══════════════════════════════════════════════ */
.intel-section {
    margin: 1rem 0;
}

.intel-section-header {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: var(--accent-indigo);
    font-weight: 600;
    margin-bottom: 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border-subtle);
}

.intel-section p, .intel-section div {
    font-size: 0.875rem;
    line-height: 1.7;
    color: var(--text-secondary);
}

.intel-tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    margin: 2px;
}

.intel-tag.positive { background: rgba(16,185,129,0.12); color: var(--accent-emerald); border: 1px solid rgba(16,185,129,0.25); }
.intel-tag.negative { background: rgba(244,63,94,0.12);  color: var(--accent-rose);    border: 1px solid rgba(244,63,94,0.25); }
.intel-tag.neutral  { background: rgba(79,110,247,0.1);  color: var(--accent-indigo);  border: 1px solid rgba(79,110,247,0.2); }
.intel-tag.warning  { background: rgba(245,158,11,0.1);  color: var(--accent-amber);   border: 1px solid rgba(245,158,11,0.2); }

/* ═══════════════════════════════════════════════
   RECOMMENDATION BANNER
═══════════════════════════════════════════════ */
.rec-banner {
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin: 1rem 0;
    border-left: 3px solid;
    font-size: 0.875rem;
    line-height: 1.6;
}

.rec-banner.invest {
    background: rgba(16,185,129,0.08);
    border-color: var(--accent-emerald);
    color: var(--accent-emerald);
}

.rec-banner.pass {
    background: rgba(244,63,94,0.08);
    border-color: var(--accent-rose);
    color: var(--accent-rose);
}

.rec-banner.monitor {
    background: rgba(245,158,11,0.08);
    border-color: var(--accent-amber);
    color: var(--accent-amber);
}

/* ═══════════════════════════════════════════════
   STREAMLIT COMPONENT OVERRIDES
═══════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(13, 17, 23, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-size: 0.875rem !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(79, 110, 247, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(79, 110, 247, 0.15), inset 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}

.stButton > button {
    background: linear-gradient(180deg, #5C7CFA 0%, #4F6EF7 100%) !important;
    color: white !important;
    border: 1px solid #3B4FD4 !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.5rem 1.4rem !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 2px 10px rgba(79,110,247,0.3), inset 0 1px 0 rgba(255,255,255,0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(79,110,247,0.4), inset 0 1px 0 rgba(255,255,255,0.3) !important;
    background: linear-gradient(180deg, #6C8CFF 0%, #5C7CFA 100%) !important;
}

.stButton > button[kind="secondary"] {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-active) !important;
    color: var(--text-secondary) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, var(--accent-emerald), #059669) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
}

/* Spinner / loading */
.stSpinner > div {
    border-top-color: var(--accent-indigo) !important;
}

/* Divider */
hr {
    border-color: var(--border-subtle) !important;
    margin: 1.5rem 0 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-surface) !important;
    border-radius: 8px 8px 0 0 !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--text-secondary) !important;
    padding: 0.7rem 1.2rem !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent-indigo) !important;
    background: transparent !important;
    border-bottom: 2px solid var(--accent-indigo) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
}

/* Alerts */
.stAlert {
    border-radius: 6px !important;
    border: 1px solid var(--border-subtle) !important;
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-indigo), var(--accent-cyan)) !important;
    border-radius: 999px !important;
}

/* Sidebar nav links */
.stSidebarNav a {
    font-size: 0.82rem !important;
    color: var(--text-secondary) !important;
    font-weight: 400 !important;
    padding: 0.4rem 1rem !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.02em !important;
}

.stSidebarNav a:hover {
    color: var(--text-primary) !important;
    background: rgba(79,110,247,0.08) !important;
}

.stSidebarNav a[aria-current="page"] {
    color: var(--accent-indigo) !important;
    background: rgba(79,110,247,0.1) !important;
    font-weight: 500 !important;
}

/* ═══════════════════════════════════════════════
   LOADING ANIMATION
═══════════════════════════════════════════════ */
.ai-loading {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 1rem 1.4rem;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    margin: 1rem 0;
}

.ai-loading .dots {
    display: flex;
    gap: 4px;
}

.ai-loading .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-indigo);
    animation: bounce 1.4s infinite ease-in-out both;
}

.ai-loading .dot:nth-child(2) { animation-delay: 0.16s; }
.ai-loading .dot:nth-child(3) { animation-delay: 0.32s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

.ai-loading .loading-text {
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
}

/* ═══════════════════════════════════════════════
   MEMO FORMATTING
═══════════════════════════════════════════════ */
.memo-container {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 2rem 2.5rem;
    font-size: 0.875rem;
    line-height: 1.8;
    color: var(--text-secondary);
}

.memo-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-subtle);
}

.memo-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.memo-subtitle {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-tertiary);
    margin-top: 0.4rem;
}

.memo-section-title {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--accent-indigo);
    font-weight: 600;
    margin: 1.5rem 0 0.6rem;
}

.memo-section-content {
    font-size: 0.875rem;
    line-height: 1.75;
    color: var(--text-secondary);
}

/* ═══════════════════════════════════════════════
   FOUNDER CARD
═══════════════════════════════════════════════ */
.founder-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.2rem;
}

.founder-avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-indigo), var(--accent-cyan));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    font-weight: 700;
    color: white;
    flex-shrink: 0;
}

.founder-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
}

.founder-role {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 2px;
}

/* ═══════════════════════════════════════════════
   ACTIVITY FEED
═══════════════════════════════════════════════ */
.activity-item {
    display: flex;
    gap: 1rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--border-subtle);
    align-items: flex-start;
}

.activity-item:last-child { border-bottom: none; }

.activity-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
    animation: activity-pulse 2s infinite ease-in-out alternate;
}

@keyframes activity-pulse {
    0% { opacity: 0.6; filter: drop-shadow(0 0 2px currentColor); }
    100% { opacity: 1; filter: drop-shadow(0 0 12px currentColor); }
}

.activity-content {
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

.activity-time {
    font-size: 0.68rem;
    color: var(--text-tertiary);
    margin-top: 2px;
    font-family: 'JetBrains Mono', monospace;
}

/* ═══════════════════════════════════════════════
   CALLOUT BOXES
═══════════════════════════════════════════════ */
.callout {
    border-left: 2px solid;
    padding: 0.8rem 1.2rem;
    border-radius: 0 6px 6px 0;
    margin: 0.75rem 0;
    font-size: 0.82rem;
    line-height: 1.6;
}

.callout.bull {
    border-color: var(--accent-emerald);
    background: rgba(16,185,129,0.06);
    color: rgba(16,185,129,0.9);
}

.callout.bear {
    border-color: var(--accent-rose);
    background: rgba(244,63,94,0.06);
    color: rgba(244,63,94,0.9);
}

.callout.info {
    border-color: var(--accent-indigo);
    background: rgba(79,110,247,0.06);
    color: rgba(79,110,247,0.9);
}

/* ═══════════════════════════════════════════════
   NUMBER HIGHLIGHTS
═══════════════════════════════════════════════ */
.stat-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin: 1rem 0;
}

.stat-item {
    flex: 1;
    min-width: 120px;
    background: var(--bg-elevated);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.9rem 1rem;
    text-align: center;
}

.stat-item .stat-number {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--accent-cyan);
    letter-spacing: -0.03em;
    font-family: 'JetBrains Mono', monospace;
}

.stat-item .stat-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-tertiary);
    margin-top: 3px;
}

/* ═══════════════════════════════════════════════
   COMPETITOR LIST
═══════════════════════════════════════════════ */
.competitor-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border-subtle);
    font-size: 0.82rem;
}

.competitor-row:last-child { border-bottom: none; }

.competitor-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent-rose);
    flex-shrink: 0;
}

.competitor-name {
    color: var(--text-primary);
    font-weight: 500;
}
</style>
"""


def inject_styles() -> None:
    """Inject the global VentureFlow stylesheet into Streamlit."""
    st.markdown(VENTUREFLOW_CSS, unsafe_allow_html=True)


def render_sidebar_logo() -> None:
    """Render the VentureFlow logo in the sidebar."""
    st.sidebar.markdown(
        """
        <div class="sidebar-logo">
            <div class="logo-text">VentureFlow AI</div>
            <div class="logo-sub">Workflow Infrastructure</div>
        </div>
        <div class="status-indicator">
            <div class="status-dot"></div>
            Intelligence Layer Active
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    """Render a standardised page header."""
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{title}</h1>
            <div class="page-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score_bar(label: str, value: int, color: str = "indigo") -> str:
    """Return an HTML score bar element."""
    return f"""
    <div class="score-bar-container">
        <div class="score-bar-label">
            <span>{label}</span>
            <span style="color:var(--text-primary);font-weight:600;">{value}</span>
        </div>
        <div class="score-bar-track">
            <div class="score-bar-fill {color}" style="width:{value}%"></div>
        </div>
    </div>
    """


def intel_tag(text: str, kind: str = "neutral") -> str:
    """Return an HTML intelligence tag."""
    return f'<span class="intel-tag {kind}">{text}</span>'


def rec_banner(text: str, kind: str = "monitor") -> str:
    """Return an HTML recommendation banner."""
    icons = {"invest": "▲ INVEST", "pass": "▼ PASS", "monitor": "◈ MONITOR"}
    label = icons.get(kind, "◈ MONITOR")
    return f"""
    <div class="rec-banner {kind}">
        <strong>{label}</strong> — {text}
    </div>
    """


def loading_indicator(message: str = "AI Intelligence Engine Processing...") -> str:
    """Return an HTML animated loading indicator."""
    return f"""
    <div class="ai-loading">
        <div class="dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
        <div class="loading-text">{message}</div>
    </div>
    """


def glass_card(content: str) -> str:
    """Wrap content in a glass card."""
    return f'<div class="glass-card">{content}</div>'


def intel_section(header: str, content: str) -> str:
    """Return a formatted intelligence section."""
    return f"""
    <div class="intel-section">
        <div class="intel-section-header">{header}</div>
        <div class="intel-section p" style="font-size:0.875rem;line-height:1.7;color:var(--text-secondary);">{content}</div>
    </div>
    """
