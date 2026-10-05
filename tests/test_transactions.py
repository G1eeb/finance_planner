"""Тесты класса Transaction и функций работы с операциями."""

from models import Transaction
from models.transactions import (
    add_transaction,
    find_transaction_by_id,
    find_transactions_by_category,
    sort_transactions_by_amount,
    total_by_type,
    category_statistics,
)


# ---------- Тесты класса Transaction ----------

def test_transaction_creation():
    """Объект Transaction создаётся с корректными атрибутами."""
    t = Transaction(1, "expense", 15000, "Техника", "2026-09-15")
    assert t.id == 1
    assert t.type == "expense"
    assert t.amount == 15000
    assert t.category == "Техника"
    assert t.date == "2026-09-15"


def test_transaction_str():
    """__str__ возвращает читаемое представление."""
    t = Transaction(1, "expense", 15000, "Техника", "2026-09-15")
    s = str(t)
    assert "Расход" in s
    assert "15000.00" in s
    assert "Техника" in s


def test_transaction_is_income_is_expense():
    """Методы is_income и is_expense работают корректно."""
    income = Transaction(1, "income", 60000, "Зарплата", "2026-09-01")
    expense = Transaction(2, "expense", 15000, "Техника", "2026-09-15")

    assert income.is_income()
    assert not income.is_expense()

    assert expense.is_expense()
    assert not expense.is_income()


def test_transaction_validation():
    """Некорректные тип и сумма вызывают ValueError."""
    import pytest

    with pytest.raises(ValueError):
        Transaction(1, "unknown", 100, "Тест", "2026-01-01")

    with pytest.raises(ValueError):
        Transaction(1, "income", -100, "Тест", "2026-01-01")


def test_transaction_from_dict_to_dict():
    """from_dict и to_dict корректно преобразуют данные."""
    data = {
        "id": 1, "type": "expense", "amount": 15000,
        "category": "Техника", "date": "2026-09-15",
    }
    t = Transaction.from_dict(data)

    assert t.id == 1
    assert t.type == "expense"
    assert t.to_dict() == data


# ---------- Тесты функций работы с коллекцией ----------

def test_add_transaction():
    """add_transaction создаёт объект и добавляет в коллекцию."""
    transactions = []
    t = add_transaction(transactions, "expense", 15000,
                        "Техника", "2026-09-15")

    assert len(transactions) == 1
    assert isinstance(t, Transaction)
    assert t.id == 1


def test_find_transaction_by_id():
    """Поиск операции по идентификатору."""
    transactions = []
    add_transaction(transactions, "income", 60000, "Зарплата", "2026-09-01")

    found = find_transaction_by_id(transactions, 1)
    assert found is not None
    assert found.category == "Зарплата"

    assert find_transaction_by_id(transactions, 99) is None


def test_find_transactions_by_category():
    """Поиск операций по подстроке категории."""
    transactions = []
    add_transaction(transactions, "expense", 15000, "Техника", "2026-09-15")
    add_transaction(transactions, "expense", 5000, "Кафе", "2026-09-16")

    found = find_transactions_by_category(transactions, "тех")
    assert len(found) == 1
    assert found[0].category == "Техника"


def test_total_by_type():
    """Сумма доходов и расходов считается раздельно."""
    transactions = []
    add_transaction(transactions, "income", 60000, "Зарплата", "2026-09-01")
    add_transaction(transactions, "expense", 15000, "Техника", "2026-09-15")
    add_transaction(transactions, "expense", 5000, "Кафе", "2026-09-16")

    assert total_by_type(transactions, "income") == 60000
    assert total_by_type(transactions, "expense") == 20000


def test_sort_transactions_by_amount():
    """Сортировка по сумме — по убыванию."""
    transactions = []
    add_transaction(transactions, "expense", 5000, "Кафе", "2026-09-16")
    add_transaction(transactions, "income", 60000, "Зарплата", "2026-09-01")
    add_transaction(transactions, "expense", 15000, "Техника", "2026-09-15")

    sorted_ts = sort_transactions_by_amount(transactions)
    assert sorted_ts[0].amount == 60000
    assert sorted_ts[1].amount == 15000
    assert sorted_ts[2].amount == 5000


def test_category_statistics():
    """Статистика по категориям расходов."""
    transactions = []
    add_transaction(transactions, "expense", 15000, "Техника", "2026-09-15")
    add_transaction(transactions, "expense", 5000, "Кафе", "2026-09-16")
    add_transaction(transactions, "income", 60000, "Зарплата", "2026-09-01")

    stats = category_statistics(transactions)
    assert stats["Техника"] == 15000
    assert stats["Кафе"] == 5000
    assert "Зарплата" not in stats
