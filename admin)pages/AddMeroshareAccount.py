import pandas as pd
import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import streamlit as st
import sqlalchemy
from config import config
from utils import helper



# if "username" not in st.session_state or not st.session_state["username"]:
#     st.warning("⚠️ You must be logged in to access this page.")
#     if st.button("Go to Login Page"):
#         st.switch_page("app.py")
#     st.stop()


# helper.hide_components()
# Set page config
# st.set_page_config(page_title="Add MeroShare Info", page_icon="📝", layout="centered")

st.title("📝 Add MeroShare Account Info")
if st.button("⬅️ Go to Dashboard"):
    st.switch_page("pages/dashboard.py")


# Input fields
client_name = st.text_input("Client Name", help="Username cannot be change, once added.").title()
dp = st.text_input("DP")
username = st.text_input("Username").upper()
password = st.text_input("Password", type="password")
has_verified = st.selectbox("Has Verified Credentials", options=["-select-","Yes", "No"])
category = st.text_input("Cateogry", value="CRED", disabled=True)


# Submit button
if st.button("Submit"):
    if not client_name or not dp or not username or not password:
        st.warning("Please fill in all fields.")
    elif has_verified == "-select-":
        st.warning("Please select a valid option for 'Has Verified Credentials'.")
    elif not dp.isdigit():
        st.warning("DP should be a valid integer.")
    else:
        verified_bool = has_verified == "Yes"
        dp_int = int(dp)

        try:
            engine = sqlalchemy.create_engine(helper.get_holding_engine())
            with engine.begin() as conn:
                result = conn.execute(
                    sqlalchemy.text("SELECT 1 FROM meroshare_acc WHERE username = :username"),
                    {"username": username}
                ).fetchone()

                if result:
                    st.warning("Username already exists. Please use a different one.")
                else:
                    # ✅ Insert new record
                    conn.execute(
                        sqlalchemy.text("""
                            INSERT INTO meroshare_acc (id,"clientName", category ,dp, username, password, "hasVerifiedCredentials", bro)
                            VALUES (gen_random_uuid(), :cname , :category ,:dp,:username, :password, :verified, :bro)
                        """),
                        {
                            "dp": dp_int,
                            "cname":client_name,
                            "category": category,
                            "username": username,
                            "password": password,
                            "verified": verified_bool,
                            "bro": st.session_state.get("username")
                        }
                    )
                    st.success("✅ MeroShare account info added successfully!")
                    

        except Exception as e:
            st.error(f"❌ Failed to insert data: {e}")








def load_data():
    if role in ["MANAGER", "ADMIN"]:
        df = pd.read_sql("SELECT * FROM meroshare_acc", engine)
    else:
        df = pd.read_sql(
            "SELECT * FROM meroshare_acc WHERE bro = %s",
            engine,
            params=(st.session_state['username'],)
        )
    return df


# 📦 Load and display data
try:
    engine = sqlalchemy.create_engine(helper.get_holding_engine())
    role = st.session_state.get("role", "").upper()

    df = load_data()
    df.reset_index(drop=True, inplace=True)
    df.index = df.index + 1  
        
    df.drop(columns=['id'], inplace=True)
    column_order = ['clientName', 'category','dp', 'username', 'password','hasVerifiedCredentials', 'bro']
    total_count = len(df)
    df = df[column_order]
    df.rename(columns=lambda x: helper.camel_to_title(x), inplace=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<h3>👥 Total MeroShare Accounts : {total_count}</h3>", unsafe_allow_html=True)

    if df.empty:
        st.info("No MeroShare accounts registered yet.")
    else:
        st.dataframe(df, width='stretch')

        # 🔧 Add edit/delete controls per row
        for i, row in df.iterrows():
            with st.expander(f"🔧 Manage: {row['Client Name']}"):
                st.write(f"DP: {row['Dp']}")
                st.write(f"Verified: {row['Has Verified Credentials']}")

                # 📝 Edit form
                with st.form(f"edit_form_{i}"):
                    new_dp = st.text_input("DP", value=str(row['Dp']))
                    new_password = st.text_input("Password", value=row['Password'], type="password")
                    new_verified = st.selectbox(
                        "Has Verified Credentials",
                        ["Yes", "No"],
                        index=0 if row['Has Verified Credentials'] else 1
                    )
                    submitted = st.form_submit_button("Update")
                    if submitted:
                        try:
                            with engine.begin() as conn:
                                conn.execute(
                                    sqlalchemy.text("""
                                        UPDATE meroshare_acc
                                        SET dp = :dp, password = :password, "hasVerifiedCredentials" = :verified
                                        WHERE username = :username
                                    """),
                                    {
                                        "dp": int(new_dp),
                                        "password": new_password,
                                        "verified": new_verified == "Yes",
                                        "username": row['Username']
                                    }
                                )
                            st.success("✅ Updated successfully!")
                            df = load_data()
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Update failed: {e}")

                # 🗑️ Delete button
                if st.button(f"Delete {row['Username']}", key=f"delete_{i}"):
                    try:
                        with engine.begin() as conn:
                            conn.execute(
                                sqlalchemy.text("DELETE FROM meroshare_acc WHERE username = :username"),
                                {"username": row['Username']}
                            )
                        st.success(f"🗑️ Deleted {row['Username']} successfully!")
                        df = load_data()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")

except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
