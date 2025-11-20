import streamlit as st
from utils import helper

helper.hide_login_page()
st.title("💬 Feedback")

whatsapp_number = "9868212319"
message = "Hi, I’d like to give feedback about your app."

# Encode message for URL
encoded_message = message.replace(" ", "%20").replace("\n", "%0A")
whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

# Styled button
st.markdown(
    f"""
    <a href="{whatsapp_url}" target="_blank">
        <button style='font-size:16px;padding:10px 20px;border:none;border-radius:5px;background-color:#1a6600;color:white;cursor:pointer;'>
            📲 Send feedback on WhatsApp
        </button>
    </a>
    """,
    unsafe_allow_html=True
)
# # Styled button
# st.markdown(
#     f"""
#     <a href="{whatsapp_url}" target="_blank">
#         <button style='font-size:16px;padding:10px 20px;border:none;border-radius:5px;background-color:#25D366;color:white;cursor:pointer;'>
#         <button style='font-size:16px;padding:10px 20px;border:none;border-radius:5px;background-color:#25D366;color:white;cursor:pointer;'>
#             📲 Send feedback on WhatsApp
#         </button>
#     </a>
#     """,
#     unsafe_allow_html=True
# )