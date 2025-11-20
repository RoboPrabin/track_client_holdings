import streamlit as st
from utils import helper  # adjust path as needed

def render_sidebar(role: str):
    base_path = "pages/"
    hero_roles = helper.get_hero_role()

    # Define all pages and their access roles
    pages = [
        {"label": "🏠 Dashboard", "file": "Dashboard.py", "roles": ["ALL"]},
        {"label": "📃 Client Summary", "file": "ClientSummary.py", "roles": ["ALL"]},
        {"label": "🧑‍🦱 Bro Limit", "file": "BroLimit.py", "roles": ["ALL"]},
        {"label": "👨‍💼 Manager Summary", "file": "ManagerSummary.py", "roles": ["ALL"]},
        {"label": "➕ Create App User", "file": "CreateAppUser.py", "roles": hero_roles},
        {"label": "✨ Add Meroshare Account", "file": "AddMeroshareAccount.py", "roles": ["ALL"]},
    ]

    # Normalize role
    role = role.upper() if role else ""

    # Render sidebar links
    for page in pages:
        if "ALL" in page["roles"] or role in page["roles"]:
            st.sidebar.page_link(base_path + page["file"], label=page["label"])