import streamlit as st

from components.sidebar import build_sidebar
from components.cards import metric_card

from utils import (
    load_transactions,
    delete_transaction,
    transaction_summary
)

st.set_page_config(
    page_title="Transaction History",
    page_icon="📜",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")

build_sidebar()

st.title("📜 Transaction History")

user_id = st.session_state["user_id"]

df = load_transactions(user_id)

summary = transaction_summary(user_id)

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Income", f"₹{summary['income']:,.2f}")

with col2:
    metric_card("Expense", f"₹{summary['expense']:,.2f}")

with col3:
    metric_card("Balance", f"₹{summary['balance']:,.2f}")

with col4:
    metric_card("Transactions", summary["count"])

from components.cards import metric_card
st.divider()
if df.empty:

    st.info(
        "No transactions yet."
    )

    st.stop()
search = st.text_input(
    "🔍 Search"
)

if search:

    df = df[
        df["category"].str.contains(
            search,
            case=False,
            na=False
        )
        |
        df["description"].fillna("").str.contains(
            search,
            case=False,
            na=False
        )
    ]
transaction_filter = st.selectbox(

    "Transaction Type",

    [
        "All",
        "Income",
        "Expense"
    ]

)

if transaction_filter != "All":

    df = df[
        df["type"] == transaction_filter
    ]
sort = st.radio(

    "Sort",

    [
        "Newest First",
        "Oldest First"
    ],

    horizontal=True

)

ascending = sort == "Oldest First"

df = df.sort_values(

    "date",

    ascending=ascending

)

st.divider()

st.subheader("Transactions")

for row in df.itertuples():

    with st.container(border=True):

        left, right = st.columns([6, 1])

        with left:

            icon = "💸" if row.type == "Expense" else "💰"

            st.markdown(
                f"""
### {icon} {row.category}

**Date:** {row.date}

**Type:** {row.type}

**Amount:** ₹{row.amount:,.2f}

**Description:** {row.description if row.description else "-"}
"""
            )
            with right:
                if st.button(
                    "✏️ Edit",
                    key=f"edit_{row.id}"
                ):
                    
                    st.session_state["edit_transaction"] = row.id
                    st.switch_page("pages/Edit_Transaction.py")
                
                if st.button(
                    "🗑 Delete",
                    key=f"delete_{row.id}",
                    width="stretch"
                ):
                    delete_transaction(
                        row.id,
                        user_id
                        )
                    st.success(
                        "Transaction deleted."
                        )
                    st.rerun()
