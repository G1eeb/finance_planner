"""Настройки админ-панели приложения categories."""

from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-класс для модели Category."""
