"""View-функции приложения budgets."""

from django.http import HttpResponse

from homepage.views import page
from models.budgets import find_budget_by_id
from storage import load_budgets

BUDGETS_FILE = "data/budgets.json"


def budgets(request):
    """Список бюджетов."""
    budgets_list = load_budgets(BUDGETS_FILE)

    if not budgets_list:
        content = """
        <h1>Бюджеты</h1>
        <p class="text-muted">Бюджетов пока нет.</p>
        <a href="/" class="btn btn-outline-secondary">На главную</a>
        """
        return HttpResponse(page("Finance Planner — бюджеты", content))

    items = ""
    for budget in budgets_list:
        remaining = budget.get_remaining()
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/budgets/{budget.id}/">
                {budget.month}: бюджет {budget.monthly_budget:.2f} руб.,
                остаток {remaining:.2f} руб.
            </a>
        </li>
        """
    content = f"""
    <h1>Бюджеты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Finance Planner — бюджеты", content))


def budget_detail(request, budget_id):
    """Страница отдельного бюджета + разовый калькулятор."""
    budgets_list = load_budgets(BUDGETS_FILE)
    budget = find_budget_by_id(budgets_list, budget_id)

    if budget is None:
        content = """
        <h1 class="text-danger">Бюджет не найден</h1>
        <a href="/budgets/" class="btn btn-outline-secondary">
            ← к списку бюджетов
        </a>
        """
        return HttpResponse(
            page("Бюджет не найден", content),
            status=404,
        )

    remaining = budget.get_remaining()
    planned = request.GET.get("planned")

    if planned:
        try:
            planned_f = float(planned)
            if budget.can_afford(planned_f):
                after = budget.get_remaining_after(planned_f)
                alert = f"""
                <div class="alert alert-success">
                    Трата возможна. Остаток после: {after:.2f} руб.
                </div>
                """
            else:
                overspend = planned_f - remaining
                alert = f"""
                <div class="alert alert-danger">
                    Трата невозможна. Превышение: {overspend:.2f} руб.
                </div>
                """
        except ValueError:
            alert = """
            <div class="alert alert-warning">
                Некорректное значение планируемой траты.
            </div>
            """
    else:
        alert = (
            '<p class="text-muted">'
            'Добавьте параметр <code>?planned=15000</code> '
            'к URL, чтобы проверить трату.'
            '</p>'
        )

    content = f"""
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">Бюджет на {budget.month}</h5>
            <p class="card-text">
                <strong>Бюджет:</strong> {budget.monthly_budget:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Потрачено:</strong>
                {budget.current_expenses:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Остаток:</strong> {remaining:.2f} руб.
            </p>
        </div>
    </div>
    {alert}
    <a href="/budgets/" class="btn btn-outline-secondary">
        ← к списку бюджетов
    </a>
    """
    return HttpResponse(
        page(f"Бюджет {budget.month}", content),
        status=200,
    )
