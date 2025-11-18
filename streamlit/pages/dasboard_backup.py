import re
from datetime import datetime
import io
from config import config
import streamlit as st
import pandas as pd
import sqlalchemy
import time


engine = sqlalchemy.create_engine(
    f"postgresql+psycopg2://{config.postgresql_config['db_user']}:{config.postgresql_config['db_password']}@"
    f"{config.postgresql_config['db_host']}:{config.postgresql_config['db_port']}/{config.postgresql_config['db_name']}"
)

def load_data():
    return pd.read_sql("SELECT * FROM holdings", engine)

st.set_page_config(
    page_title="Live Client Holdings-TSL",  
    page_icon="📊",                          
    layout="wide"                            
)

st.markdown(
    """
    <div style='display: flex; align-items: baseline; gap: 0px;'>
        <h1 style='margin: 0;'>
            <span style='color: red;'>Live</span> Client Holdings
        </h1>
        <span style='font-style: italic; font-size: 1em;'>Refresh every 30 seconds.</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'show_selector' not in st.session_state:
    st.session_state.show_selector = False
if 'selected_cols' not in st.session_state:
    st.session_state.selected_cols = []
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

placeholder = st.empty()




# Function to convert camelCase to Title Case with spaces
def camel_to_title(name):
    # Add space before each capital letter that follows a lowercase letter
    s1 = re.sub('([a-z])([A-Z])', r'\1 \2', name)
    # Capitalize the first letter of each word
    return s1.title()



while True:
    with placeholder.container():
        df = load_data()
        # df.columns = df.columns.str.upper()
        df.rename(columns=lambda x: camel_to_title(x), inplace=True)

        # df = df.drop(columns=['ID' ], errors='ignore')
        df = df.drop(columns=['Id', 'Username' , 'Dp', 'Isin', 'REMARKS', 'SCRIPTDESC', 'Demat Pending', 'Freeze Balance', 
                              'Locking Balance', 'Remarks', 'Wacc Calculated Quantity', 'Wacc Rate',
                              'Total Cost Of Capital', 'Pending Wacc Quantity', 
                              'Pending Wacc Rate', 'Pending Wacc', 'Pending Wacc Count',
                               'Pending Wacc Valuation', 'Pending Wacc Total Quantity',
                                'Pending Wacc Source', 'Script Desc',
                                 'Average Broker Commission','Sebon', 'Dp Fee','Capital Gain',
                                  'Estimated Capital Gain Tax' ], errors='ignore')
        df = df.sort_values(by='Name').reset_index(drop=True)

        # column_order = ['Name',m 'Boid', 'Script']
        # df = df[column_order]
        df.index = df.index + 1

        # Set default selected columns on first load
        if not st.session_state.selected_cols:
            st.session_state.selected_cols = df.columns.tolist()

        # Sidebar
        with st.sidebar:
            st.header("Column Selector")
            if st.button("Show/Hide Columns"):
                st.session_state.show_selector = not st.session_state.show_selector

            if st.session_state.show_selector:
                cols = []
                for col in df.columns:
                    checked = st.checkbox(col, value=col in st.session_state.selected_cols, key=f"chk_{col}")
                    if checked:
                        cols.append(col)
                st.session_state.selected_cols = cols
            else:
                cols = st.session_state.selected_cols

        df_display = df[cols].copy() if cols else df.copy()

        # Search
        st.text_input("Search in table", value=st.session_state.search_query, key="search_query")
        search = st.session_state.search_query.strip()

        if search:
            mask = df_display.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
            df_filtered = df_display[mask]
        else:
            df_filtered = df_display

        # Download button
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        st.download_button(
            label="Download XLSX",
            data=output,
            file_name=f"client_holdings_TSL_{datetime.now().strftime('%Y-%m-%d %I-%M-%S %p')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.dataframe(df_filtered, width='stretch')
    time.sleep(config._REFRESH_TIME_IN_SECONDS)
    st.rerun()
