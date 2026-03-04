from django.contrib import admin
from .models import *

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display=['user','title','description','category','expense_amount','payment_method','expense_date','is_recurring','recurring_type']
    search_fields=['category','expense_date','is_recurring']
    list_filter=['recurring_type']

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display=['user','amount','source','month','year','received_on']
    search_fields=['user','amount','source']
    list_filter=['month','year','received_on']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['user','category_name']
    search_fields=['category_name']
    list_filter=['category_name']

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display=['user','category','budget_amount','month','year']
    search_fields=['user','category','budget_amount']
    list_filter=['month','year']

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display=['user','main_balance','saving_balance']
    search_fields=['user','main_balance']

@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display=['user','name','emi_amount','frequency','start_date','end_date','active','next_due_date','created_at']
    search_fields=['name','active','start_date']

@admin.register(FD)
class FDAdmin(admin.ModelAdmin):
    list_display=['user','name','target_amount','monthly_payment','current_balance','start_date','maturity_date','active','created_at']
    search_fields=['name','start_date','active']



