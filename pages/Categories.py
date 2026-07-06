import streamlit as st

from components.sidebar import build_sidebar

from utils import (
    load_categories,
    add_category,
    delete_category
)

st.set_page_config(
    page_title="Categories",
    page_icon="🏷️",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")

build_sidebar()

st.title("🏷️ Categories")

user_id = st.session_state["user_id"]

categories = load_categories(user_id)
new_category = st.text_input(
    "New Category"
)

if st.button(
    "Add Category",
    width="stretch"
):

    if new_category.strip():

        success = add_category(
            user_id,
            new_category
        )

        if success:

            st.success(
                "Category added."
            )

            st.rerun()

        else:

            st.warning(
                "Category already exists."
            )
st.divider()

st.subheader("Your Categories")