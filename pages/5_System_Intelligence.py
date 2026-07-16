"""
VentureFlow AI — System Intelligence
Allows configuration of AI models and API preferences.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from core.auth import require_login, require_admin
from core.styles import inject_styles, render_top_nav, page_header
from core.config import load_config, save_config
from core.ai_engine import MODEL_CATALOG

st.set_page_config(
    page_title="System Intelligence — VentureFlow AI",
    page_icon="⚙️",
    layout="wide"
)

inject_styles()
require_login()
require_admin()
render_top_nav()
page_header("System Intelligence", "Configure active reasoning engines and API connections")

config = load_config()

st.markdown("### AI Model Configuration")
st.markdown(
    "<div style='color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;'>"
    "Choose the reasoning engine that powers the EXIMIUS intelligence layer."
    "</div>",
    unsafe_allow_html=True
)

model_ids = [model_id for _, model_id, _ in MODEL_CATALOG]
labels_by_id = {model_id: label for _, model_id, label in MODEL_CATALOG}
current_model = config.get("active_model", model_ids[0])
current_index = model_ids.index(current_model) if current_model in model_ids else 0

selected_model = st.selectbox(
    "Active Intelligence Model",
    model_ids,
    index=current_index,
    format_func=lambda mid: labels_by_id[mid],
    help="Falls back automatically to the next configured provider on rate-limit/quota errors."
)

if st.button("Save Configuration", type="primary"):
    config["active_model"] = selected_model
    save_config(config)
    st.success(f"System updated. VentureFlow AI is now powered by **{labels_by_id[selected_model]}**.")
