import streamlit as st
from datetime import date

from components.sidebar import build_sidebar

from utils import (
    add_transaction,
    load_categories
)
# -----------------------------
# Protect Page
# -----------------------------

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Add Transaction",
    page_icon="➕",
    layout="wide"
)
st.set_page_config(
    page_title="Add Transaction",
    page_icon="➕",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")

build_sidebar()

st.title("➕ Add Transaction")

st.write("Record a new income or expense.")

# -----------------------------
# User
# -----------------------------

user_id = st.session_state["user_id"]

# -----------------------------
# Form
# -----------------------------

with st.form("transaction_form"):

    col1, col2 = st.columns(2)

    with col1:

        transaction_date = st.date_input(
            "Date",
            value=date.today()
        )

        transaction_type = st.selectbox(
            "Type",
            [
                "Expense",
                "Income"
            ]
        )

    with col2:
        categories = load_categories(user_id)

        category = st.selectbox(
            "Category",
            categories
            )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=1.0
        )

    description = st.text_area(
        "Description"
    )

    submitted = st.form_submit_button(
        "💾 Save Transaction"
    )

# -----------------------------
# Save
# -----------------------------

if submitted:

    if amount <= 0:

        st.error("Amount must be greater than zero.")

    else:

        add_transaction(
            user_id,
            str(transaction_date),
            transaction_type,
            category,
            amount,
            description
        )

        st.success("Transaction added successfully!")

        st.balloons()