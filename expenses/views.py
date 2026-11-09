"""View-функции приложения expenses (Django ORM)."""

from datetime import datetime

from django.db.models import Count, F, Sum
from django.shortcuts import get_object_or_404, render

from expenses.models import Expense


def expenses(request):
    """Список расходов из БД через ORM."""
    expenses_list = (
        Expense.objects
        .annotate(category_name=F("category__name"))
        .order_by("-date")
    )
    return render(
        request,
        "expenses/expense_list.html",
        {"expenses": expenses_list},
    )


def expense_detail(request, expense_id):
    """Карточка расхода из БД через ORM."""
    expense = get_object_or_404(
        Expense.objects.select_related("category"),
        pk=expense_id,
    )
    return render(
        request,
        "expenses/expense_detail.html",
        {"expense": expense},
    )


def expense_filter(request):
    """Поиск расходов по диапазону дат через ORM."""
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    error = None
    expenses_list = []

    if date_from and date_to:
        try:
            d_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            d_to = datetime.strptime(date_to, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректные даты в формате ГГГГ-ММ-ДД."
        else:
            expenses_list = (
                Expense.objects
                .filter(date__range=(d_from, d_to))
                .annotate(category_name=F("category__name"))
                .order_by("-date")
            )

    return render(
        request,
        "expenses/expense_filter.html",
        {
            "expenses": expenses_list,
            "date_from": date_from,
            "date_to": date_to,
            "error": error,
        },
    )


def expense_statistics(request):
    """Статистика расходов по категориям через ORM."""
    stats = (
        Expense.objects
        .values(category_name=F("category__name"))
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )
    return render(
        request,
        "expenses/expense_statistics.html",
        {"stats": stats},
    )
