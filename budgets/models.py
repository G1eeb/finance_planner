"""Django-модели приложения budgets."""

from django.db import models


class Budget(models.Model):
    """Месячный бюджет."""

    month = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="Месяц (ГГГГ-ММ)",
    )
    monthly_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Бюджет на месяц",
    )
    current_expenses = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Потрачено за месяц",
    )

    class Meta:
        ordering = ["-month"]
        verbose_name = "Бюджет"
        verbose_name_plural = "Бюджеты"

    def __str__(self):
        return f"Бюджет {self.month}"

    @property
    def remaining(self):
        """Остаток бюджета."""
        return self.monthly_budget - self.current_expenses

    @property
    def is_overspent(self):
        """Превышен ли бюджет."""
        return self.current_expenses > self.monthly_budget

    def can_afford(self, amount):
        """Проверить, возможна ли планируемая трата."""
        return amount <= self.remaining
