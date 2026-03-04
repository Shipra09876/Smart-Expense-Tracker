from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generate_pdf(user, data):
    filename = f"{user.username}_{data['month']}_{data['year']}_report.pdf"
    filepath = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)

    c = canvas.Canvas(filepath, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "Smart Expense Tracker Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"User: {user.username} ({user.email})")
    c.drawString(50, 740, f"Month: {data['month']} - Year: {data['year']}")

    c.drawString(50, 700, "Budget Summary")
    y = 680
    for summary in data["summary"]:  
        c.drawString(
            60, y,
            f"{summary['category_name']}: "
            f"Budget {summary['budget_amount']} | "
            f"Spent {summary['spent_amount']} | "
            f"Remaining {summary['remaining']}"
        )
        y -= 20

    c.drawString(50, y - 20, "Expenses:")
    y -= 40
    for exp in data["expenses"]:
        c.drawString(
            60, y,
            f"{exp['expense_date']} - {exp['category']} - {exp['title']} - {exp['amount']}"
        )
        y -= 20
        if y < 100:
            c.showPage()
            y = 800

    c.save()
    return filepath

