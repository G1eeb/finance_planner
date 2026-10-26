"""View-функции приложения budgets."""

import sqlite3

from django.shortcuts import render

DB_PATH = "data/finance_planner.sqlite"


def budgets(request):
    """Список бюджетов из БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    budgets_list = conn.execute("""
        SELECT id, month, monthly_budget, current_expenses,
               (monthly_budget - current_expenses) AS remaining,
               CASE
                   WHEN current_expenses > monthly_budget THEN 1
                   ELSE 0
               END AS is_overspent
        FROM budgets
        ORDER BY month DESC
    """).fetchall()
    conn.close()

    return render(
        request,
        "budgets/budget_list.html",
        {"budgets": budgets_list},
    )


def budget_detail(request, budget_id):
    """Бюджет с калькулятором (?planned=X)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    budget = conn.execute("""
        SELECT id, month, monthly_budget, current_expenses,
               (monthly_budget - current_expenses) AS remaining,
               CASE
                   WHEN current_expenses > monthly_budget THEN 1
                   ELSE 0
               END AS is_overspent
        FROM budgets
        WHERE id = ?
    """, (budget_id,)).fetchone()
    conn.close()

    if budget is None:
        return render(
            request,
            "budgets/budget_detail.html",
            {"budget": None},
            status=404,
        )

    remaining = budget["remaining"]
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
            if planned <= remaining:
                context["can_afford"] = True
                context["remaining_after"] = remaining - planned
            else:
                context["can_afford"] = False
                context["overspend"] = planned - remaining
        except ValueError:
            context["error"] = "Некорректное значение планируемой траты."

    return render(request, "budgets/budget_detail.html", context)
