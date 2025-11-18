import sqlalchemy
import streamlit as st
from auth_guard import require_role
from config import config
import pandas as pd
from utils import helper

helper.hide_components()
if st.button("⬅️ Go to Dashboard"):
    st.switch_page("pages/dashboard.py")

st.set_page_config(page_title="BRO Summary")

require_role(("BRO", "MANAGER", "ADMIN"))

st.title("🙎🏻 BRO Summary")
# st.title("👤 BRO Summary")

def load_data():
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{config.postgresql_config['db_user']}:{config.postgresql_config['db_password']}@{config.postgresql_config['db_host']}:{config.postgresql_config['db_port']}/{config.postgresql_config['db_name']}")
    return pd.read_sql("SELECT * FROM bro_summary", engine)


# Load and display the bro_summary table
df = load_data()
df.rename(columns=lambda x: helper.camel_to_title(x), inplace=True)
for col in df.columns:
    # if col != 'Boid':
    df[col] = helper.format_with_comma(df[col])
st.dataframe(df, width='stretch')

# st.write("Display BRO summary table here...")
