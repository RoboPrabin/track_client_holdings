# app_state.py
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import time
from utils import page_url
# ------ COOKIE SETUP ------
cookies = EncryptedCookieManager(
    prefix="trishakti_app_",  # cookie namespace
    password="THIS_IS_SECRET_CHANGE_IT_123"  # must be constant
)

if not cookies.ready():
    st.stop()


def login_user(username, role):
    """Sets logged in user info in encrypted cookies."""
    cookies["logged_in"] = "1"
    cookies["username"] = username
    cookies["role"] = role
    cookies.save()     # IMPORTANT


def logout_user():
    """Clears login cookies."""
    cookies["logged_in"] = "0"
    cookies["username"] = ""
    cookies["role"] = ""
    cookies.save()
    st.rerun()
    st.switch_page(page_url.login_url)


def is_logged_in():
    return cookies.get("logged_in") == "1"


def current_user():
    return {
        "username": cookies.get("username"),
        "role": cookies.get("role")
    }


def require_login():
    """Redirects to login if cookie says user is not logged in."""
    if not is_logged_in():
        st.switch_page(page_url.login_url)
        st.stop()