import streamlit as st

def require_role(allowed_roles: tuple):
    role = st.session_state.get("role")
    
    if role not in allowed_roles:
        st.error("Unauthorized access")
        st.stop()
