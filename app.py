"""Diwali Spin & Play — Streamlit wrapper with a simple host login.

Username and password come from Streamlit Secrets:

    [login]
    username = "admin"
    password = "your-password"
"""
import hmac
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Diwali Spin & Play", page_icon="🪔", layout="wide",
                   initial_sidebar_state="collapsed")

# Hide Streamlit's menu, header and footer so the big screen shows only the app.
st.markdown("""
<style>
  #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {visibility:hidden; height:0;}
  .stApp {background:#1b1035;}
  .block-container {padding-top:1rem; padding-bottom:0; max-width:1200px;}
  h1, h2, h3, p, label, .stMarkdown {color:#fff4dc !important;}
  .login-title {font-size:2.4rem; color:#f6a821 !important; text-align:center; margin-bottom:0;}
  .login-sub {text-align:center; color:#c9b9e6 !important;}
</style>
""", unsafe_allow_html=True)


def credentials():
    try:
        return st.secrets["login"]["username"], st.secrets["login"]["password"]
    except Exception:
        return None, None


def login_screen():
    user, pwd = credentials()
    st.markdown('<p class="login-title">🪔 Happy Diwali</p>', unsafe_allow_html=True)
    st.markdown('<p class="login-sub">Host sign-in for the Diwali celebration</p>', unsafe_allow_html=True)
    if user is None:
        st.error("The login isn't set up yet. Add a [login] section with username and password "
                 "in this app's Settings → Secrets on Streamlit Cloud.")
        st.stop()
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            ok = st.form_submit_button("Sign in", use_container_width=True)
        if ok:
            if hmac.compare_digest(u.strip().lower(), str(user).lower()) and hmac.compare_digest(p, str(pwd)):
                st.session_state.signed_in = True
                st.rerun()
            else:
                st.error("That username or password doesn't match. Check with the event host.")


if not st.session_state.get("signed_in"):
    login_screen()
    st.stop()

html = (Path(__file__).parent / "diwali.html").read_text(encoding="utf-8")
components.html(html, height=1250, scrolling=True)

_, right = st.columns([6, 1])
with right:
    if st.button("Sign out"):
        st.session_state.signed_in = False
        st.rerun()
