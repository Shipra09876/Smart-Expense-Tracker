import django_filters
from .models import *

class ExpenseFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="expense_date", lookup_expr="year")
    month = django_filters.NumberFilter(field_name="expense_date", lookup_expr="month")
    category_name = django_filters.CharFilter(field_name='category__category_name', lookup_expr='iexact')

    min_amount = django_filters.NumberFilter(field_name="expense_amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="expense_amount", lookup_expr="lte")
    start_date = django_filters.DateFilter(field_name="expense_date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="expense_date", lookup_expr="lte")

    class Meta:
        model = Expense
        fields = ["category", "payment_method", "min_amount", "max_amount", "start_date", "end_date"]


class BudgetFilter(django_filters.FilterSet):
    month=django_filters.NumberFilter(field_name="month",lookup_expr="exact")
    year=django_filters.NumberFilter(field_name="year",lookup_expr="exact")

    class Meta:
        model=Budget
        fields=["month","year"]