import streamlit as st

from components.sidebar import build_sidebar
from utils import (
    get_user,
    update_user_name,
    verify_current_password,
    update_password
)

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")

build_sidebar()

st.title("⚙️ Settings")

st.subheader("Account")

user = get_user(
    st.session_state["user_id"]
)

_, name, email, created = user

st.write(f"**Name:** {name}")

st.write(f"**Email:** {email}")

st.write(f"**Joined:** {created}")

st.write(
    f"**User ID:** {st.session_state['user_id']}"
)
st.divider()

st.subheader("Update Name")

new_name = st.text_input(
    "New Name",
    value=name
)
if st.button(
    "💾 Save Name",
    width="stretch"
):

    if not new_name.strip():

        st.error("Name cannot be empty.")

    else:

        update_user_name(
            st.session_state["user_id"],
            new_name
        )

        st.session_state["name"] = new_name

        st.success(
            "Name updated successfully!"
        )

        st.rerun()
st.divider()

st.subheader("🔒 Change Password")

current_password = st.text_input(
    "Current Password",
    type="password"
)

new_password = st.text_input(
    "New Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm New Password",
    type="password"
)

if st.button(
    "Update Password",
    width="stretch"
):

    if not current_password:

        st.error("Please enter your current password.")

    elif len(new_password) < 6:

        st.error(
            "Password must be at least 6 characters."
        )

    elif new_password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    elif not verify_current_password(
        st.session_state["user_id"],
        current_password
    ):

        st.error(
            "Current password is incorrect."
        )

    else:

        update_password(
            st.session_state["user_id"],
            new_password
        )

        st.success(
            "Password updated successfully!"
        )