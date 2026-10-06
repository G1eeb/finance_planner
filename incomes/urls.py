"""Маршруты приложения incomes."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.incomes, name="incomes"),
    path("<int:income_id>/", views.income_detail, name="income_detail"),
]
