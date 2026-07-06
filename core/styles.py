"""
VentureFlow AI — Global Styles & CSS Injection
Light editorial institutional UI, styled after real-world VC firm sites
(warm cream ground, navy serif headlines, lavender accent, white cards).
"""

import html as _html
import re as _re

import streamlit as st


VENTUREFLOW_CSS = """
<style>
/* ═══════════════════════════════════════════════
   FONTS & ROOT VARIABLES
   Editorial VC-site palette — warm cream ground, deep
   navy text, a single lavender accent, white cards with
   soft shadows. Serif display font for headlines, Inter
   for body/data.
═══════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Lora:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-void:        #F0EEE8;
    --bg-surface:     #F7F5F0;
    --bg-card:        #FFFFFF;
    --bg-elevated:    #F7F5F0;
    --border-subtle:  #E4E0D6;
    --border-active:  #CFC9BA;
    --accent-primary: #6C5CE0;
    --accent-navy:    #1E1B4B;
    --accent-blue:    #6C5CE0;
    --accent-emerald: #2F7D5C;
    --accent-amber:   #A6791F;
    --accent-rose:    #B23B3B;
    --text-primary:   #1E1B4B;
    --text-secondary: #5B5A66;
    --text-tertiary:  #86859A;
    --font-serif:     'Lora', Georgia, serif;
    /* Back-compat aliases so existing markup referencing the old names still resolves */
    --accent-indigo:  var(--accent-blue);
    --accent-cyan:    var(--accent-blue);
    --glow-indigo:    rgba(108, 92, 224, 0.08);
    --glow-cyan:      rgba(108, 92, 224, 0.06);
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
    background: var(--bg-void) !important;
}

/* Hide Streamlit branding. IMPORTANT: do not override the header's height/
   layout via CSS — Streamlit's own JS measures the header's rendered height
   at runtime to position the sidebar (confirmed in the bundled source: the
   sidebar section takes an `adjustTop` prop derived from that measurement).
   Forcing a CSS height here desyncs that measurement and breaks the sidebar
   collapse/expand toggle. Only recolor it; `toolbarMode = "minimal"` in
   .streamlit/config.toml is what actually shrinks it, via a path Streamlit's
   own layout code accounts for. */
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: var(--bg-void) !important;
}
.stDeployButton, .stAppDeployButton {display: none !important;}

/* ═══════════════════════════════════════════════
   SIDEBAR — hidden entirely. Navigation moved to a top
   nav bar (render_top_nav) matching the reference site's
   layout. Hiding via display:none (not width/position
   tricks) so nothing is left in the layout flow to
   desync Streamlit's own measurements — this removes the
   sidebar and its own collapse button together, since the
   button is nested inside it. The separate re-open arrow
   (stExpandSidebarButton) needs its own rule since it
   renders outside the sidebar precisely so it survives
   the sidebar being collapsed/hidden.
═══════════════════════════════════════════════ */
section[data-testid="stSidebar"],
[data-testid="stExpandSidebarButton"] {
    display: none !important;
}

/* ═══════════════════════════════════════════════
   TOP NAV BAR
   Sticky brand + page links, replacing the sidebar as the
   single navigation surface. Lives inside block-container
   (our own territory) as the first rendered element on
   every page — block-container's default top padding
   already clears Streamlit's header, so this never
   overlaps it (confirmed via DevTools: header is 60px,
   block-container padding-top is 96px).
═══════════════════════════════════════════════ */
.st-key-topnav {
    position: sticky;
    top: 0;
    z-index: 50;
    background: var(--bg-void);
    border-bottom: 1px solid var(--border-subtle);
    /* block-container's default top padding is 96px, sized to clear a taller
       header than the 60px one toolbarMode=minimal actually renders (both
       measured directly via DevTools) — leaving a 36px dead gap above this
       bar. Pulling up by exactly that measured difference (not a guess)
       closes the gap while leaving exactly enough room for the header,
       nothing more. Horizontal margin still bleeds the bar edge-to-edge. */
    margin: -2.25rem -2.5rem 1.3rem;
    padding: 0.9rem 2.5rem;
}

.topnav-brand {
    font-family: var(--font-serif);
    font-size: 1.15rem;
    line-height: 1.6;
    font-weight: 600;
    color: var(--text-primary);
    white-space: nowrap;
}

.st-key-topnav [data-testid="stPageLink"] a {
    font-size: 0.82rem !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
}

.st-key-topnav [data-testid="stPageLink"] a:hover {
    color: var(--accent-primary) !important;
}

.st-key-topnav [data-testid="stPageLink"] a[aria-current="page"] {
    color: var(--accent-primary) !important;
    font-weight: 700 !important;
}

/* ═══════════════════════════════════════════════
   MAIN CONTENT AREA
═══════════════════════════════════════════════ */
.main .block-container,
div[data-testid="stMainBlockContainer"] {
    /* Deliberately NOT overriding padding-top: Streamlit sets it to clear the
       height of its own header/toolbar element above. An earlier override here
       (padding: 0.75rem ...) cut that clearance away, which let page content
       slide up underneath the header and get visually clipped by it — this is
       what DevTools showed (stToolbar sitting in front of the page title).
       Only override the sides we actually need to change. */
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1200px !important;
}

/* ═══════════════════════════════════════════════
   PAGE HEADER
═══════════════════════════════════════════════ */
.page-header {
    margin-bottom: 1.1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-subtle);
}

.page-header .page-title {
    display: block;
    font-family: var(--font-serif);
    font-size: 1.65rem;
    line-height: 1.5;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    margin: 0 0 0.3rem;
}

.page-header .page-subtitle {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-weight: 400;
    letter-spacing: 0.01em;
}

.gradient-text {
    color: var(--accent-primary);
}

/* ═══════════════════════════════════════════════
   CARDS
═══════════════════════════════════════════════ */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.3rem 1.5rem;
    position: relative;
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.05), 0 1px 2px rgba(30, 27, 75, 0.04);
    transition: box-shadow 0.15s ease, border-color 0.15s ease;
}

.glass-card:hover {
    border-color: var(--border-active);
    box-shadow: 0 4px 14px rgba(30, 27, 75, 0.09), 0 1px 3px rgba(30, 27, 75, 0.06);
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.05), 0 1px 2px rgba(30, 27, 75, 0.04);
}

.metric-card .metric-value {
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-primary);
    line-height: 1;
}

.metric-card .metric-label {
    font-size: 0.66rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    margin-top: 0.35rem;
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
        var(--accent-primary) calc(var(--score) * 1%),
        var(--border-subtle) 0
    );
    position: relative;
}

.score-badge::after {
    content: attr(data-score);
    position: absolute;
    inset: 6px;
    border-radius: 50%;
    background: var(--bg-card);
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

.score-bar-fill.indigo { background: var(--accent-blue); }
.score-bar-fill.cyan   { background: var(--accent-blue); }
.score-bar-fill.emerald{ background: var(--accent-emerald); }
.score-bar-fill.amber  { background: var(--accent-amber); }
.score-bar-fill.rose   { background: var(--accent-rose); }

/* ═══════════════════════════════════════════════
   INTELLIGENCE SECTIONS
═══════════════════════════════════════════════ */
.intel-section {
    margin: 1rem 0;
}

.intel-section-header {
    font-size: 0.66rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-tertiary);
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
    border-radius: 3px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    margin: 2px;
}

.intel-tag.positive { background: rgba(47,125,92,0.1);  color: var(--accent-emerald); border: 1px solid rgba(47,125,92,0.25); }
.intel-tag.negative { background: rgba(178,59,59,0.1);  color: var(--accent-rose);    border: 1px solid rgba(178,59,59,0.25); }
.intel-tag.neutral  { background: rgba(108,92,224,0.1); color: var(--accent-blue);   border: 1px solid rgba(108,92,224,0.25); }
.intel-tag.warning  { background: rgba(166,121,31,0.1); color: var(--accent-amber);  border: 1px solid rgba(166,121,31,0.25); }

/* ═══════════════════════════════════════════════
   RECOMMENDATION BANNER
═══════════════════════════════════════════════ */
.rec-banner {
    border-radius: 4px;
    padding: 0.85rem 1.2rem;
    margin: 1rem 0;
    border-left: 2px solid;
    font-size: 0.85rem;
    line-height: 1.6;
    background: var(--bg-elevated);
    color: var(--text-secondary);
}

.rec-banner.invest  { border-color: var(--accent-emerald); }
.rec-banner.pass    { border-color: var(--accent-rose); }
.rec-banner.monitor { border-color: var(--accent-amber); }

.rec-banner strong { color: var(--text-primary); letter-spacing: 0.04em; }

/* ═══════════════════════════════════════════════
   STREAMLIT COMPONENT OVERRIDES
═══════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-active) !important;
    border-radius: 5px !important;
    color: var(--text-primary) !important;
    font-size: 0.875rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.15s ease !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-tertiary) !important;
    opacity: 1 !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: none !important;
}

.stButton > button {
    background: var(--accent-navy) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--accent-navy) !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
    padding: 0.55rem 1rem !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    transition: opacity 0.15s ease !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: none !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
}

/* Note: every st.button() call in this app is a primary action (Run Analysis,
   Generate Memo, etc.) — none pass type="secondary" — but Streamlit's default
   `kind` attribute on a plain st.button() is still "secondary". A prior
   `[kind="secondary"]` override here was silently winning (same specificity,
   declared later) and turning every button white/outlined instead of solid
   navy. Removed rather than re-added, since this app has no actual two-tier
   button hierarchy to express. */

.stDownloadButton > button {
    background: var(--bg-card) !important;
    color: var(--accent-navy) !important;
    border: 1px solid var(--accent-navy) !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* Spinner / loading */
.stSpinner > div {
    border-top-color: var(--accent-primary) !important;
}

/* Divider */
hr {
    border-color: var(--border-subtle) !important;
    margin: 1.1rem 0 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    color: var(--text-secondary) !important;
    padding: 0.6rem 1.1rem !important;
}

.stTabs [aria-selected="true"] {
    color: var(--text-primary) !important;
    background: transparent !important;
    border-bottom: 2px solid var(--accent-primary) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 5px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
}

/* Alerts */
.stAlert {
    border-radius: 5px !important;
    border: 1px solid var(--border-subtle) !important;
}

/* Progress */
.stProgress > div > div > div {
    background: var(--accent-primary) !important;
    border-radius: 999px !important;
}

/* Sidebar nav links — the real current test-id is stSidebarNavLink (verified
   against the installed Streamlit build); the old ".stSidebarNav a" selector
   never matched anything, so nav links were unstyled/default-colored. */
[data-testid="stSidebarNavLink"],
.stSidebarNav a {
    font-size: 0.85rem !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
    border-radius: 4px !important;
    transition: background 0.15s ease !important;
    letter-spacing: 0.01em !important;
}

[data-testid="stSidebarNavLink"] span,
.stSidebarNav a span {
    color: inherit !important;
}

[data-testid="stSidebarNavLink"]:hover,
.stSidebarNav a:hover {
    color: var(--accent-primary) !important;
    background: var(--bg-elevated) !important;
}

[data-testid="stSidebarNavLink"][aria-current="page"],
.stSidebarNav a[aria-current="page"] {
    color: var(--accent-primary) !important;
    background: var(--bg-elevated) !important;
    font-weight: 700 !important;
    box-shadow: inset 3px 0 0 var(--accent-primary) !important;
}

/* ═══════════════════════════════════════════════
   LOADING ANIMATION
═══════════════════════════════════════════════ */
.ai-loading {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.85rem 1.2rem;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 5px;
    margin: 1rem 0;
}

.ai-loading .dots {
    display: flex;
    gap: 4px;
}

.ai-loading .dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--accent-primary);
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
    padding: 1.8rem 2.2rem;
    font-size: 0.875rem;
    line-height: 1.8;
    color: var(--text-secondary);
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.05), 0 1px 2px rgba(30, 27, 75, 0.04);
}

.memo-header {
    text-align: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1.1rem;
    border-bottom: 1px solid var(--border-subtle);
}

.memo-title {
    font-family: var(--font-serif);
    font-size: 1.4rem;
    line-height: 1.4;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.005em;
    padding-top: 0.15rem;
}

.memo-subtitle {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-tertiary);
    margin-top: 0.4rem;
}

.memo-section-title {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-tertiary);
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
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #E9E6F9;
    border: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--accent-primary);
    flex-shrink: 0;
}

.founder-name {
    font-family: var(--font-serif);
    font-size: 1.15rem;
    line-height: 1.4;
    font-weight: 600;
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
    width: 7px;
    height: 7px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
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
    background: var(--bg-elevated);
    color: var(--accent-emerald);
}

.callout.bear {
    border-color: var(--accent-rose);
    background: var(--bg-elevated);
    color: var(--accent-rose);
}

.callout.info {
    border-color: var(--accent-blue);
    background: var(--bg-elevated);
    color: var(--accent-blue);
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
    border-radius: 6px;
    padding: 0.9rem 1rem;
    text-align: center;
}

.stat-item .stat-number {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
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


PAGES = [
    ("0_Home_Dashboard.py", "Home"),
    ("pages/1_Startup_Analyzer.py", "Startup Analyzer"),
    ("pages/2_Founder_Intelligence.py", "Founder Intelligence"),
    ("pages/3_Memo_Generator.py", "Memo Generator"),
    ("pages/4_Market_Graph.py", "Market Graph"),
    ("pages/5_System_Intelligence.py", "Settings"),
]


def render_top_nav() -> None:
    """Render the single top nav bar: brand + page links. This replaces the
    sidebar as the only navigation surface in the app (the sidebar is hidden
    via CSS) — call this once, as the first thing rendered on every page,
    right after inject_styles()."""
    with st.container(key="topnav"):
        # Column widths scale with label length so longer labels (e.g.
        # "Founder Intelligence") don't clip inside an equally-sized column
        # meant for a short one (e.g. "Home") — a uniform ratio was cutting
        # text off in longer links.
        ratios = [2.0] + [max(0.8, len(label) / 9) for _, label in PAGES]
        cols = st.columns(ratios)
        with cols[0]:
            st.markdown('<div class="topnav-brand">VentureFlow AI</div>', unsafe_allow_html=True)
        for col, (page_path, label) in zip(cols[1:], PAGES):
            with col:
                st.page_link(page_path, label=label)


def page_header(title: str, subtitle: str) -> None:
    """Render a standardised page header.

    Deliberately a <div>, not <h1> — Streamlit applies its own default
    heading styles/behavior to h1-h6 markdown output that fought with our
    serif override in ways that clipped or hid the text entirely. A plain
    div sidesteps that inherited styling completely."""
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-title">{title}</div>
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
    labels = {"invest": "INVEST", "pass": "PASS", "monitor": "MONITOR"}
    label = labels.get(kind, "MONITOR")
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


def esc(value) -> str:
    """Escape a value for safe interpolation into raw-HTML markdown blocks —
    neutralizes characters (<, >, &, backticks) that could otherwise be
    misread as HTML tags or trigger unintended Markdown parsing."""
    if value is None:
        return ""
    return _html.escape(str(value), quote=False).replace("`", "&#96;")


def flatten_html(fragment: str) -> str:
    """Collapse a dynamically-built (often loop-concatenated) HTML fragment to
    single-line tags. Streamlit's markdown-in-HTML renderer follows CommonMark's
    HTML-block rules: raw HTML built across multiple lines with heavy leading
    indentation (as happens naturally when an f-string sits inside nested Python
    blocks) can be misread as an indented code block after the first entry in a
    loop, silently dumping literal escaped tags into the page. Collapsing
    whitespace before interpolation avoids that whole failure class."""
    if not fragment:
        return fragment
    return _re.sub(r">\s+<", "><", _re.sub(r"\s+", " ", fragment)).strip()


def data_source_badge(meta: dict) -> str:
    """Return an HTML badge + source list showing whether an analysis is
    grounded in real fetched data or inferred from LLM training knowledge.
    `meta` is the `_meta` dict attached by core.ai_engine to every result."""
    if not meta:
        return ""

    confidence = meta.get("confidence", "inferred")
    style_map = {
        "grounded": ("#2F7D5C", "GROUNDED", "Backed by 2+ live data sources"),
        "partial":  ("#A6791F", "PARTIAL",  "Backed by 1 live data source"),
        "inferred": ("#B23B3B", "AI-INFERRED", "No live data fetched — LLM knowledge/guess only"),
    }
    color, label, tooltip = style_map.get(confidence, style_map["inferred"])

    chips = []
    if meta.get("used_website_scrape"):
        chips.append("Website scraped")
    if meta.get("used_web_search"):
        n = len(meta.get("web_sources", []))
        chips.append(f"Web search ({n} sources)")
    if meta.get("used_github"):
        chips.append("GitHub profile")

    sources = meta.get("web_sources", [])
    source_links = "".join(
        f'<a href="{s}" target="_blank" style="display:block;color:#6C5CE0;font-size:0.72rem;'
        f'margin-top:2px;text-decoration:none;overflow:hidden;text-overflow:ellipsis;'
        f'white-space:nowrap;">&#8599; {s}</a>'
        for s in sources
    )
    github_url = meta.get("github_profile_url")
    if github_url:
        source_links += (
            f'<a href="{github_url}" target="_blank" style="display:block;color:#6C5CE0;'
            f'font-size:0.72rem;margin-top:2px;text-decoration:none;">&#8599; {github_url}</a>'
        )

    return f"""
    <div style="margin: 0.6rem 0 1rem; padding: 0.65rem 1rem; background: var(--bg-elevated);
                border: 1px solid var(--border-subtle); border-radius: 5px;">
        <div style="display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap;">
            <span title="{tooltip}" style="font-size:0.65rem; font-weight:700; letter-spacing:0.04em;
                        color:{color}; background:{color}1a; padding:2px 8px; border-radius:3px;">
                {label}
            </span>
            <span style="font-size:0.72rem; color:var(--text-secondary);">{" · ".join(chips) if chips else "No live sources fetched"}</span>
        </div>
        {f'<div style="margin-top:0.5rem;">{source_links}</div>' if source_links else ""}
    </div>
    """


def intel_section(header: str, content: str) -> str:
    """Return a formatted intelligence section."""
    return f"""
    <div class="intel-section">
        <div class="intel-section-header">{header}</div>
        <div class="intel-section p" style="font-size:0.875rem;line-height:1.7;color:var(--text-secondary);">{content}</div>
    </div>
    """
