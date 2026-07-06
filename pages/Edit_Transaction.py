import streamlit as st
from datetime import datetime

from utils import (
    get_transaction,
    update_transaction,
    load_categories
)

from components.sidebar import build_sidebar

# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title="Edit Transaction",
    page_icon="✏️",
    layout="wide"
)

# ---------------------------------------
# Protect Page
# ---------------------------------------

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")
if "edit_transaction" not in st.session_state:
    st.switch_page("pages/Transaction_History.py")
build_sidebar()

st.title("✏️ Edit Transaction")

user_id = st.session_state["user_id"]

transaction_id = st.session_state.get("edit_transaction")

if transaction_id is None:
    st.switch_page("pages/Transaction_History.py")

transaction = get_transaction(
    transaction_id,
    user_id
)

if transaction is None:

    st.error("Transaction not found.")

    st.stop()

_, date, transaction_type, category, amount, description = transaction

categories = load_categories(user_id)

if category not in categories:
    categories.append(category)

categories = sorted(categories)

with st.form("edit_form"):

    new_date = st.date_input(
        "Date",
        value=datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()
    )

    new_type = st.selectbox(
        "Type",
        [
            "Expense",
            "Income"
        ],
        index=0 if transaction_type == "Expense" else 1
    )

    new_category = st.selectbox(
         "Category",
         categories,
         index=categories.index(category)
         )

    new_amount = st.number_input(
        "Amount",
        min_value=0.0,
        value=float(amount)
    )

    new_description = st.text_area(
        "Description",
        value=description
    )

    col1, col2 = st.columns(2)

    save = col1.form_submit_button(
        "💾 Save Changes"
    )

    cancel = col2.form_submit_button(
        "❌ Cancel"
    )

if save:

    update_transaction(

        transaction_id,

        user_id,

        str(new_date),

        new_type,

        new_category,

        new_amount,

        new_description

    )

    st.success("Transaction updated successfully.")

    del st.session_state["edit_transaction"]

    st.switch_page("pages/Transaction_History.py")

if cancel:

    del st.session_state["edit_transaction"]

    st.switch_page("pages/Transaction_History.py")