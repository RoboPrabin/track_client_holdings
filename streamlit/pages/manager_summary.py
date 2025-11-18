import streamlit as st
import pandas as pd
import sqlalchemy
from config import config
from utils import helper
from auth_guard import require_role

class ManagerSummaryPage:
    def __init__(self):
        st.set_page_config(page_title="Manager Summary")
        helper.hide_components()
        require_role(("MANAGER", "ADMIN"))

    def render(self):
        self.render_header()
        df = self.load_data()
        df = self.format_dataframe(df)
        st.dataframe(df, use_container_width=True)

    def render_header(self):
        if st.button("⬅️ Go to Dashboard"):
            st.switch_page("pages/dashboard.py")
        st.title("🧑‍💼 Manager Summary")

    def load_data(self):
        engine = sqlalchemy.create_engine(helper.get_engine_connection_holding_db())
        return pd.read_sql("SELECT * FROM bro_summary", engine)

    def format_dataframe(self, df):
        df.rename(columns=lambda x: helper.camel_to_title(x), inplace=True)
        for col in df.columns:
            df[col] = helper.format_with_comma(df[col])
        return df

# 🔄 Entry point
if __name__ == "__main__":
    ManagerSummaryPage().render()






# from config import config
# import pandas as pd
# import sqlalchemy
# import streamlit as st
# from auth_guard import require_role
# from utils import helper

# helper.hide_components()



# if st.button("⬅️ Go to Dashboard"):
#     st.switch_page("pages/dashboard.py")

# st.set_page_config(page_title="Manager Summary")

# require_role(("MANAGER", "ADMIN"))

# st.title("🧑‍💼 Manager Summary")

# def load_data():
#     engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{config.postgresql_config['db_user']}:{config.postgresql_config['db_password']}@{config.postgresql_config['db_host']}:{config.postgresql_config['db_port']}/{config.postgresql_config['db_name']}")
#     return pd.read_sql("SELECT * FROM bro_summary", engine)

# # Load and display the bro_summary table
# df = load_data()
# df.rename(columns=lambda x: helper.camel_to_title(x), inplace=True)

# for col in df.columns:
#     # if col != 'Boid':
#     df[col] = helper.format_with_comma(df[col])
# st.dataframe(df, width='stretch')
