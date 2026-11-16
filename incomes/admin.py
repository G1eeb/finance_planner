"""Настройки админ-панели приложения incomes."""

from django.contrib import admin

from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    """Админ-класс для модели Income."""
