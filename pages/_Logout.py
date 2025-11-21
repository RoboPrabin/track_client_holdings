# _Logout.py
import streamlit as st
from utils import page_url
from app_state import logout_user

logout_user()                    # clears cookies
# st.switch_page(page_url.login_url)  # redirect immediately