import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import streamlit as st
from db import get_user_by_username
import streamlit.components.v1 as components
from utils.helper import hide_components

class StreamlitLoginPage:
    def __init__(self):
        st.set_page_config(page_title="Login", layout="centered", page_icon="🔐")
        hide_components()
        
    def start_page(self):
        st.title("Login Portal 🔐 ")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = get_user_by_username(username)
            print(user, password)
            if user and user["password"] == password:
                st.session_state["username"] = user["username"]
                st.session_state["role"] = user["role"]
                st.session_state["logged_in"] = True 

                st.success("Login successful! Redirecting...")
                st.switch_page("pages/dashboard.py")
            else:
                st.error("Invalid credentials")


if __name__ == "__main__":
    StreamlitLoginPage().start_page()