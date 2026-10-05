"""Тесты функций модуля transactions."""

from transactions import (
    add_transaction,
    total_by_type,
    find_transactions_by_category,
)


def test_add_transaction():
    """Операция добавляется в список с уникальным id."""
    transactions = []
    t = add_transaction(transactions, "expense", 15000, "Техника",
                        "2026-09-15")
    assert len(transactions) == 1
    assert t["id"] == 1
    assert t["amount"] == 15000


def test_total_by_type():
    """Сумма доходов и расходов считается раздельно."""
    transactions = []
    add_transaction(transactions, "income", 60000, "Зарплата", "2026-09-01")
    add_transaction(transactions, "expense", 15000, "Техника", "2026-09-15")
    add_transaction(transactions, "expense", 5000, "Кафе", "2026-09-16")

    assert total_by_type(transactions, "income") == 60000
    assert total_by_type(transactions, "expense") == 20000


def test_find_transactions_by_category():
    """Поиск по подстроке находит нужные операции."""
    transactions = []
    add_transaction(transactions, "expense", 15000, "Техника", "2026-09-15")
    add_transaction(transactions, "expense", 5000, "Кафе", "2026-09-16")

    found = find_transactions_by_category(transactions, "техн")
    assert len(found) == 1
    assert found[0]["category"] == "Техника"
