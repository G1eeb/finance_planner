"""Настройки админ-панели приложения incomes."""

from django.contrib import admin

from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    """Админ-класс для модели Income."""

    list_display = ("id", "amount", "category", "date")
    list_display_links = ("id", "amount")
    list_filter = ("category", "date")
    search_fields = ("category__name",)
    ordering = ("-date",)
    date_hierarchy = "date"
    list_select_related = ("category",)
    list_per_page = 20
