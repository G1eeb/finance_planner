"""Настройки админ-панели приложения categories."""

from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-класс для модели Category."""

    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20
