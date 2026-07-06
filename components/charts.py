import plotly.express as px


def expense_trend_chart(df):

    fig = px.line(
        df,
        x="date",
        y="amount",
        markers=True,
        title="Daily Expenses"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount",
        height=400
    )

    return fig


def expense_breakdown_chart(df):

    fig = px.pie(
        df,
        names="category",
        values="amount",
        hole=0.45
    )

    fig.update_layout(
        height=400
    )

    return fig