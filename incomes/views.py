"""View-функции приложения incomes (Django ORM)."""

from datetime import datetime
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Count, F, Sum
from django.shortcuts import get_object_or_404, render

from categories.models import Category
from incomes.models import Income


SORT_FIELDS = {
    "-date": "-date",
    "date": "date",
    "-amount": "-amount",
    "amount": "amount",
    "category": "category__name",
    "-category": "-category__name",
}


def _parse_decimal(value):
    """Попытаться превратить строку в Decimal. Вернуть None при ошибке."""
    if not value:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def incomes(request):
    """Список доходов с фильтрами, сортировкой и пагинацией."""
    q = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    exclude_category_id = request.GET.get(
        "exclude_category", ""
    ).strip()
    amount_min = request.GET.get("amount_min", "").strip()
    amount_max = request.GET.get("amount_max", "").strip()
    sort = request.GET.get("sort", "-date")

    qs = Income.objects.select_related("category")

    if q:
        qs = qs.filter(category__name__icontains=q)

    if category_id.isdigit():
        qs = qs.filter(category_id=int(category_id))

    if exclude_category_id.isdigit():
        qs = qs.exclude(category_id=int(exclude_category_id))

    d_min = _parse_decimal(amount_min)
    if d_min is not None:
        qs = qs.filter(amount__gte=d_min)

    d_max = _parse_decimal(amount_max)
    if d_max is not None:
        qs = qs.filter(amount__lte=d_max)

    sort_field = SORT_FIELDS.get(sort, "-date")
    qs = qs.order_by(sort_field)

    totals = qs.aggregate(
        total=Sum("amount"),
        cnt=Count("id"),
    )

    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)
    base_qs = urlencode(params)
    page_url_prefix = f"?{base_qs}&" if base_qs else "?"

    categories = Category.objects.order_by("name")

    context = {
        "incomes": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "q": q,
        "selected_category": category_id,
        "exclude_category": exclude_category_id,
        "amount_min": amount_min,
        "amount_max": amount_max,
        "sort": sort,
        "total_sum": totals["total"] or Decimal("0"),
        "total_count": totals["cnt"] or 0,
        "page_url_prefix": page_url_prefix,
    }
    return render(request, "incomes/income_list.html", context)


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

    categories_without = Category.objects.filter(
        incomes__isnull=True
    ).order_by("name")

    return render(
        request,
        "incomes/income_statistics.html",
        {
            "stats": stats,
            "categories_without": categories_without,
        },
    )
