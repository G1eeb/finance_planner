"""View-функции приложения budgets."""

from django.shortcuts import render

from models.budgets import find_budget_by_id
from storage import load_budgets

BUDGETS_FILE = "data/budgets.json"


def budgets(request):
    """Список бюджетов."""
    budgets_list = load_budgets(BUDGETS_FILE)
    context = {
        "budgets": budgets_list,
    }
    return render(request, "budgets/budget_list.html", context)


def budget_detail(request, budget_id):
    """Страница бюджета с калькулятором (GET-параметр planned)."""
    budgets_list = load_budgets(BUDGETS_FILE)
    budget = find_budget_by_id(budgets_list, budget_id)

    if budget is None:
        return render(
            request,
            "budgets/budget_detail.html",
            {"budget": None},
            status=404,
        )

    remaining = budget.get_remaining()
    planned_raw = request.GET.get("planned")

    context = {
        "budget": budget,
        "remaining": remaining,
        "error": None,
        "can_afford": None,
        "remaining_after": None,
        "overspend": None,
    }

    if planned_raw:
        try:
            planned = float(planned_raw)
            context["can_afford"] = budget.can_afford(planned)
            if context["can_afford"]:
                context["remaining_after"] = budget.get_remaining_after(
                    planned
                )
            else:
                context["overspend"] = planned - remaining
        except ValueError:
            context["error"] = (
                "Некорректное значение планируемой траты."
            )

    return render(
        request,
        "budgets/budget_detail.html",
        context,
        status=200,
    )
