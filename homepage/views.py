"""View-функции приложения homepage."""

from django.http import HttpResponse

from budget import calculate_budget, check_budget

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)


def page(title, content):
    """Собрать HTML-страницу с общим каркасом."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Finance Planner</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/transactions/">Операции</a>
                <a class="nav-link" href="/goals/">Цели</a>
                <a class="nav-link" href="/budget/">Бюджет</a>
            </div>
        </div>
    </nav>
    <div class="container">
        {content}
    </div>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Finance Planner</h1>
    <p class="lead">Сервис финансового планирования.</p>
    <p>Основные разделы:</p>
    <a href="/transactions/" class="btn btn-primary me-2">Операции</a>
    <a href="/goals/" class="btn btn-secondary me-2">Цели</a>
    <a href="/budget/" class="btn btn-outline-primary">Проверить бюджет</a>
    """
    return HttpResponse(page("Finance Planner", content))


def budget_check(request):
    """Разовый расчёт: возможна ли планируемая трата."""
    monthly = request.GET.get("monthly")
    expenses = request.GET.get("expenses")
    planned = request.GET.get("planned")

    if monthly and expenses and planned:
        try:
            monthly_f = float(monthly)
            expenses_f = float(expenses)
            planned_f = float(planned)

            remaining, after = calculate_budget(
                monthly_f, expenses_f, planned_f
            )
            status, warning = check_budget(
                planned_f, remaining, after
            )

            is_ok = "возможна" in status
            alert_class = "alert-success" if is_ok else "alert-danger"

            result = f"""
            <div class="alert {alert_class}">
                <p><strong>Остаток бюджета:</strong>
                   {remaining:.2f} руб.</p>
                <p><strong>После траты:</strong>
                   {after:.2f} руб.</p>
                <p><strong>Статус:</strong> {status}</p>
                <p><strong>Примечание:</strong> {warning}</p>
            </div>
            """
        except ValueError:
            result = """
            <div class="alert alert-warning">
                Некорректные данные. Введите числа.
            </div>
            """
    else:
        result = """
        <p class="text-muted">
            Введите параметры в адресной строке:<br>
            <code>/budget/?monthly=60000&expenses=42500&planned=15000</code>
        </p>
        """

    content = f"""
    <h1>Проверка бюджета</h1>
    <p class="lead">Разовая проверка: возможна ли планируемая трата.</p>
    {result}
    <a href="/" class="btn btn-outline-secondary">На главную</a>
    """
    return HttpResponse(page("Finance Planner — бюджет", content))


def page_not_found(request, exception):
    """Кастомная страница 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
