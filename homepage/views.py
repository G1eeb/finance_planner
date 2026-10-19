"""View-функции приложения homepage."""

from django.http import HttpResponse
from django.shortcuts import render

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
                <a class="nav-link" href="/incomes/">Доходы</a>
                <a class="nav-link" href="/expenses/">Расходы</a>
                <a class="nav-link" href="/budgets/">Бюджеты</a>
            </div>
        </div>
    </nav>
    <div class="container">
        {content}
    </div>
</body>
</html>"""


def index(request):
    return render(request, "homepage/index.html")


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
