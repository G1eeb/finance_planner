"""Корневая маршрутизация проекта Finance Planner."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("transactions/", include("transactions.urls")),
    path("goals/", include("goals.urls")),
]
