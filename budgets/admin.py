"""Настройки админ-панели приложения budgets."""

from django.contrib import admin

from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """Админ-класс для модели Budget."""
