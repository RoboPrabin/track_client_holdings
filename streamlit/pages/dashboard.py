import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from utils.helper import camel_to_title, format_with_comma, hide_components
from components.nav import navigation_bar
import io
from config import config
import streamlit as st
import pandas as pd
import sqlalchemy 

st = hide_components()
st.set_page_config(
    page_title="Live Client Holdings-TSL",  
    page_icon="📊",                          
    layout="wide"                            
)


# Handle logout logic
if st.query_params.get("logout") == "true":
    hide_components()
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("login.py")



if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Unauthorized access. Please login first.")
    # 👉 Button redirect BEFORE stop()
    if st.button("Go to Login Page"):
        st.switch_page("login.py")
    st.stop()



def load_data():
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{config.postgresql_config['db_user']}:{config.postgresql_config['db_password']}@{config.postgresql_config['db_host']}:{config.postgresql_config['db_port']}/{config.postgresql_config['db_name']}")
    return pd.read_sql("SELECT * FROM holdings", engine)



st.markdown(
    """
    <style>
        .header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .header-title {
            margin: 0;
            display: flex;
            flex-direction: column;
        }
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
    <div class='header-container'>
        <div class='header-title'>
            <h1 style='margin: 0;'>
                <span style='color: red;'>Live</span> Client Holdings
            </h1>
        </div>
        <a href="?logout=true" class="red-button">Logout</a>
    </div>
    """,
    unsafe_allow_html=True
)




df = load_data()
df.rename(columns=lambda x: camel_to_title(x), inplace=True)

# df = df.drop(columns=['ID' ], errors='ignore')
df = df.drop(columns=['Id', 'Username' , 'Dp', 'Isin', 'REMARKS', 'SCRIPTDESC', 'Demat Pending', 'Freeze Balance', 
                        'Locking Balance', 'Remarks', 'Wacc Calculated Quantity', 'Wacc Rate',
                        'Total Cost Of Capital', 'Pending Wacc Quantity', 
                        'Pending Wacc Rate', 'Pending Wacc', 'Pending Wacc Count',
                        'Pending Wacc Valuation', 'Pending Wacc Total Quantity',
                        'Pending Wacc Source', 'Script Desc',
                            'Average Broker Commission','Sebon', 'Dp Fee','Capital Gain',
                            'Estimated Capital Gain Tax', 'Ledger Fetched' ], errors='ignore')



df = df.sort_values(by='Name').reset_index(drop=True)
column_order = ['Bro','Name', 'Boid', 'Client Code', 'Ledger Balance', 'Script', 'Ltp', 'Market Value', 'Profit Loss', 'Profit Loss Percentage']
df = df[column_order + [col for col in df.columns if col not in column_order]]

for col in df.columns:
    if col != 'Boid':
        df[col] = format_with_comma(df[col])

df.reset_index(drop=True, inplace=True)
df.index = df.index + 1  # Start from 1




# Excel download
output = io.BytesIO()
df.to_excel(output, index=False, engine='openpyxl')
output.seek(0)

role = st.session_state.get("role", "").upper()


col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:
    st.download_button(
        label="Download XLSX",
        data=output,
        file_name="client_holdings_TSL.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.markdown("<div style='margin-right: 1    60px;'></div>", unsafe_allow_html=True)




with col2:
    if role != "BRO":
        if st.button("BRO Summary"):
            st.switch_page("pages/bro_summary.py")
    else:
        if st.button("My Summary"):
            st.switch_page("pages/bro_summary.py")



if role != "BRO":
    with col3:
        if st.button("Manager Summary"):
            st.switch_page("pages/manager_summary.py")




st.text_input("Search in table", key="search_query")

search = st.session_state.get("search_query", "").strip()

if search:
    mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
    df_filtered = df[mask]
else:
    df_filtered = df

st.dataframe(df_filtered, width='content')





st.markdown("""
<style>
/* Hide 'Download as CSV' and 'Search' buttons */
button[aria-label="Download as CSV"],
button[aria-label="Search"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)