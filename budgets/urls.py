from django.urls import path
from . import views

app_name = "budgets"

urlpatterns = [
    path("", views.budgets, name="list"),
    path("<int:budget_id>/", views.budget_detail, name="detail"),
]
