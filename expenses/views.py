"""View-функции приложения expenses."""

from django.shortcuts import render

from models.expenses import find_expense_by_id
from storage import load_expenses

EXPENSES_FILE = "data/expenses.json"


def expenses(request):
    """Список расходов."""
    expenses_list = load_expenses(EXPENSES_FILE)
    context = {
        "expenses": expenses_list,
    }
    return render(request, "expenses/expense_list.html", context)


def expense_detail(request, expense_id):
    """Страница отдельного расхода."""
    expenses_list = load_expenses(EXPENSES_FILE)
    expense = find_expense_by_id(expenses_list, expense_id)

    context = {
        "expense": expense,
    }
    return render(
        request,
        "expenses/expense_detail.html",
        context,
        status=404 if expense is None else 200,
    )
