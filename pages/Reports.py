import streamlit as st

from components.sidebar import build_sidebar
from exports.excel import export_transactions_excel
from exports.pdf import export_pdf

from utils import (
    budget_summary,
    goal_summary,
    get_dashboard_summary
)
from utils import (
    load_transactions,
    load_categories
)

st.set_page_config(
    page_title="Reports",
    page_icon="📊",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")

build_sidebar()

st.title("📊 Reports")

user_id = st.session_state["user_id"]

df = load_transactions(user_id)

if df.empty:

    st.info("No transactions available.")

    st.stop()

# ----------------------------
# Filters
# ----------------------------

st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:

    transaction_type = st.selectbox(
        "Type",
        ["All", "Income", "Expense"]
    )

with col2:

    categories = ["All"] + load_categories(user_id)

    category = st.selectbox(
        "Category",
        categories
    )

with col3:

    months = ["All"] + sorted(
        df["date"].str[:7].unique(),
        reverse=True
    )

    month = st.selectbox(
        "Month",
        months
    )

filtered = df.copy()

if transaction_type != "All":
    filtered = filtered[
        filtered["type"] == transaction_type
    ]

if category != "All":
    filtered = filtered[
        filtered["category"] == category
    ]

if month != "All":
    filtered = filtered[
        filtered["date"].str.startswith(month)
    ]

st.divider()

income = filtered[
    filtered["type"] == "Income"
]["amount"].sum()

expense = filtered[
    filtered["type"] == "Expense"
]["amount"].sum()

balance = income - expense

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Transactions",
    len(filtered)
)

c2.metric(
    "Income",
    f"₹{income:,.2f}"
)

c3.metric(
    "Expense",
    f"₹{expense:,.2f}"
)

c4.metric(
    "Balance",
    f"₹{balance:,.2f}"
)

st.divider()

excel_file = export_transactions_excel(filtered)
st.download_button(

    label="📥 Download Excel Report",

    data=excel_file,

    file_name="Finance_Report.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    width="stretch"
)

summary = get_dashboard_summary(user_id)

budget = budget_summary(user_id)

goal = goal_summary(user_id)

pdf = export_pdf(

    st.session_state["name"],

    summary,

    budget,

    goal,

    filtered

)

st.download_button(

    label="📄 Download PDF Report",

    data=pdf,

    file_name="Finance_Report.pdf",

    mime="application/pdf",

    width="stretch"

)


st.dataframe(
    filtered,
    hide_index=True,
    width="stretch"
)

