"""View-функции приложения incomes."""

from django.http import HttpResponse

from homepage.views import page
from models.incomes import find_income_by_id
from storage import load_incomes

INCOMES_FILE = "data/incomes.json"


def incomes(request):
    """Список доходов."""
    incomes_list = load_incomes(INCOMES_FILE)

    if not incomes_list:
        content = """
        <h1>Доходы</h1>
        <p class="text-muted">Доходов пока нет.</p>
        <a href="/" class="btn btn-outline-secondary">На главную</a>
        """
        return HttpResponse(page("Finance Planner — доходы", content))

    items = ""
    for income in incomes_list:
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/incomes/{income.id}/">
                {income.amount:.2f} руб. — {income.category}
            </a>
            <span class="badge bg-success">{income.date}</span>
        </li>
        """
    content = f"""
    <h1>Доходы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Finance Planner — доходы", content))


def income_detail(request, income_id):
    """Страница отдельного дохода."""
    incomes_list = load_incomes(INCOMES_FILE)
    income = find_income_by_id(incomes_list, income_id)

    if income is None:
        content = """
        <h1 class="text-danger">Доход не найден</h1>
        <a href="/incomes/" class="btn btn-outline-secondary">
            ← к списку доходов
        </a>
        """
        return HttpResponse(
            page("Доход не найден", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Доход №{income.id}</h5>
            <p class="card-text">
                <strong>Сумма:</strong> {income.amount:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Категория:</strong> {income.category}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {income.date}
            </p>
            <a href="/incomes/" class="btn btn-outline-secondary">
                ← к списку доходов
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Доход №{income.id}", content),
        status=200,
    )
