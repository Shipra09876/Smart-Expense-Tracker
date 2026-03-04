from datetime import time,date
from calendar import monthrange
from decimal import Decimal
from django.db.models import Sum
from expense_management.models import *

def month_date_range(year,month):
    """Return (first_day, last_day) for given year/month."""
    first=date(year,month,1)
    last=date(year,month,monthrange(year,month)[1])

    return first,last

# how much a user spent in a category for that month
def calculate_monthly_spend(user,category_name,year,month):
    start,end=month_date_range(year,month)
    total=(Expense.objects.filter(
        user=user,
        category__category_name=category_name,
        expense_date__range=(start,end)
        ).aggregate(total=Sum('expense_amount'))['total']) or Decimal('0')
    return Decimal(total)

def get_budget_for_period(user,category,year,month):
    return Budget.objects.filter(
            user=user,
            category=category,
            year=year,
            month=month).first()

def remaining_budget(user,category,year,month):
    b=get_budget_for_period(user,category,year,month)
    if not b:
        return None
    
    spent=calculate_monthly_spend(user,category,year,month)
    budget_amt=Decimal(b.budget_amount)
    remaining=budget_amt-Decimal(spent)
    percent_used=float(Decimal(spent)/budget_amt*100) if budget_amt>0 else 0.0
    return {
        "budget":budget_amt,
        "spent":spent,
        'remaining':remaining,
        'precent used':percent_used 
    }

def check_budget_before_adding(user,category,year,month,new_amount):
    new_amount=Decimal(str(new_amount))
    info=remaining_budget(user, category, year, month)

    if info is None:
        return {
            "Ok":True,
            "reason":None,
            "remaining_after":None,
            "percent_after":None
        }
    
    remaining_after=info["remaining"]-new_amount
    percent_after=float(((info["spent"] + new_amount) / info["budget"]) * 100) if info["budget"] > 0 else 0.0
    reason=None
    
    if remaining_after<0:
        reason="Over Budget"
    elif  percent_after>=80:
        reason="Near limit"
    return {
        "ok": True, 
        "reason": reason, 
        "remaining_after": remaining_after, 
        "percent_after": percent_after
    }

def budgets_summary_for_month(user, year:int, month:int):
    """Return list of budgets for that month with spent/remaining/flags."""
    out = []
    qs = Budget.objects.filter(user=user, year=year, month=month)
    for b in qs:
        spent = calculate_monthly_spend(user, b.category.category_name, year, month)
        remaining = Decimal(b.budget_amount) - spent
        percent_used = float((spent / Decimal(b.budget_amount) * 100) if b.budget_amount > 0 else 0.0)

        out.append({
            "budget_id": b.id,
            "category_id": b.category.id,
            "category_name": b.category.category_name,
            "budget_amount": str(b.budget_amount),
            "spent_amount": str(spent),
            "remaining": str(remaining),
            "percent_used": round(percent_used, 2),
            "near_limit": percent_used >= 80 and percent_used <= 100,
            "over_budget": percent_used > 100,
            "month": b.month,
            "year": b.year,
        })

    return out