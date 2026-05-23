"""
VentureFlow AI — System Intelligence
Allows configuration of AI models and API preferences.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from core.styles import inject_styles, render_sidebar_logo, page_header
from core.config import load_config, save_config

st.set_page_config(
    page_title="System Intelligence — VentureFlow AI",
    page_icon="⚙️",
    layout="wide"
)

inject_styles()
render_sidebar_logo()
page_header("System Intelligence", "Configure active reasoning engines and API connections")

config = load_config()

st.markdown("### AI Model Configuration")
st.markdown(
    "<div style='color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem;'>"
    "Choose the reasoning engine that powers the EXIMIUS intelligence layer."
    "</div>",
    unsafe_allow_html=True
)

models = ["gpt-4o", "gemini-2.5-flash", "gemini-2.5-pro", "llama-3.3-70b-versatile"]
current_index = models.index(config.get("active_model", "gpt-4o")) if config.get("active_model") in models else 3

selected_model = st.selectbox(
    "Active Intelligence Model",
    models,
    index=current_index,
    help="Requires the appropriate API key in your .env file (OPENAI_API_KEY or GEMINI_API_KEY)"
)

if st.button("Save Configuration", type="primary"):
    config["active_model"] = selected_model
    save_config(config)
    st.success(f"System updated. VentureFlow AI is now powered by **{selected_model}**.")
