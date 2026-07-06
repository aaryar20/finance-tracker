import streamlit as st

from components.sidebar import build_sidebar

from utils import (
    load_goal,
    save_goal,
    goal_summary
)

st.set_page_config(
    page_title="Savings Goals",
    page_icon="🎯",
    layout="wide"
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/Login.py")

build_sidebar()

st.title("🎯 Savings Goals")

user_id = st.session_state["user_id"]

goal = load_goal(user_id)

goal_name = st.text_input(
    "Goal Name",
    value=goal["goal_name"]
)

target = st.number_input(
    "Target Amount",
    min_value=0.0,
    value=float(goal["target_amount"]),
    step=100.0
)

current = st.number_input(
    "Current Savings",
    min_value=0.0,
    value=float(goal["current_amount"]),
    step=100.0
)

if st.button(
    "Save Goal",
    width="stretch"
):

    save_goal(
        user_id,
        goal_name,
        target,
        current
    )

    st.success(
        "Goal saved successfully."
    )

    st.rerun()

summary = goal_summary(user_id)

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Target",
    f"₹{summary['target_amount']:,.2f}"
)

col2.metric(
    "Saved",
    f"₹{summary['current_amount']:,.2f}"
)

col3.metric(
    "Remaining",
    f"₹{summary['remaining']:,.2f}"
)
if summary["target_amount"] > 0:

    st.subheader("Progress")

    st.progress(summary["progress"])

    st.write(
        f"{summary['progress'] * 100:.1f}% completed"
    )
if summary["target_amount"] == 0:

    st.info(
        "Create a savings goal to start tracking."
    )

elif summary["current_amount"] >= summary["target_amount"]:

    st.success(
        "🎉 Congratulations! You achieved your goal."
    )

else:

    st.info(
        f"₹{summary['remaining']:,.2f} remaining to reach your goal."
    )