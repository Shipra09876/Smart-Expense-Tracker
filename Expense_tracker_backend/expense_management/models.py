from django.db import models
from user_management.models import User
from django.conf import settings

# Create your models here.
User=settings.AUTH_USER_MODEL

class Category(models.Model):
    user=models.ForeignKey(User,related_name='custom_categories',on_delete=models.CASCADE,blank=True,null=True)
    category_choice=[
        ('housing',"Housing"),
        ('transportation',"Transportation"),
        ('utilities','Utilities'),
        ('insurance','Insurance'),
        ('debt-payment','Debt-Payment'),
        ('clothing',"Clothing"),
        ('childcare',"Childcare"),
        ('entertainment',"Entertainment"),
        ('health-care',"Health-care"),
        ('gifts',"Gifts"),
        ('rent',"Rent"),
        ('subcription',"Subcription"),
        ('food',"Food"),
        ('gas',"Gas"),
    ]
    category_name=models.CharField(max_length=100)

    is_default=models.BooleanField(default=False)

    class Meta:
        unique_together=('category_name','user','is_default')
        
    def __str__(self):
        return self.category_name

class Expense(models.Model):
    user=models.ForeignKey(User,related_name='expenses',on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=100)
    category=models.ForeignKey(Category,related_name='expenses',on_delete=models.CASCADE)

    Payment_choices=[
        ("UPI","upi"),
        ("Card","card"),
        ("Cash","cash")
    ]
    payment_method=models.CharField(max_length=100,blank=True,choices=Payment_choices,null=True)
    expense_amount=models.DecimalField(max_digits=10,decimal_places=2)
    expense_date=models.DateField()
    is_recurring=models.BooleanField(default=False)

    Recurring_choice=[
        ("daily","Daily"),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    recurring_type=models.CharField(max_length=10,choices=Recurring_choice,blank=True,null=True)

    def __str__(self):
        return f"{self.title}->{self.expense_amount}"


class Income(models.Model):
    user=models.ForeignKey(User,related_name='incomes',on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=15,decimal_places=2)
    source=models.CharField(max_length=100,blank=True)
    month=models.IntegerField(choices=[(i, str(i)) for i in range(1, 13)])
    year=models.IntegerField()
    received_on=models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'month', 'year','source')

    def __str__(self):
        return f"{self.user} - ₹{self.amount}"

class Budget(models.Model):
    user=models.ForeignKey(User,related_name='budgets',on_delete=models.CASCADE)
    category=models.ForeignKey(Category,related_name='budgets',on_delete=models.CASCADE)
    budget_amount=models.DecimalField(max_digits=10,decimal_places=2)
    
    month=models.IntegerField(choices=[(i, str(i)) for i in range(1, 13)])
    year=models.IntegerField()

    class Meta:
        unique_together=('user','category','month','year')

    def __str__(self):
        return f"{self.user.name}->{self.category.category_name}"
    
class Wallet(models.Model):
    user=models.ForeignKey(User,related_name="wallet_user",on_delete=models.CASCADE)
    main_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.00,) # main wallet store available amount 
    saving_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)

    def __str__(self):
        return f"{self.user.username}->{self.main_balance}->{self.saving_balance}"

class RecurringExpense(models.Model):
    user=models.ForeignKey(User,related_name="recurring_expense",on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    emi_amount=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    Choices = [
        ("daily", "Daily"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly")
    ]
    frequency=models.CharField(max_length=120,choices=Choices)
    start_date=models.DateField()
    end_date=models.DateField(null=True,blank=True)
    active=models.BooleanField(default=True)
    next_due_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.name}"

class FD(models.Model):
    user=models.ForeignKey(User,related_name="Saving_amount",on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    target_amount=models.DecimalField(max_digits=50,decimal_places=2,default=0.00)
    monthly_payment=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    current_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    start_date=models.DateField()
    maturity_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}-{self.name}-{self.monthly_payment}"
    

