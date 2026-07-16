"""
EXIMIUS AI — Access Gate
Single shared-password gate protecting the publicly deployed app from
unauthenticated use of API-calling features. If APP_PASSWORD is unset,
the gate is skipped entirely (local/dev convenience) — it only activates
once a password is configured, e.g. via Streamlit Cloud secrets.
"""

import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def is_gated() -> bool:
    return bool(os.getenv("APP_PASSWORD"))


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def require_login() -> None:
    """Block the rest of the page from rendering until the correct shared
    password is entered. Call this immediately after inject_styles(), before
    anything else (including the nav bar) — a full gate, not a banner."""
    if not is_gated() or is_authenticated():
        return

    st.markdown(
        """
        <div style="max-width: 380px; margin: 12vh auto 0; text-align: center;">
            <div style="font-family: 'Lora', serif; font-size: 1.6rem; font-weight: 600;
                        color: #1E1B4B; margin-bottom: 0.4rem;">VentureFlow AI</div>
            <div style="font-size: 0.85rem; color: #5B5A66; margin-bottom: 1.8rem;">
                Enter the access password to continue.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        with st.form("login_form"):
            password = st.text_input("Password", type="password", label_visibility="collapsed",
                                      placeholder="Access password")
            submitted = st.form_submit_button("Enter", use_container_width=True)
            if submitted:
                if password == os.getenv("APP_PASSWORD"):
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")

    st.stop()


def render_logout_button(container) -> None:
    """Render a small logout control — only meaningful when the gate is active."""
    if not is_gated():
        return
    with container:
        if st.button("Log out", key="logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()


def is_admin_gated() -> bool:
    return bool(os.getenv("ADMIN_PASSWORD"))


def is_admin_authenticated() -> bool:
    return st.session_state.get("admin_authenticated", False)


def require_admin() -> None:
    """Block a page behind a separate admin password (distinct from the
    regular shared-access password). Fails CLOSED when ADMIN_PASSWORD is
    unset — unlike require_login(), this page exposes backend configuration
    (active model, API routing) that must never be reachable by accident."""
    if is_admin_authenticated():
        return

    if not is_admin_gated():
        st.error(
            "Admin access is not configured. Set `ADMIN_PASSWORD` in your "
            "environment/secrets to enable this page."
        )
        st.stop()

    st.markdown(
        """
        <div style="max-width: 380px; margin: 12vh auto 0; text-align: center;">
            <div style="font-family: 'Lora', serif; font-size: 1.6rem; font-weight: 600;
                        color: #1E1B4B; margin-bottom: 0.4rem;">Admin Access</div>
            <div style="font-size: 0.85rem; color: #5B5A66; margin-bottom: 1.8rem;">
                Enter the admin password to configure system settings.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        with st.form("admin_login_form"):
            password = st.text_input("Admin Password", type="password", label_visibility="collapsed",
                                      placeholder="Admin password")
            submitted = st.form_submit_button("Enter", use_container_width=True)
            if submitted:
                if password == os.getenv("ADMIN_PASSWORD"):
                    st.session_state["admin_authenticated"] = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")

    st.stop()
