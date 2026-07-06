import streamlit as st

from config import APP_NAME, APP_ICON
from database import initialize_database

initialize_database()

st.set_page_config(

    page_title=APP_NAME,

    page_icon=APP_ICON,

    layout="centered"

)

if st.session_state.get("logged_in", False):

    st.switch_page("pages/Dashboard.py")

else:

    st.switch_page("pages/Login.py")