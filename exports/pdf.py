from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def export_pdf(
    user_name,
    summary,
    budget,
    goal,
    df
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>Finance Tracker Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Generated for: {user_name}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            f"Income: ₹{summary['income']:,.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Expense: ₹{summary['expense']:,.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Balance: ₹{summary['balance']:,.2f}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,20))

    data = [
        [
            "Date",
            "Type",
            "Category",
            "Amount"
        ]
    ]

    for row in df.itertuples():

        data.append([
            row.date,
            row.type,
            row.category,
            f"₹{row.amount:,.2f}"
        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.grey),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

        ])

    )

    story.append(table)

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            f"Monthly Budget: ₹{budget['budget']:,.2f}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Remaining Budget: ₹{budget['remaining']:,.2f}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            f"Savings Goal: {goal['goal_name']}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Target: ₹{goal['target_amount']:,.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Current Savings: ₹{goal['current_amount']:,.2f}",
            styles["Normal"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer