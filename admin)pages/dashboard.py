# import sys, os
# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
import sqlalchemy
import io

from utils.helper import camel_to_title, format_with_comma, hide_components, get_holding_engine
from utils import helper
from utils.sidebar import render_sidebar

role = st.session_state.get("role", "")
render_sidebar(role)

# ---------------------------------------------------------
# PAGE CONFIG MUST BE THE FIRST STREAMLIT COMMAND
# ---------------------------------------------------------
# st.set_page_config(
#     page_title="Live Client Holdings - TSL",
#     page_icon="📊",
#     layout="wide"
# )

st.title("Dashboard")
st.write("session status: ", st.session_state['logged_in'])
# ---------------------------------------------------------
# AUTHENTICATION CHECK
# ---------------------------------------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("1_🔐_Homepage.py")

# ---------------------------------------------------------
# CLEAN UI
# ---------------------------------------------------------
# hide_components()


# ---------------------------------------------------------
# LOGOUT HANDLER
# ---------------------------------------------------------
if st.query_params.get("logout") == "true":
    st.session_state.clear()
    st.switch_page("app.py")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
def load_data():
    engine = sqlalchemy.create_engine(get_holding_engine())
    df = pd.read_sql("SELECT * FROM holdings", engine)
    return df


# ---------------------------------------------------------
# HEADER UI
# ---------------------------------------------------------
st.markdown("""
<style>
    .header-container { display:flex; justify-content:space-between; align-items:center; }
    .red-button {
        background-color:#d9534f; 
        color:white !important; 
        padding:0.5em 1em; 
        font-weight:bold; 
        border-radius:5px; 
        text-decoration:none !important;
    }
</style>
<div class="header-container">
    <h1><span style="color:red;">Live</span> Client Holdings</h1>
    <a href="?logout=true" class="red-button">Logout</a>
</div>
""", unsafe_allow_html=True)



# ---------------------------------------------------------
# PROCESS DATA
# ---------------------------------------------------------
df = load_data()
df.rename(columns=lambda x: camel_to_title(x), inplace=True)

columns_to_drop = [
    'Id', 'Username', 'Dp', 'Isin', 'REMARKS', 'SCRIPTDESC', 'Demat Pending',
    'Freeze Balance', 'Locking Balance', 'Remarks', 'Wacc Calculated Quantity',
    'Wacc Rate', 'Total Cost Of Capital', 'Pending Wacc Quantity',
    'Pending Wacc Rate', 'Pending Wacc', 'Pending Wacc Count',
    'Pending Wacc Valuation', 'Pending Wacc Total Quantity',
    'Pending Wacc Source', 'Script Desc', 'Average Broker Commission',
    'Sebon', 'Dp Fee', 'Capital Gain', 'Estimated Capital Gain Tax',
    'Ledger Fetched'
]

df = df.drop(columns=columns_to_drop, errors="ignore")

df = df.sort_values(by="Name").reset_index(drop=True)

column_order = [
    'Bro', 'Name', 'Boid', 'Client Code', 'Ledger Balance',
    'Script', 'Ltp', 'Market Value', 'Profit Loss', 'Profit Loss Percentage'
]

df = df[column_order + [c for c in df.columns if c not in column_order]]

df = helper.format_dataframe(df)
df.index = df.index + 1


# ---------------------------------------------------------
# DOWNLOAD BUTTON + NAV BUTTONS
# ---------------------------------------------------------
output = io.BytesIO()
df.to_excel(output, index=False, engine="openpyxl")
output.seek(0)

role = st.session_state.get("role", "").upper()
if role in helper.get_hero_role():
    st.download_button("📥 Download XLSX", data=output, file_name="client_holdings_TSL.xlsx", width='content')


# col_left, col_right = st.columns([3.3, 1])

# with col_left:
#     b1, b2, b3, _ = st.columns([1.3, 1.2, 1.4, 2])

#     with b1:
#         if role in ["MANAGER", "ADMIN"]:
#             st.download_button(
#                 "📥 Download XLSX",
#                 data=output,
#                 file_name="client_holdings_TSL.xlsx",
#                 use_container_width=True
#             )
#         else:
#             if st.button("🧑🏻 Client Summary"):
#                 st.switch_page("pages/client_summary.py")

#     with b2:
#         if role in ["MANAGER", "ADMIN"]:
#             if st.button("🧑🏻 Client Summary"):
#                 st.switch_page("pages/client_summary.py")

#     with b3:
#         if role in ["MANAGER", "ADMIN"]:
#             if st.button("👨🏻‍💼 Manager Summary"):
#                 st.switch_page("pages/manager_summary.py")


# with col_right:
#     if st.button("➕ Add/View Meroshare Account"):
#         st.switch_page("pages/add_meroshare_credentials.py")

#     if role in ['MANAGER', 'ADMIN']:
#         if st.button("➕ Add/View Bro Limit"):
#             st.switch_page("pages/bro_limit.py")
#         if st.button("➕ Create app user"):
#             st.switch_page("pages/create_app_user.py")
#     else:
#         if st.button("👁️ View my Limits"):
#             st.switch_page("pages/bro_limit.py")


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------
search = st.text_input("Search in table", "").strip()

if search:
    mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
    df_filtered = df[mask]
    df_filtered.index = df_filtered.index + 1
else:
    df_filtered = df

st.dataframe(df_filtered, width='content')


# ---------------------------------------------------------
# CSS cleanup
# ---------------------------------------------------------
st.markdown("""
<style>
button[aria-label="Download as CSV"], button[aria-label="Search"] {
    display:none !important;
}
</style>
""", unsafe_allow_html=True)