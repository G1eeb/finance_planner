"""Корневая маршрутизация проекта Finance Planner."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("incomes/", include("incomes.urls")),
    path("expenses/", include("expenses.urls")),
    path("budgets/", include("budgets.urls")),
]

handler404 = "homepage.views.page_not_found"
