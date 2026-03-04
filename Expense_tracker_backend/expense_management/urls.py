from .views import *
from django.urls import path

urlpatterns=[
    path('add_income/',AddIncome.as_view(),name='Add-income'),
    path('edit_income/<int:pk>/',EditIncome.as_view(),name='edit-income'),
    path('ListIncome/',ViewIncome.as_view(),name='List-income'),
    path('ListIncome/<int:pk>/',ViewIncomeById.as_view(),name='List-income-id'),

    path("get_wallet/",GetWalletBalance.as_view(),name='Wallet-balance'),
    path("transfer_to_saving/",TransferMoneyToSaving.as_view(),name='Transfer-to-saving'),
    #  and transfer to main wallet
    path("withdraw_from_saving/",WithdrawSaving.as_view(),name='Withdraw-from-saving'),
    
    path("add_category/",CategoryListCreate.as_view(),name="Create-category"),
    path("list_category/",CategoryListCreate.as_view(),name="list-category"),

    # by user 
    path('add_expense/',AddExpense.as_view(),name='Add-expense'),
    path('get_expense/',GetExpense.as_view(),name='Get-expense'),
    path('edit_expense/<int:uid>/',EditExpense.as_view(),name='Edit-expense'),
    path('delete_expense/<int:uid>/',DeleteExpense.as_view(),name='Delete-expense'),

    # Recurring Expenses
    path("add_recurring_expense/",AddRecurringExpense.as_view(),name="add-recurring-expense"),
    path("get_recurring_expense/",GetRecurringExpense.as_view(),name="get-recurring-expense"),
    path("recurring_expense/<int:pk>/",RecurringExpenseById.as_view(),name="get-recurring-expense-by-id"),

    # FD's expenses 
    path("add_goal/",AddGoal.as_view(),name="add-goal"),
    path("get_goal/",GetGaol.as_view(),name="get-goal"),
    path("get_goal/<int:pk>/",GetGoalByID.as_view(),name="get-goal-by-id"),

    # Budget set per category 
    path("budget/upsert/",BudgetUpsert.as_view(),name="budget-upsert"),
    path("budget_list/",BudgetList.as_view(),name="Budget-list"),
    path("budget_details/<int:pk>/",BudgetDetails.as_view(),name="Budget-details"),
    path("budget_summary/",BudgetSummary.as_view(),name="Budget-summary")
]   