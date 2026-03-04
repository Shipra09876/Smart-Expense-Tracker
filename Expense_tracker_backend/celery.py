# expense_tracker_backend/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Expense_tracker_backend.settings")

app = Celery("Expense_tracker_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    "send-monthly-reports": {
        "task": "expense_management.tasks.send_monthly_reports",
        # "schedule": crontab(minute=0, hour=0, day_of_month=1), 
        "schedule": crontab(minute="*/2"),
    },
}
