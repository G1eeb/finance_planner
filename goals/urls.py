"""Маршруты приложения goals."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.goals, name="goals"),
    path("<int:goal_id>/", views.goal_detail, name="goal_detail"),
]
