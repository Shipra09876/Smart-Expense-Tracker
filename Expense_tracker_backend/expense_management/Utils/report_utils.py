from django.db.models import Sum
from expense_management.models import Expense, Budget
from datetime import date

# def get_monthly_report(user, month=None, year=None):
#     today = date.today()
#     month = month or today.month
#     year = year or today.year

#     # Budget summary
#     budgets = Budget.objects.filter(user=user, month=month, year=year)
#     summary = []

#     for b in budgets:
#         spent_amount = Expense.objects.filter(
#             user=user,
#             category=b.category, 
#             expense_date__month=month,
#             expense_date__year=year
#         ).aggregate(total=Sum('expense_amount'))['total'] or 0

#         summary.append({
#             "budget_id": b.id,
#             "category_id": b.category.id,
#             "category_name": b.category.category_name,
#             "budget_amount": float(b.budget_amount),   
#             "spent_amount": float(spent_amount),
#             "remaining": float(b.budget_amount - spent_amount),
#             "percent_used": round((spent_amount / b.budget_amount * 100) if b.budget_amount else 0, 2),
#             "percent_used": float(round(percent_used, 2)),
#             "near_limit": spent_amount >= 0.9 * b.budget_amount,
#             "over_budget": spent_amount > b.budget_amount,
#             "month": month,
#             "year": year
#         })

#     # Expense details
#     expenses = Expense.objects.filter(
#         user=user,
#         expense_date__month=month,
#         expense_date__year=year
#     )

#     expenses_list = [
#         {
#             "expense_date": e.expense_date.strftime("%Y-%m-%d"),
#             "title": e.title,
#             "description": e.description,
#             "amount": float(e.expense_amount),
#             "category": e.category.category_name if e.category else "N/A"
#         }
#         for e in expenses
#     ]

#     return {
#         "month": month,
#         "year": year,
#         "summary": summary,
#         "expenses": expenses_list,
#         "total_spent": sum(e["amount"] for e in expenses_list),
#         "total_budget": sum(b["budget_amount"] for b in summary)
#     }

from decimal import Decimal

def get_monthly_report(user, month=None, year=None):
    today = date.today()
    month = month or today.month
    year = year or today.year

    budgets = Budget.objects.filter(user=user, month=month, year=year)
    summary = []

    for b in budgets:
        spent_amount = Expense.objects.filter(
            user=user,
            category=b.category,
            expense_date__month=month,
            expense_date__year=year
        ).aggregate(total=Sum('expense_amount'))['total'] or Decimal("0.00")

        # Keep calculations in Decimal
        percent_used = (
            (spent_amount / b.budget_amount * Decimal("100.00"))
            if b.budget_amount else Decimal("0.00")
        )

        summary.append({
            "budget_id": b.id,
            "category_id": b.category.id,
            "category_name": b.category.category_name,
            "budget_amount": float(b.budget_amount),   # convert for JSON
            "spent_amount": float(spent_amount),
            "remaining": float(b.budget_amount - spent_amount),
            "percent_used": float(round(percent_used, 2)),  # convert safely
            "near_limit": spent_amount >= Decimal("0.9") * b.budget_amount,
            "over_budget": spent_amount > b.budget_amount,
            "month": month,
            "year": year
        })

    expenses = Expense.objects.filter(
        user=user,
        expense_date__month=month,
        expense_date__year=year
    )

    expenses_list = [
        {
            "expense_date": e.expense_date.strftime("%Y-%m-%d"),
            "title": e.title,
            "description": e.description,
            "amount": float(e.expense_amount),   # convert at the edge
            "category": e.category.category_name if e.category else "N/A"
        }
        for e in expenses
    ]

    return {
        "month": month,
        "year": year,
        "summary": summary,
        "expenses": expenses_list,
        "total_spent": sum(e["amount"] for e in expenses_list),
        "total_budget": sum(b["budget_amount"] for b in summary)
    }


'''
3. Run Celery & Beat

In 2 terminals inside your project root:

# Terminal 1: run celery worker
celery -A Expense_tracker_backend worker -l info --pool=solo

# Terminal 2: run celery beat scheduler
celery -A Expense_tracker_backend beat -l info


✅ This will trigger your send_monthly_reports task based on crontab.


4. Test Manually Before Scheduling

Run the task directly in Django shell:

python manage.py shell

from expense_management.tasks import send_monthly_reports
send_monthly_reports()


It should create a reports/username_month_year_report.pdf

Send an email with the PDF attached ✅
'''