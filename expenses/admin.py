"""Настройки админ-панели приложения expenses."""

from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Админ-класс для модели Expense."""
