"""View-функции приложения incomes (Django ORM)."""

from datetime import datetime

from django.db.models import Count, F, Sum
from django.shortcuts import get_object_or_404, render

from incomes.models import Income


def incomes(request):
    """Список доходов из БД через ORM."""
    incomes_list = (
        Income.objects
        .annotate(category_name=F("category__name"))
        .order_by("-date")
    )
    return render(
        request,
        "incomes/income_list.html",
        {"incomes": incomes_list},
    )


def income_detail(request, income_id):
    """Карточка дохода из БД через ORM."""
    income = get_object_or_404(
        Income.objects.select_related("category"),
        pk=income_id,
    )
    return render(
        request,
        "incomes/income_detail.html",
        {"income": income},
    )


def income_filter(request):
    """Поиск доходов по диапазону дат через ORM."""
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    error = None
    incomes_list = []

    if date_from and date_to:
        try:
            d_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            d_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректные даты в формате ГГГГ-ММ-ДД."
        else:
            incomes_list = (
                Income.objects
                .filter(date__range=(d_from, d_to))
                .annotate(category_name=F("category__name"))
                .order_by("-date")
            )

    return render(
        request,
        "incomes/income_filter.html",
        {
            "incomes": incomes_list,
            "date_from": date_from,
            "date_to": date_to,
            "error": error,
        },
    )


def income_statistics(request):
    """Статистика доходов по категориям через ORM."""
    stats = (
        Income.objects
        .values(category_name=F("category__name"))
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )
    return render(
        request,
        "incomes/income_statistics.html",
        {"stats": stats},
    )
