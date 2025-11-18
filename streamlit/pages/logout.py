import streamlit as st

st.session_state.clear()
st.success("Logged out successfully.")
st.switch_page("login.py")
