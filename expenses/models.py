"""Django-модели приложения expenses."""

from django.db import models

from categories.models import Category


class Expense(models.Model):
    """Расход — списание денежных средств."""

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Сумма",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="expenses",
        verbose_name="Категория",
    )
    date = models.DateField(
        verbose_name="Дата",
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"

    def __str__(self):
        return f"{self.amount} — {self.category}"
