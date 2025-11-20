
import streamlit as st
from db.db import get_user_by_username
from utils.helper import hide_components
from utils.sidebar import render_sidebar
from utils import page_url
from utils import helper


# helper.hide_login_page()

hide_components()
st.set_page_config(page_title="Login", page_icon="🔐", layout='centered')
st.title("Login Portal 🔐")

st.session_state.clear()
# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Show login form only if not logged in
if not st.session_state["logged_in"]:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        user = get_user_by_username(username)
        if user and user["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["role"] = user["role"]
            st.session_state["username"] = user["username"]
            st.switch_page(page_url.dashbord_url)
            # st.navigation()
            # st.page_link(page="pages/Dashboard.py", label="Dashboad", icon="✨")
        else:
            st.error("Invalid credentials")