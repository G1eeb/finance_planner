"""Настройки админ-панели приложения expenses."""

from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Админ-класс для модели Expense."""

    list_display = ("id", "amount", "category", "date")
    list_display_links = ("id", "amount")
    list_filter = ("category", "date")
    search_fields = ("category__name",)
    ordering = ("-date",)
    date_hierarchy = "date"
    list_select_related = ("category",)
    list_per_page = 20
