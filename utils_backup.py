import sqlite3
import pandas as pd

from config import DB_NAME
from database import get_connection
from components.auth import hash_password, verify_password




# ---------------------------------------
# Register User
# ---------------------------------------

def register_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES(?,?,?)
            """,
            (
                name.strip(),
                email.strip().lower(),
                hash_password(password)
            )
        )

        user_id = cursor.lastrowid

        conn.commit()

        conn.close()

        create_default_categories(user_id)

        return True

    except sqlite3.IntegrityError:

        conn.close()

        return False
# ---------------------------------------
# Login User
# ---------------------------------------

def login_user(email, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,name,password
        FROM users
        WHERE email=?
        """,
        (email.strip().lower(),)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return None

    user_id, name, hashed_password = user

    if verify_password(password, hashed_password):

        return {

            "id": user_id,

            "name": name

        }

    return None

# ---------------------------------------
# Transactions
# ---------------------------------------

def add_transaction(
    user_id,
    date,
    transaction_type,
    category,
    amount,
    description
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions(
            user_id,
            date,
            type,
            category,
            amount,
            description
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            user_id,
            date,
            transaction_type,
            category,
            amount,
            description
        )
    )

    conn.commit()

    conn.close()

def load_transactions(user_id):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM transactions
        WHERE user_id=?
        ORDER BY date DESC
        """,
        conn,
        params=(user_id,)
    )

    conn.close()

    return df  

def delete_transaction(
    transaction_id,
    user_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM transactions
        WHERE id=?
        AND user_id=?
        """,
        (
            transaction_id,
            user_id
        )
    )

    conn.commit()

    conn.close()

def get_transaction(transaction_id, user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            date,
            type,
            category,
            amount,
            description
        FROM transactions
        WHERE id=?
        AND user_id=?
        """,
        (
            transaction_id,
            user_id
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row

def update_transaction(
    transaction_id,
    user_id,
    date,
    transaction_type,
    category,
    amount,
    description
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET
            date=?,
            type=?,
            category=?,
            amount=?,
            description=?
        WHERE
            id=?
        AND
            user_id=?
        """,
        (
            date,
            transaction_type,
            category,
            amount,
            description,
            transaction_id,
            user_id
        )
    )

    conn.commit()

    conn.close()


# ---------------------------------------
# Transaction Summary
# ---------------------------------------

def transaction_summary(user_id):

    df = load_transactions(user_id)

    if df.empty:

        return {
            "income": 0,
            "expense": 0,
            "balance": 0,
            "count": 0
        }

    income = df[df["type"] == "Income"]["amount"].sum()

    expense = df[df["type"] == "Expense"]["amount"].sum()

    return {

        "income": income,

        "expense": expense,

        "balance": income - expense,

        "count": len(df)

    }


def get_dashboard_summary(user_id):

    df = load_transactions(user_id)

    if df.empty:

        return {
            "income": 0,
            "expense": 0,
            "balance": 0,
            "transactions": 0
        }

    income = df[df["type"] == "Income"]["amount"].sum()

    expense = df[df["type"] == "Expense"]["amount"].sum()

    return {

        "income": income,

        "expense": expense,

        "balance": income - expense,

        "transactions": len(df)
        }
def expense_trend(user_id):

    df = load_transactions(user_id)

    expense = df[df["type"] == "Expense"]

    if expense.empty:

        return expense

    return (
        expense
        .groupby("date")["amount"]
        .sum()
        .reset_index()
    )
def expense_categories(user_id):

    df = load_transactions(user_id)

    expense = df[df["type"] == "Expense"]

    if expense.empty:

        return expense

    return (
        expense
        .groupby("category")["amount"]
        .sum()
        .reset_index()
    )
def recent_transactions(user_id, limit=5):

    df = load_transactions(user_id)

    return df.head(limit)

# ---------------------------------------
# Budget
# ---------------------------------------

def load_budget(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT monthly_budget
        FROM budget
        WHERE user_id=?
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return row[0]

    return 0
def save_budget(
    user_id,
    amount
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO budget(
            user_id,
            monthly_budget
        )
        VALUES(?,?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            monthly_budget=excluded.monthly_budget
        """,
        (
            user_id,
            amount
        )
    )

    conn.commit()

    conn.close()
def budget_summary(user_id):

    budget = load_budget(user_id)

    df = load_transactions(user_id)

    expense = df[
        df["type"] == "Expense"
    ]["amount"].sum()

    remaining = budget - expense

    return {

        "budget": budget,

        "expense": expense,

        "remaining": remaining

    }
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
        goal["target_amount"] - goal["current_amount"],
        0
    )

    progress = 0

    if goal["target_amount"] > 0:

        progress = goal["current_amount"] / goal["target_amount"]

    return {

        "goal_name": goal["goal_name"],

        "target_amount": goal["target_amount"],

        "current_amount": goal["current_amount"],

        "remaining": remaining,

        "progress": min(progress, 1.0)

    }
# ---------------------------------------
# Categories
# ---------------------------------------

def load_categories(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM categories
        WHERE user_id=?
        ORDER BY name
        """,
        (user_id,)
    )

    categories = [
        row[0]
        for row in cursor.fetchall()
    ]

    conn.close()

    return categories
# ---------------------------------------
# Categories
# ---------------------------------------

def load_categories(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM categories
        WHERE user_id=?
        ORDER BY name
        """,
        (user_id,)
    )

    categories = [row[0] for row in cursor.fetchall()]

    conn.close()

    return categories


def create_default_categories(user_id):

    default_categories = [
        "Food",
        "Transport",
        "Shopping",
        "Entertainment",
        "Bills",
        "Healthcare",
        "Education",
        "Salary",
        "Freelance",
        "Investment",
        "Other"
    ]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT OR IGNORE INTO categories(user_id, name)
        VALUES(?, ?)
        """,
        [
            (user_id, category)
            for category in default_categories
        ]
    )

    conn.commit()
    conn.close()


def add_category(user_id, category_name):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO categories(user_id, name)
            VALUES(?, ?)
            """,
            (
                user_id,
                category_name.strip()
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def delete_category(user_id, category_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM categories
        WHERE user_id=?
        AND name=?
        """,
        (
            user_id,
            category_name
        )
    )

    conn.commit()
    conn.close()
def delete_category(
    user_id,
    category_name
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM categories
        WHERE
            user_id=?
        AND
            name=?
        """,
        (
            user_id,
            category_name
        )
    )

    conn.commit()

    conn.close()
