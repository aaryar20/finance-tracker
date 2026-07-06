import streamlit as st

from utils import login_user

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Login")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login", use_container_width=True):

    user = login_user(
        email,
        password
    )

    if user:

        st.session_state["logged_in"] = True
        st.session_state["user_id"] = user["id"]
        st.session_state["name"] = user["name"]

        st.switch_page("pages/Dashboard.py")

    else:

        st.error("Invalid email or password.")

st.divider()

if st.button("Create Account"):

    st.switch_page("pages/Register.py")