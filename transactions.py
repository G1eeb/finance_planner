"""Модуль работы с операциями (доходами и расходами)."""


def add_transaction(transactions: list[dict], type_: str, amount: float,
                    category: str, date: str) -> dict:
    """Добавить операцию и вернуть её.
    Проверяет тип операции и положительность суммы.
    """
    if type_ not in ("income", "expense"):
        raise ValueError(f"Недопустимый тип операции: {type_}")
    if amount <= 0:
        raise ValueError("Сумма должна быть положительной.")

    transaction_id = max((t["id"] for t in transactions), default=0) + 1
    transaction = {
        "id": transaction_id,
        "type": type_,
        "amount": amount,
        "category": category,
        "date": date,
    }
    transactions.append(transaction)
    return transaction


def find_transactions_by_category(transactions: list[dict],
                                  query: str) -> list[dict]:
    """Найти операции, в категории которых есть подстрока query."""
    query_lower = query.lower()
    return [
        t for t in transactions
        if query_lower in t["category"].lower()
    ]


def filter_transactions_by_date(transactions: list[dict],
                                start_date: str,
                                end_date: str):
    """Отобрать операции за период [start_date, end_date].
    Возвращает генератор.
    """
    return (
        t for t in transactions
        if start_date <= t["date"] <= end_date
    )


def sort_transactions_by_amount(transactions: list[dict]) -> list[dict]:
    """Отсортировать операции по сумме по убыванию."""
    return sorted(transactions, key=lambda t: t["amount"], reverse=True)


def total_by_type(transactions: list[dict], type_: str) -> float:
    """Подсчитать сумму операций заданного типа."""
    return sum(t["amount"] for t in transactions if t["type"] == type_)


def category_statistics(transactions: list[dict]) -> dict[str, float]:
    """Собрать статистику расходов по категориям."""
    stats: dict[str, float] = {}
    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]
            stats[category] = stats.get(category, 0.0) + t["amount"]
    return stats
