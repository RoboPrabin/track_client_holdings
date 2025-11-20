from time import sleep
import streamlit as st
import pandas as pd
import sqlalchemy
import io
from utils import page_url
from utils.helper import camel_to_title, format_with_comma, hide_components, get_holding_engine
from utils import helper
from app_state import require_login, current_user
import navigation

# st.set_page_config(page_title="Dashboard")
st.set_page_config(
    page_title="Dashboard",
    page_icon="🏠",
    layout="wide"
)


require_login()            # Redirect to login if not authenticated
navigation.render_sidebar()  # Sidebar menus

user = current_user()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data(ttl=helper.default_ttl())
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

role = current_user().get("role", "").upper()
if role in helper.get_hero_role():
    st.download_button("📥 Download XLSX", data=output, file_name="client_holdings_TSL.xlsx", width='content')

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