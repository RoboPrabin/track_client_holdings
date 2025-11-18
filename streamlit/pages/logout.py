import streamlit as st
from utils import helper

helper.hide_components()
st.session_state.clear()
st.success("Logged out successfully.")
st.switch_page("login.py")
