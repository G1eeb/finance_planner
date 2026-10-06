"""Маршруты приложения budgets."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.budgets, name="budgets"),
    path("<int:budget_id>/", views.budget_detail, name="budget_detail"),
]
