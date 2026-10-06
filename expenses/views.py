"""View-функции приложения expenses."""

from django.http import HttpResponse

from homepage.views import page
from models.expenses import find_expense_by_id
from storage import load_expenses

EXPENSES_FILE = "data/expenses.json"


def expenses(request):
    """Список расходов."""
    expenses_list = load_expenses(EXPENSES_FILE)

    if not expenses_list:
        content = """
        <h1>Расходы</h1>
        <p class="text-muted">Расходов пока нет.</p>
        <a href="/" class="btn btn-outline-secondary">На главную</a>
        """
        return HttpResponse(page("Finance Planner — расходы", content))

    items = ""
    for expense in expenses_list:
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/expenses/{expense.id}/">
                {expense.amount:.2f} руб. — {expense.category}
            </a>
            <span class="badge bg-danger">{expense.date}</span>
        </li>
        """
    content = f"""
    <h1>Расходы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Finance Planner — расходы", content))


def expense_detail(request, expense_id):
    """Страница отдельного расхода."""
    expenses_list = load_expenses(EXPENSES_FILE)
    expense = find_expense_by_id(expenses_list, expense_id)

    if expense is None:
        content = """
        <h1 class="text-danger">Расход не найден</h1>
        <a href="/expenses/" class="btn btn-outline-secondary">
            ← к списку расходов
        </a>
        """
        return HttpResponse(
            page("Расход не найден", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Расход №{expense.id}</h5>
            <p class="card-text">
                <strong>Сумма:</strong> {expense.amount:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Категория:</strong> {expense.category}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {expense.date}
            </p>
            <a href="/expenses/" class="btn btn-outline-secondary">
                ← к списку расходов
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Расход №{expense.id}", content),
        status=200,
    )
