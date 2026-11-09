"""Django-модели приложения incomes."""

from django.db import models

from categories.models import Category


class Income(models.Model):
    """Доход — поступление денежных средств."""

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Сумма",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="incomes",
        verbose_name="Категория",
    )
    date = models.DateField(
        verbose_name="Дата",
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "Доход"
        verbose_name_plural = "Доходы"

    def __str__(self):
        return f"{self.amount} — {self.category}"
