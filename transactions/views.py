"""View-функции приложения transactions."""

from django.http import HttpResponse


def transactions(request):
    """Список операций."""
    return HttpResponse("Список операций")


def transaction_detail(request, transaction_id):
    """Страница отдельной операции."""
    return HttpResponse(f"Операция {transaction_id}")
