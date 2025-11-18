# components/nav.py
import streamlit as st

def navigation_bar():
    role = st.session_state.get("role", "").upper()

    left, right = st.columns([3, 1])

    with left:
        if role in ["MANAGER", "ADMIN"]:
            cols = st.columns(2)
            with cols[0]:
                if st.button("BRO Summary"):
                    st.switch_page("pages/bro_summary.py")
            with cols[1]:
                if st.button("Manager Summary"):
                    st.switch_page("pages/manager_summary.py")
        elif role == "BRO":
            if st.button("My Summary"):
                st.switch_page("pages/bro_summary.py")

    with right:
        st.markdown("""
            <style>
                .red-button {
                    display: inline-block;
                    background-color: #d9534f;
                    color: white !important;
                    border: none;
                    padding: 0.5em 1em;
                    font-weight: bold;
                    border-radius: 5px;
                    text-align: center;
                    text-decoration: none !important;
                    cursor: pointer;
                }
            </style>
            <a href="?logout=true" class="red-button">Logout</a>
        """, unsafe_allow_html=True)

        if st.query_params.get("logout") == "true":
            st.session_state.logged_in = False
            st.session_state.role = None
            st.switch_page("login.py")