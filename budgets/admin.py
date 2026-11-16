"""Настройки админ-панели приложения budgets."""

from django.contrib import admin

from .models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """Админ-класс для модели Budget."""

    list_display = (
        "id",
        "month",
        "monthly_budget",
        "current_expenses",
        "remaining_display",
        "is_overspent_display",
    )
    list_display_links = ("id", "month")
    list_filter = ("month",)
    search_fields = ("month",)
    ordering = ("-month",)
    list_per_page = 20

    @admin.display(description="Остаток")
    def remaining_display(self, obj):
        """Остаток бюджета."""
        return f"{obj.remaining:.2f} руб."

    @admin.display(description="Превышение", boolean=True)
    def is_overspent_display(self, obj):
        """Признак превышения бюджета."""
        return obj.is_overspent
