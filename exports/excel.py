from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font


def export_transactions_excel(df):

    wb = Workbook()

    ws = wb.active

    ws.title = "Transactions"

    headers = [
        "Date",
        "Type",
        "Category",
        "Amount",
        "Description"
    ]

    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for row in df.itertuples():

        ws.append([
            row.date,
            row.type,
            row.category,
            row.amount,
            row.description
        ])

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return output