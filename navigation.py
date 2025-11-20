
# navigation.py
import streamlit as st
from app_state import is_logged_in, current_user, logout_user
from utils import page_url
def render_sidebar():
    """
    Renders the sidebar menus based on login state and role.
    """

    # lt = st.sidebar.feedback(options='faces')
    # user = current_user()
    # print(str(current_user['username'].upper()))
    # st.success(f"{lt}, {user['username'].upper()}")
    st.markdown("""
        <style>
            [data-testid="stSidebarCollapseButton"] {
                visibility: visible !important;
                opacity: 1 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    # st.sidebar.title("Menu")
    # st.sidebar.image("https://trishakti.com.np/img/logo1.png",width=140)
    # st.sidebar.markdown(
    # """
    # <div style='text-align:center; margin-bottom:10px;'>
    #     <img src='https://trishakti.com.np/img/logo1.png' width='100'>
    # </div>
    # <hr style='margin:30px 0 30px 0;'>
    # """,
    # unsafe_allow_html=True
    # )
    # st.sidebar.markdown("---")
    # st.sidebar.caption("-----")
    # st.markdown("<hr></hr>", unsafe_allow_html=True)

    if not is_logged_in():
        st.sidebar.page_link(page_url.login_url, label="Login", icon="🔐")
        return

    user = current_user()
    role = user.get("role")
    
    # Authenticated menus
    st.sidebar.page_link(page_url.dashbord_url, label="Dashboard", icon="🏠")

    # navigation.py (partial, inside render_sidebar)
    if role in ["BRO", "MANAGER", "ADMIN"]:
        st.sidebar.markdown("## Summary")  # Group header
        st.sidebar.page_link(page_url.client_summary_url, label="Client", icon="📃")
        st.sidebar.page_link(page_url.manager_summary_url, label="Manager", icon="👨‍💼")
        # st.sidebar.button("Client Summary", key="client_summary_btn",
                        # on_click=lambda: st.session_state.update({"current_page": page_url.client_summary_url}))
        
        if role in ["MANAGER", "ADMIN"]:
            st.sidebar.markdown("## Limiter")  # Group header
            st.sidebar.page_link(page_url.bro_limit_url, label="BR Officer", icon="🧑‍🦱")
            st.sidebar.markdown("## Create")  # Group header
            st.sidebar.page_link(page_url.create_app_user_url, label="App user", icon="➕")
            # st.sidebar.button("Manager Summary", key="manager_summary_btn",
            st.sidebar.page_link(page_url.meroshare_url, label="Meroshare account", icon="✨")
                            # on_click=lambda: st.session_state.update({"current_page": page_url.manager_summary_url}))
    
        st.sidebar.markdown("## Feedback")  # Group header
        st.sidebar.page_link(page_url.feedback_url, label="Ping", icon="💬")
    # st.markdown("""_______""", unsafe_allow_html=True)
    st.sidebar.page_link(page_url.login_url, label="Logout", icon="🏃")
    # st.sidebar.page_link("pages/_Dashboard.py", label="Dashboard", icon="🏠")
    # st.sidebar.page_link("pages/_Dashboard.py", label="Dashboard", icon="🏠")
    # st.sidebar.page_link("pages/_Dashboard.py", label="Dashboard", icon="🏠")
    # st.sidebar.page_link("pages/_Dashboard.py", label="Dashboard", icon="🏠")

    # if role == "bro":
    #     st.sidebar.page_link("4_🧑‍🦱_Bro Limit", label="BRO Summary")
    # if role == "manager":
    #     st.sidebar.page_link("5_👨‍💼_Manager Summary", label="Manager Summary")
    # if role == "admin":
    #     st.sidebar.page_link("6_➕_Create App User", label="Admin Panel")

    # Logout
    # if st.sidebar.button("Logout"):
    #     logout_user()
    #     st.switch_page(page_url.login_url)
    
    with st.sidebar:
    # ... your other sidebar items ...

        st.markdown("""<div style="margin-top: 100px;"></div>""", unsafe_allow_html=True)  # spacer
        st.markdown(
            "<p style='text-align: center; color: gray; font-size: 12px;'>"
            "© Trishakti Securities Limited.<br>All Rights Reserved."
            "</p>",
            unsafe_allow_html=True
        )