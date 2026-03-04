from django.apps import AppConfig
from expense_management import signals

class ExpenseManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expense_management'

    def ready(self):
        import expense_management.signals
    