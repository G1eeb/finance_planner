"""Маршруты приложения transactions."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.transactions, name="transactions"),
    path("<int:transaction_id>/", views.transaction_detail,
         name="transaction_detail"),
]
