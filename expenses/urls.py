from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.expenses, name="list"),
    path("filter/", views.expense_filter, name="filter"),
    path("statistics/", views.expense_statistics, name="statistics"),
    path("<int:expense_id>/", views.expense_detail, name="detail"),
]
