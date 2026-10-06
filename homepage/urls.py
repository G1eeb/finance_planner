"""Маршруты приложения homepage."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("budget/", views.budget_check, name="budget_check"),
]
