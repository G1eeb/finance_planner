"""View-функции приложения homepage."""

from django.http import HttpResponse

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
