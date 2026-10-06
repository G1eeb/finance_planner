"""View-функции приложения goals."""

from django.http import HttpResponse


def goals(request):
    """Список целей."""
    return HttpResponse("Список целей")


def goal_detail(request, goal_id):
    """Страница отдельной цели."""
    return HttpResponse(f"Цель {goal_id}")
