import streamlit as st

from components.cards import metric_card

from components.charts import (
    expense_trend_chart,
    expense_breakdown_chart
)

from components.sidebar import build_sidebar

from database import get_connection
from utils import (
    get_dashboard_summary,
    expense_trend,
    expense_categories,
    recent_transactions,
    budget_summary,
    goal_summary
)

# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------
# Protect Page
# ---------------------------------------

if not st.session_state.get("logged_in", False):

    st.switch_page("pages/Login.py")

build_sidebar()

st.title(f"👋 Welcome, {st.session_state['name']}")

st.caption(
    "Here's an overview of your financial activity."
)

user_id = st.session_state["user_id"]

summary = get_dashboard_summary(user_id)
budget = budget_summary(user_id)
goal = goal_summary(user_id)

# ---------------------------------------
# Summary Cards
# ---------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        "Income",
        f"₹{summary['income']:,.2f}"
    )

with col2:
    metric_card(
        "Expense",
        f"₹{summary['expense']:,.2f}"
    )

with col3:
    metric_card(
        "Balance",
        f"₹{summary['balance']:,.2f}"
    )

with col4:
    metric_card(
        "Transactions",
        summary["transactions"]
    )
st.divider()

st.subheader("💰 Monthly Budget")

if budget["budget"] > 0:

    progress = budget["expense"] / budget["budget"]
    progress = min(progress, 1.0)

    st.progress(progress)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Budget",
        f"₹{budget['budget']:,.2f}"
    )

    col2.metric(
        "Spent",
        f"₹{budget['expense']:,.2f}"
    )

    col3.metric(
        "Remaining",
        f"₹{budget['remaining']:,.2f}"
    )

    if budget["expense"] > budget["budget"]:

        st.error("⚠️ Budget exceeded!")

    elif budget["expense"] >= budget["budget"] * 0.8:

        st.warning("⚠️ You've used over 80% of your budget.")

    else:

        st.success("✅ You're within your monthly budget.")

else:

    st.info(
        "No monthly budget set yet."
    )

st.divider()


st.subheader("🎯 Savings Goal")

if goal["target_amount"] > 0:

    st.write(f"**Goal:** {goal['goal_name']}")

    st.progress(goal["progress"])

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Target",
        f"₹{goal['target_amount']:,.2f}"
    )

    col2.metric(
        "Saved",
        f"₹{goal['current_amount']:,.2f}"
    )

    col3.metric(
        "Remaining",
        f"₹{goal['remaining']:,.2f}"
    )

    if goal["progress"] >= 1:

        st.success("🎉 Goal achieved!")

    else:

        st.info(
            f"{goal['progress'] * 100:.1f}% completed"
        )

else:

    st.info(
        "No savings goal created yet."
    )

st.divider()

# ---------------------------------------
# Savings Goals
# ---------------------------------------

def load_goal(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            goal_name,
            target_amount,
            current_amount
        FROM savings_goals
        WHERE user_id=?
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return {

            "goal_name": row[0],

            "target_amount": row[1],

            "current_amount": row[2]

        }

    return {

        "goal_name": "",

        "target_amount": 0,

        "current_amount": 0

    }
def save_goal(
    user_id,
    goal_name,
    target_amount,
    current_amount
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO savings_goals(
            user_id,
            goal_name,
            target_amount,
            current_amount
        )
        VALUES(?,?,?,?)
        ON CONFLICT(user_id)
        DO UPDATE SET

            goal_name=excluded.goal_name,

            target_amount=excluded.target_amount,

            current_amount=excluded.current_amount
        """,
        (
            user_id,
            goal_name,
            target_amount,
            current_amount
        )
    )

    conn.commit()

    conn.close()

def goal_summary(user_id):

    goal = load_goal(user_id)

    remaining = max(
        goal["target_amount"] -
        goal["current_amount"],
        0
    )

    percentage = 0

    if goal["target_amount"] > 0:

        percentage = (
            goal["current_amount"] /
            goal["target_amount"]
        )

    return {

        **goal,

        "remaining": remaining,

        "progress": min(
            percentage,
            1.0
        )

    }

# ---------------------------------------
# Charts
# ---------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("📈 Expense Trend")

    trend = expense_trend(user_id)

    if trend.empty:

        st.info("No expense data.")

    else:

        fig = expense_trend_chart(trend)
        st.plotly_chart(
            fig,
            width="stretch"
            )

with right:

    st.subheader("🥧 Expense Breakdown")

    categories = expense_categories(user_id)

    if categories.empty:

        st.info("No expense data.")

    else:
        fig = expense_breakdown_chart(categories)
        st.plotly_chart(
            fig,
            width="stretch"
        )

st.divider()
st.divider()

left, right = st.columns([2, 1])

with left:

    st.subheader("🧾 Recent Transactions")

    recent = recent_transactions(user_id)

    recent = recent.drop(
        columns=["id", "user_id", "created_at"],
        errors="ignore"
    )

    if recent.empty:

        st.info("No transactions yet.")

    else:

        st.dataframe(
            recent,
            hide_index=True,
            width="stretch"
        )

with right:

    st.subheader("💡 Financial Insights")

    if summary["transactions"] == 0:

        st.info(
            "Start by adding your first transaction."
        )

    else:

        savings_rate = 0

        if summary["income"] > 0:

            savings_rate = (
                summary["balance"] /
                summary["income"]
            ) * 100

        if summary["balance"] < 0:

            st.error(
                "Expenses exceed income."
            )

        elif savings_rate >= 20:

            st.success(
                "Excellent savings rate!"
            )

        else:

            st.info(
                "You're within your budget."
            )