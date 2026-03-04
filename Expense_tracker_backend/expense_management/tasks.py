from celery import shared_task
from django.contrib.auth import get_user_model
from expense_management.Utils.expense_utils import generate_recurring_expense, deduct_fd_from_saving
from datetime import date
from expense_management.Utils.report_utils import get_monthly_report
from expense_management.Utils.pdf_utils import generate_pdf
from expense_management.Utils.email_utils import send_report_email
from .models import *
from django.utils import timezone


User = get_user_model()

@shared_task
def deduct_emi_task():
    for user in User.objects.all():
        generate_recurring_expense(user)
    return "EMI deducted successfully"

@shared_task
def add_fd_interest_task():
    for user in User.objects.all():
        deduct_fd_from_saving(user)
    return "FD interest added successfully"


def send_monthly_reports_func(month=None, year=None):
    """Reusable function for generating and sending reports."""
    today = timezone.now()

    if not month:
        month = today.month - 1 if today.month > 1 else 12
    if not year:
        year = today.year if today.month > 1 else today.year - 1

    expenses = Expense.objects.filter(
        expense_date__month=month, expense_date__year=year
    )

    users = User.objects.all()
    for user in users:
        try:
            data = get_monthly_report(user, month, year)
            pdf_path = generate_pdf(user, data)
            send_report_email(user, pdf_path, month, year)
            print(f"✅ Report sent for {user.email}")
        except Exception as e:
            print(f"❌ Error for {user.email}: {str(e)}")


@shared_task
def send_monthly_reports(month=None, year=None):
    """Celery task wrapper"""
    return send_monthly_reports_func(month, year)

@shared_task
def test_task():
    print("Celery is working ")
    return "Task completed"