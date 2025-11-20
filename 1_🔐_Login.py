import time
from app_state import login_user, is_logged_in
import streamlit as st
from db.db import get_user_by_username
from utils.helper import hide_components
from utils.sidebar import render_sidebar
from utils import page_url
from utils import helper

# # Initialize session state
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# hide_components()
# st.set_page_config(page_title="Login", page_icon="🔐", layout='centered')
# st.title("Login Portal 🔐")


st.set_page_config(page_title="Login", layout="centered")

# If already logged in, redirect automatically
if is_logged_in():
    st.success("Already logged in, redirecting...")
    time.sleep(0.5)
    st.switch_page(page_url.dashbord_url)

# navigation.render_sidebar()  # Optional: show sidebar even on login

st.title("🔐 Login")
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    user = get_user_by_username(username)
    if user and password == user["password"]:
        login_user(user["username"], user["role"])
        st.success("Login successful! Redirecting...")
        time.sleep(0.5)
        st.switch_page(page_url.dashbord_url)
    else:
        st.error("Invalid username or password.")






# # Show login form only if not logged in
# if not st.session_state["logged_in"]:
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     login_button = st.button("Login")

#     if login_button:
#         user = get_user_by_username(username)
#         if user and user["password"] == password:
#             # st.session_state["logged_in"] = True
#             st.session_state.logged_in = True
#             st.session_state["role"] = user["role"]
#             st.session_state["username"] = user["username"]
#             st.switch_page(page_url.dashbord_url)   
#         else:
#             st.error("Invalid credentials")