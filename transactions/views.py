"""View-функции приложения transactions."""

from django.http import HttpResponse

from homepage.views import page
from models.transactions import find_transaction_by_id
from storage import load_transactions

TRANSACTIONS_FILE = "data/transactions.json"


def transactions(request):
    """Список операций."""
    transactions_list = load_transactions(TRANSACTIONS_FILE)

    if not transactions_list:
        content = """
        <h1>Операции</h1>
        <p class="text-muted">Операций пока нет.</p>
        <a href="/" class="btn btn-outline-secondary">На главную</a>
        """
        return HttpResponse(page("Finance Planner — операции", content))

    items = ""
    for t in transactions_list:
        type_ru = "Доход" if t.is_income() else "Расход"
        badge = "bg-success" if t.is_income() else "bg-danger"
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/transactions/{t.id}/">
                {type_ru}: {t.amount:.2f} руб. — {t.category}
            </a>
            <span class="badge {badge}">{t.date}</span>
        </li>
        """
    content = f"""
    <h1>Операции</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Finance Planner — операции", content))


def transaction_detail(request, transaction_id):
    """Страница отдельной операции."""
    transactions_list = load_transactions(TRANSACTIONS_FILE)
    transaction = find_transaction_by_id(transactions_list, transaction_id)

    if transaction is None:
        content = """
        <h1 class="text-danger">Операция не найдена</h1>
        <a href="/transactions/" class="btn btn-outline-secondary">
            ← к списку операций
        </a>
        """
        return HttpResponse(
            page("Операция не найдена", content),
            status=404,
        )

    type_ru = "Доход" if transaction.is_income() else "Расход"
    badge = "bg-success" if transaction.is_income() else "bg-danger"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{type_ru} №{transaction.id}</h5>
            <p class="card-text">
                <strong>Сумма:</strong> {transaction.amount:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Категория:</strong> {transaction.category}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {transaction.date}
            </p>
            <p class="card-text">
                Тип: <span class="badge {badge}">{type_ru}</span>
            </p>
            <a href="/transactions/" class="btn btn-outline-secondary">
                ← к списку операций
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Операция №{transaction.id}", content),
        status=200,
    )
