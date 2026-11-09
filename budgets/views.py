"""View-функции приложения budgets (Django ORM)."""

from django.shortcuts import get_object_or_404, render

from budgets.models import Budget


def budgets(request):
    """Список бюджетов из БД через ORM."""
    budgets_list = Budget.objects.order_by("-month")
    return render(
        request,
        "budgets/budget_list.html",
        {"budgets": budgets_list},
    )


def budget_detail(request, budget_id):
    """Бюджет с калькулятором (?planned=X) через ORM."""
    budget = get_object_or_404(Budget, pk=budget_id)

    planned_raw = request.GET.get("planned")
    context = {
        "budget": budget,
        "remaining": budget.remaining,
        "error": None,
        "can_afford": None,
        "remaining_after": None,
        "overspend": None,
    }

    if planned_raw:
        try:
            planned = float(planned_raw)
            if budget.can_afford(planned):
                context["can_afford"] = True
                context["remaining_after"] = (
                    budget.remaining - planned
                )
            else:
                context["can_afford"] = False
                context["overspend"] = (
                    planned - budget.remaining
                )
        except ValueError:
            context["error"] = (
                "Некорректное значение планируемой траты."
            )

    return render(
        request,
        "budgets/budget_detail.html",
        context,
    )
