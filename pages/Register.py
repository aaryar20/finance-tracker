import streamlit as st

from utils import register_user

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Create Account")

name = st.text_input("Full Name")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

confirm = st.text_input(
    "Confirm Password",
    type="password"
)

if st.button("Create Account", use_container_width=True):

    if not name.strip():

        st.error("Please enter your name.")

    elif not email.strip():

        st.error("Please enter your email.")

    elif password != confirm:

        st.error("Passwords do not match.")

    else:

        success = register_user(
            name,
            email,
            password
        )

        if success:

            st.success("Account created successfully.")

            st.switch_page("pages/Login.py")

        else:

            st.error("Email already exists.")

st.divider()

if st.button("Already have an account?"):

    st.switch_page("pages/Login.py")