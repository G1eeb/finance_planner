"""Django-модели приложения categories."""

from django.db import models


class Category(models.Model):
    """Категория дохода или расхода."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название категории",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
