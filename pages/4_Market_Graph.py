"""
VentureFlow AI — Page 4: Startup Market Graph
Interactive competitive landscape visualization using PyVis.
"""

import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import streamlit.components.v1 as components
from core.styles import inject_styles, render_sidebar_logo, page_header, loading_indicator
from core.ai_engine import generate_graph_data
from core.database import get_all_startup_analyses

st.set_page_config(
    page_title="Market Graph — VentureFlow AI",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()
render_sidebar_logo()
page_header("Startup Intelligence Graph", "Interactive competitive market landscape visualization")

# ── PyVis graph builder ────────────────────────────────────────────────────────

def build_market_graph(graph_data: dict) -> str:
    """
    Build a PyVis network graph from structured graph_data.
    Returns the HTML string of the graph.
    """
    try:
        from pyvis.network import Network
    except ImportError:
        return "<div style='color:#F43F5E;padding:2rem;'>PyVis not installed. Run: pip install pyvis</div>"

    net = Network(
        height="580px",
        width="100%",
        bgcolor="#050810",
        font_color="#8892B0",
        directed=False,
    )
    net.barnes_hut(
        gravity=-8000,
        central_gravity=0.3,
        spring_length=180,
        spring_strength=0.04,
        damping=0.95,
    )

    company_name = graph_data.get("company_name", "Target")

    # ── Target node (centre) ────────────────────────────────────────────────
    net.add_node(
        company_name,
        label=company_name,
        title=f"<b>{company_name}</b><br>Target Company<br>Sector: {graph_data.get('sector','—')}",
        color={
            "background": "#00D4FF",
            "border":     "#4F6EF7",
            "highlight":  {"background": "#4F6EF7", "border": "#00D4FF"},
        },
        size=40,
        font={"size": 14, "color": "#F0F4FF", "bold": True},
        shape="dot",
        shadow={"enabled": True, "color": "rgba(0,212,255,0.7)", "size": 35, "x": 0, "y": 0},
    )

    # ── Competitor / adjacent nodes ─────────────────────────────────────────
    competitors = graph_data.get("competitors", [])
    for comp in competitors:
        name = comp.get("name", "Unknown")
        comp_type = comp.get("type", "adjacent")
        desc = comp.get("description", "")
        stage = comp.get("stage", "")

        if comp_type == "direct":
            color_bg   = "#F43F5E"
            color_brd  = "#C0102A"
            size       = 24
            label_color = "#F43F5E"
        else:
            color_bg   = "#4F6EF7"
            color_brd  = "#2D3A6B"
            size       = 18
            label_color = "#8892B0"

        if comp_type == "direct":
            glow_color = "rgba(244,63,94,0.5)"
            glow_size = 25
        else:
            glow_color = "rgba(79,110,247,0.4)"
            glow_size = 15

        net.add_node(
            name,
            label=name,
            title=f"<b>{name}</b><br>Type: {comp_type.title()}<br>Stage: {stage}<br>{desc}",
            color={
                "background": color_bg,
                "border":     color_brd,
                "highlight":  {"background": "#F0F4FF", "border": color_bg},
            },
            size=size,
            font={"size": 11, "color": label_color},
            shape="dot",
            shadow={"enabled": True, "color": glow_color, "size": glow_size, "x": 0, "y": 0},
        )

        # Edge
        edge_color = "#F43F5E" if comp_type == "direct" else "#2D3A6B"
        edge_label = "Competes" if comp_type == "direct" else "Adjacent"
        net.add_edge(
            company_name,
            name,
            color={"color": edge_color, "opacity": 0.5, "highlight": "#F0F4FF"},
            width=2 if comp_type == "direct" else 1,
            dashes=comp_type != "direct",
            title=edge_label,
        )

    # ── Sector nodes ─────────────────────────────────────────────────────────
    sector_nodes = graph_data.get("sector_nodes", [])
    for sn in sector_nodes:
        sname = sn.get("name", "Sector")
        scat  = sn.get("category", "")
        net.add_node(
            sname,
            label=sname,
            title=f"<b>{sname}</b><br>Category: {scat}",
            color={
                "background": "#111827",
                "border":     "#1A2744",
                "highlight":  {"background": "#1A2744", "border": "#4F6EF7"},
            },
            size=12,
            font={"size": 9, "color": "#4A5568"},
            shape="diamond",
        )
        # Connect sector node to main company
        net.add_edge(
            company_name,
            sname,
            color={"color": "#1A2744", "opacity": 0.3},
            width=1,
            dashes=True,
        )

    # ── Physics / interaction options ────────────────────────────────────────
    net.set_options(json.dumps({
        "nodes": {
            "borderWidth": 2,
            "borderWidthSelected": 4,
            "chosen": True,
        },
        "edges": {
            "smooth": {"type": "continuous", "roundness": 0.4},
            "selectionWidth": 3,
            "hoverWidth": 1.5,
        },
        "interaction": {
            "hover": True,
            "hoverConnectedEdges": True,
            "tooltipDelay": 100,
            "hideEdgesOnDrag": False,
            "navigationButtons": False,
            "keyboard": False,
            "zoomView": True,
        },
        "physics": {
            "enabled": True,
            "barnesHut": {
                "gravitationalConstant": -12000,
                "centralGravity": 0.15,
                "springLength": 220,
                "springConstant": 0.02,
                "damping": 0.09,
            },
            "stabilization": {"iterations": 150},
        },
    }))

    # Write to temp file and read back
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as tmp:
        net.save_graph(tmp.name)
        tmp_path = tmp.name

    with open(tmp_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Inject background colour override into the generated HTML
    html_content = html_content.replace(
        "background-color: #ffffff;", "background-color: #050810;"
    ).replace(
        "background-color:#ffffff;", "background-color:#050810;"
    )

    os.unlink(tmp_path)
    return html_content


# ── Input ──────────────────────────────────────────────────────────────────────
startup_analyses = get_all_startup_analyses()

with st.container():
    c1, c2 = st.columns([2, 1], gap="large")
    with c1:
        # Load from saved or manual
        options_map = {
            f"{s['company_name']} ({s['market_category'] or '—'})": s["data"]
            for s in startup_analyses
        }
        options_map = {"-- Enter manually below --": None, **options_map}
        selected_key = st.selectbox("Load from Saved Analysis", list(options_map.keys()))
        loaded = options_map[selected_key]

        if loaded:
            company_name_g = loaded.get("company_name", "")
            market_cat_g   = loaded.get("market_category", "")
            competitors_g  = loaded.get("competitors", [])
        else:
            company_name_g = st.text_input("Company Name", placeholder="e.g. Substrate AI")
            market_cat_g   = st.text_input("Market Category", placeholder="e.g. AI Infrastructure")
            competitors_raw = st.text_input(
                "Known Competitors (comma-separated)",
                placeholder="e.g. Weights & Biases, MLflow, Comet"
            )
            competitors_g = [c.strip() for c in competitors_raw.split(",") if c.strip()]

    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if loaded:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="intel-section-header">Loaded Context</div>
                    <div style="font-size:0.8rem;color:#8892B0;margin-top:0.3rem;">
                        <strong style="color:#F0F4FF;">{loaded.get('company_name','—')}</strong><br>
                        {loaded.get('market_category','—')} · {loaded.get('stage_fit','—')}<br>
                        Score: {int(loaded.get('investment_score',0))}/100<br>
                        {len(loaded.get('competitors',[]))} competitors identified
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

gen_graph_btn = st.button("⬡  Generate Market Intelligence Graph", use_container_width=False)

# ── Graph generation ───────────────────────────────────────────────────────────
if gen_graph_btn:
    if not company_name_g:
        st.warning("Please select a startup or enter a company name.")
        st.stop()

    loading_placeholder = st.empty()
    loading_placeholder.markdown(
        loading_indicator("Mapping competitive landscape → generating market graph..."),
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        try:
            graph_data = generate_graph_data(
                company_name=company_name_g,
                market_category=market_cat_g,
                competitors=competitors_g,
            )
        except ValueError as e:
            loading_placeholder.empty()
            st.error(f"API Error: {e}")
            st.stop()
        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Graph generation failed: {e}")
            st.stop()

    loading_placeholder.empty()
    st.session_state["last_graph_data"] = graph_data
    st.success("Market graph generated.")

# ── Render graph ───────────────────────────────────────────────────────────────
graph_data = st.session_state.get("last_graph_data")

if graph_data:
    company   = graph_data.get("company_name", "")
    sector    = graph_data.get("sector", "")
    narrative = graph_data.get("market_narrative", "")
    comps     = graph_data.get("competitors", [])

    direct_count   = sum(1 for c in comps if c.get("type") == "direct")
    adjacent_count = sum(1 for c in comps if c.get("type") == "adjacent")

    # Stats
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, val, label in [
        (s1, company, "Target Company"),
        (s2, sector,  "Market Sector"),
        (s3, str(direct_count),   "Direct Competitors"),
        (s4, str(adjacent_count), "Adjacent Companies"),
    ]:
        with col:
            col.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value" style="font-size:1.1rem;">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Market narrative
    if narrative:
        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div class="intel-section-header">Market Intelligence</div>
                <div style="font-size: 0.875rem; color: #8892B0; line-height: 1.75; margin-top: 0.4rem;">
                    {narrative}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Legend
    st.markdown(
        """
        <div style="display:flex;gap:1.5rem;margin-bottom:0.8rem;font-size:0.72rem;color:#8892B0;
                    flex-wrap:wrap;align-items:center;">
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:12px;height:12px;border-radius:50%;background:#00D4FF;flex-shrink:0;"></div>
                <span>Target Company</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:10px;height:10px;border-radius:50%;background:#F43F5E;flex-shrink:0;"></div>
                <span>Direct Competitor</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:10px;height:10px;border-radius:50%;background:#4F6EF7;flex-shrink:0;"></div>
                <span>Adjacent Company</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:10px;height:10px;transform:rotate(45deg);background:#111827;
                            border:1px solid #1A2744;flex-shrink:0;"></div>
                <span>Sector Node</span>
            </div>
            <div style="color:#4A5568;">— Scroll to zoom · Drag to pan · Hover for details</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Graph wrapper
    st.markdown(
        """
        <div style="border: 1px solid #1A2744; border-radius: 10px; overflow: hidden;
                    box-shadow: 0 0 40px rgba(79,110,247,0.06);">
        """,
        unsafe_allow_html=True,
    )

    graph_html = build_market_graph(graph_data)
    components.html(graph_html, height=590, scrolling=False)

    st.markdown("</div>", unsafe_allow_html=True)

    # Competitor table
    if comps:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="glass-card"><div class="intel-section-header">Competitive Landscape Details</div>',
            unsafe_allow_html=True,
        )
        tbl_html = ""
        for c in comps:
            t = c.get("type", "adjacent")
            t_color = "#F43F5E" if t == "direct" else "#4F6EF7"
            t_label = "DIRECT" if t == "direct" else "ADJACENT"
            tbl_html += f"""
            <div style="display:grid;grid-template-columns:140px 80px 1fr 100px;
                        gap:0.8rem;padding:0.65rem 0;border-bottom:1px solid #1A2744;
                        align-items:start;font-size:0.82rem;">
                <div style="color:#F0F4FF;font-weight:600;">{c.get('name','—')}</div>
                <div><span style="font-size:0.65rem;font-weight:700;color:{t_color};
                     text-transform:uppercase;letter-spacing:0.08em;
                     background:rgba(79,110,247,0.08);padding:2px 7px;border-radius:999px;">
                     {t_label}</span></div>
                <div style="color:#8892B0;line-height:1.55;">{c.get('description','')}</div>
                <div style="color:#4A5568;font-size:0.75rem;">{c.get('stage','')}</div>
            </div>
            """
        st.markdown(tbl_html + "</div>", unsafe_allow_html=True)
