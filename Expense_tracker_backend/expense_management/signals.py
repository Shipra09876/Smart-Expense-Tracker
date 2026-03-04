from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_default_categories(sender,**kwargs):
    if sender.name=="expense_management":
        Category = apps.get_model("expense_management", "Category")  
        default_categories=[
            "Housing", "Transportation", "Utilities", "Insurance",
            "Debt-Payment", "Clothing", "Childcare", "Entertainment",
            "Health-care", "Gifts", "Rent", "Subscription",
            "Food", "Gas", "EMI", "FD","Others"
        ]

        for cat in default_categories:
            Category.objects.update_or_create(category_name=cat,is_default=True,defaults={"user":None})