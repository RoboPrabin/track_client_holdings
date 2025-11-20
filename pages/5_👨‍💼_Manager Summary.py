import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from config import config
from utils import helper
# from auth_guard import require_role


class ManagerSummaryPage:
    def __init__(self):
        helper.hide_login_page()
        helper.logout_if_unauthorized()

    def render(self):
        self.render_header()
        df = self.load_data()
        df = helper.format_dataframe(df)
        search_query = st.text_input("Search in table")

        if search_query:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

        df.index += 1
        st.dataframe(df, width='stretch')

    def render_header(self):
        # if st.button("⬅️ Go to Dashboard"):
        #     st.switch_page("pages/dashboard.py")
        st.title("🧑‍💼 Manager Summary")


    def sync_limits_to_manager_summary(self):
        engine = create_engine(helper.get_holding_engine())
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE manager_summary2
                SET 
                    "totalLimit" = bl."totalLimit",
                    "usedLimit" = bl."usedLimit"
                FROM bro_limit bl
                WHERE manager_summary2.bro = bl."broCode"
            """))

    @st.cache_data(ttl=helper.default_ttl())
    def load_data(_self):
        engine = create_engine(helper.get_holding_engine())
        
        # Sync limits from bro_limit
        _self.sync_limits_to_manager_summary()

        df = pd.read_sql("SELECT * FROM manager_summary2", engine)
        df.reset_index(drop=True, inplace=True)
        df.index = df.index + 1  
        return df



# 🔄 Entry point
if __name__ == "__main__":
    ManagerSummaryPage().render()