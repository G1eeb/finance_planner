"""Тесты класса Expense и функций работы с расходами."""

import pytest

from models import Expense
from models.expenses import (
    add_expense,
    expenses_by_category,
    find_expense_by_id,
    find_expenses_by_category,
    sort_expenses_by_amount,
    total_expenses,
)


# ---------- Тесты класса Expense ----------

def test_expense_creation():
    """Объект Expense создаётся с корректными атрибутами."""
    expense = Expense(1, 15000, "Техника", "2026-09-15")
    assert expense.id == 1
    assert expense.amount == 15000
    assert expense.category == "Техника"
    assert expense.date == "2026-09-15"


def test_expense_str():
    """__str__ возвращает читаемое представление."""
    expense = Expense(1, 15000, "Техника", "2026-09-15")
    text = str(expense)
    assert "Расход" in text
    assert "15000.00" in text


def test_expense_validation():
    """Некорректная сумма вызывает ValueError."""
    with pytest.raises(ValueError):
        Expense(1, -100, "Тест", "2026-01-01")

    with pytest.raises(ValueError):
        Expense(1, 0, "Тест", "2026-01-01")


def test_expense_from_dict_to_dict():
    """from_dict и to_dict корректно преобразуют данные."""
    data = {
        "id": 1, "amount": 15000,
        "category": "Техника", "date": "2026-09-15",
    }
    expense = Expense.from_dict(data)
    assert expense.id == 1
    assert expense.amount == 15000
    assert expense.to_dict() == data


# ---------- Тесты функций работы с коллекцией ----------

def test_add_expense():
    """add_expense создаёт объект и добавляет его в коллекцию."""
    expenses = []
    expense = add_expense(expenses, 15000, "Техника", "2026-09-15")
    assert len(expenses) == 1
    assert isinstance(expense, Expense)
    assert expense.id == 1


def test_find_expense_by_id():
    """Поиск расхода по идентификатору."""
    expenses = []
    add_expense(expenses, 15000, "Техника", "2026-09-15")

    found = find_expense_by_id(expenses, 1)
    assert found is not None
    assert found.category == "Техника"

    assert find_expense_by_id(expenses, 99) is None


def test_find_expenses_by_category():
    """Поиск расходов по подстроке категории."""
    expenses = []
    add_expense(expenses, 15000, "Техника", "2026-09-15")
    add_expense(expenses, 5000, "Кафе", "2026-09-16")

    found = find_expenses_by_category(expenses, "тех")
    assert len(found) == 1
    assert found[0].category == "Техника"


def test_sort_expenses_by_amount():
    """Сортировка расходов по сумме — по убыванию."""
    expenses = []
    add_expense(expenses, 5000, "Кафе", "2026-09-16")
    add_expense(expenses, 15000, "Техника", "2026-09-15")

    sorted_expenses = sort_expenses_by_amount(expenses)
    assert sorted_expenses[0].amount == 15000
    assert sorted_expenses[1].amount == 5000


def test_total_expenses():
    """Сумма всех расходов считается корректно."""
    expenses = []
    add_expense(expenses, 15000, "Техника", "2026-09-15")
    add_expense(expenses, 5000, "Кафе", "2026-09-16")

    assert total_expenses(expenses) == 20000


def test_expenses_by_category():
    """Статистика расходов по категориям."""
    expenses = []
    add_expense(expenses, 15000, "Техника", "2026-09-15")
    add_expense(expenses, 5000, "Кафе", "2026-09-16")
    add_expense(expenses, 3000, "Кафе", "2026-09-17")

    stats = expenses_by_category(expenses)
    assert stats["Техника"] == 15000
    assert stats["Кафе"] == 8000
