"""View-функции приложения incomes."""

from django.shortcuts import render

from models.incomes import find_income_by_id
from storage import load_incomes

INCOMES_FILE = "data/incomes.json"


def incomes(request):
    """Список доходов."""
    incomes_list = load_incomes(INCOMES_FILE)
    context = {
        "incomes": incomes_list,
    }
    return render(request, "incomes/income_list.html", context)


def income_detail(request, income_id):
    """Страница отдельного дохода."""
    incomes_list = load_incomes(INCOMES_FILE)
    income = find_income_by_id(incomes_list, income_id)

    context = {
        "income": income,
    }
    return render(
        request,
        "incomes/income_detail.html",
        context,
        status=404 if income is None else 200,
    )
