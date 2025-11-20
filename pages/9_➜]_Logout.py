# import sys, os
# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(ROOT_DIR)

import streamlit as st
from utils import page_url
from utils import helper
helper.hide_login_page()
# st.session_state.clear()

st.switch_page(page_url.login_url)