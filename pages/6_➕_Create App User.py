
import pandas as pd
import streamlit as st
import uuid
from sqlalchemy import create_engine, text
from utils import helper  # assuming this includes get_engine_connection_holding_db()
# helper.hide_components()

helper.hide_login_page()
helper.logout_if_unauthorized()

# UI Form
st.title("👤 Create New App User")


# st.set_page_config(layout='centered')
# Create DB engine
engine = create_engine(helper.get_holding_engine())


with st.form("create_user_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password", help="Password field is case sensitive.")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["MANAGER", "BRO", "ADMIN"])
    submitted = st.form_submit_button("Create User")

    if submitted:
        if not username or not password or not email:
            st.warning("All fields are required.")
        else:
            try:
                encrypted_pw = password
                user_id = str(uuid.uuid4())

                with engine.begin() as conn:
                    conn.execute(
                        text("""
                            INSERT INTO app_user (id, username, password, email, role)
                            VALUES (:id, :username, :password, :email, :role)
                        """),
                        {
                            "id": user_id,
                            "username": username.lower(),
                            "password": encrypted_pw,
                            "email": email.lower(),
                            "role": role
                        }
                    )
                st.success(f"User '{username}' created successfully.")
            except Exception as e:
                st.error(f"Error creating user: {e}")

st.markdown("---")
st.subheader("📋 All App Users")

# Fetch users
try:
    df_users = pd.read_sql('SELECT * FROM app_user ORDER BY username;', con=engine)
    df_users_display = df_users.drop(columns=["id"])  # Hide UUID column
    search_query = st.text_input("Search in table")

    if search_query:
        df_users_display = df_users_display[df_users_display.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    df_users_display.index += 1
    st.dataframe(df_users_display, width='stretch')
except Exception as e:
    st.error(f"Error loading users: {e}")


st.markdown("---")
st.subheader("✏️ Update or ❌ Delete User")

selected_user = st.selectbox("Select a user to modify", df_users["username"].tolist())

action = st.radio("Action", ["Update", "Delete"])

if action == "Update":
    new_email = st.text_input("New Email", value=df_users.loc[df_users["username"] == selected_user, "email"].values[0])
    new_role = st.selectbox("New Role", ["MANAGER", "BRO", "ADMIN"])
    new_password = st.text_input("New Password", type="password")

    if st.button("Update User"):
        try:
            with engine.begin() as conn:
                conn.execute(
                    text("""
                        UPDATE app_user
                        SET email = :email, role = :role, password = :password
                        WHERE username = :username
                    """),
                    {
                        "email": new_email.lower(),
                        "role": new_role,
                        "password": new_password,
                        "username": selected_user
                    }
                )
            st.success(f"User '{selected_user}' updated successfully.")
        except Exception as e:
            st.error(f"Error updating user: {e}")

elif action == "Delete":
    if st.button("Delete User"):
        try:
            with engine.begin() as conn:
                conn.execute(
                    text("DELETE FROM app_user WHERE username = :username"),
                    {"username": selected_user}
                )
            st.success(f"User '{selected_user}' deleted successfully.")
        except Exception as e:
            st.error(f"Error deleting user: {e}")