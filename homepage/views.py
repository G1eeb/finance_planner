"""View-функции приложения homepage."""

from django.http import HttpResponse


def index(request):
    """Главная страница приложения."""
    return HttpResponse("Finance Planner — сервис финансового планирования")
