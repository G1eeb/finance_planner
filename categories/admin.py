"""Настройки админ-панели приложения categories."""

from django.contrib import admin

from expenses.models import Expense
from incomes.models import Income

from .models import Category


class IncomeInline(admin.TabularInline):
    """Встроенный список доходов в карточке категории."""

    model = Income
    extra = 0
    fields = ("amount", "date")
    readonly_fields = ("amount", "date")
    can_delete = False
    show_change_link = True


class ExpenseInline(admin.TabularInline):
    """Встроенный список расходов в карточке категории."""

    model = Expense
    extra = 0
    fields = ("amount", "date")
    readonly_fields = ("amount", "date")
    can_delete = False
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-класс для модели Category."""

    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20
    inlines = (IncomeInline, ExpenseInline)
