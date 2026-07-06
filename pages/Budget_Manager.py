import streamlit as st

from utils import (
    load_budget,
    save_budget,
    budget_summary
)

from components.sidebar import build_sidebar

# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title="Budget Manager",
    page_icon="💰",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")

build_sidebar()

st.title("💰 Budget Manager")

user_id = st.session_state["user_id"]

current_budget = load_budget(user_id)
budget = st.number_input(
    "Monthly Budget",
    min_value=0.0,
    value=float(current_budget),
    step=100.0
)

if st.button(
    "Save Budget",
    width="stretch"
):

    save_budget(
        user_id,
        budget
    )

    st.success(
        "Budget saved successfully!"
    )

    st.rerun()
summary = budget_summary(user_id)

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Budget",
    f"₹{summary['budget']:,.2f}"
)

col2.metric(
    "Spent",
    f"₹{summary['expense']:,.2f}"
)

col3.metric(
    "Remaining",
    f"₹{summary['remaining']:,.2f}"
)
if summary["budget"] > 0:

    progress = summary["expense"] / summary["budget"]

    progress = min(progress, 1.0)

    st.subheader("Budget Usage")

    st.progress(progress)

    st.write(
        f"{progress * 100:.1f}% of your monthly budget has been used."
    )
if summary["budget"] == 0:

    st.info(
        "Set your monthly budget to start tracking."
    )

elif summary["expense"] > summary["budget"]:

    st.error(
        "⚠️ You have exceeded your monthly budget."
    )

elif summary["expense"] >= summary["budget"] * 0.8:

    st.warning(
        "⚠️ You have used more than 80% of your budget."
    )

else:

    st.success(
        "✅ Your spending is within budget."
    )