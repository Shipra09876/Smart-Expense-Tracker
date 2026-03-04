from expense_management.models import *
from datetime import date

def generate_recurring_expense(user):
    # store current date 
    today=date.today()
    # emis which are active 
    emis=RecurringExpense.objects.filter(user=user,active=True)

    for emi in emis:
        # check with date range
        if emi.start_date<=today and (not emi.end_date or today<=emi.end_date):
            # deduct from wallet 
            wallet=Wallet.objects.get(user=user)
            if wallet.main_balance>=emi.emi_amount:
                wallet.main_balance-=emi.emi_amount
                wallet.save()

                # expense as object
                Expense.objects.create(
                    user=user,
                    category="EMI",
                    amount=emi.emi_amount,
                    description=emi.name
                )
    
# For FD's
def deduct_fd_from_saving(user):
    wallet=Wallet.objects.get(user=user)
    goals=FD.objects.filter(user=user,active=True)

    for goal in goals:
        if wallet.saving_balance>=goal.monthly_payment:
            wallet.saving_balance-=goal.monthly_payment
            wallet.save()

            goal.current_balance+=goal.monthly_payment
            goal.save()

            
