"""Тесты класса Income и функций работы с доходами."""

import pytest

from models import Income
from models.incomes import (
    add_income,
    find_income_by_id,
    find_incomes_by_category,
    sort_incomes_by_amount,
    total_incomes,
)


# ---------- Тесты класса Income ----------

def test_income_creation():
    """Объект Income создаётся с корректными атрибутами."""
    income = Income(1, 60000, "Зарплата", "2026-09-01")
    assert income.id == 1
    assert income.amount == 60000
    assert income.category == "Зарплата"
    assert income.date == "2026-09-01"


def test_income_str():
    """__str__ возвращает читаемое представление."""
    income = Income(1, 60000, "Зарплата", "2026-09-01")
    text = str(income)
    assert "Доход" in text
    assert "60000.00" in text
    assert "Зарплата" in text


def test_income_validation():
    """Некорректная сумма вызывает ValueError."""
    with pytest.raises(ValueError):
        Income(1, -100, "Тест", "2026-01-01")

    with pytest.raises(ValueError):
        Income(1, 0, "Тест", "2026-01-01")


def test_income_from_dict_to_dict():
    """from_dict и to_dict корректно преобразуют данные."""
    data = {
        "id": 1, "amount": 60000,
        "category": "Зарплата", "date": "2026-09-01",
    }
    income = Income.from_dict(data)
    assert income.id == 1
    assert income.amount == 60000
    assert income.to_dict() == data


# ---------- Тесты функций работы с коллекцией ----------

def test_add_income():
    """add_income создаёт объект и добавляет его в коллекцию."""
    incomes = []
    income = add_income(incomes, 60000, "Зарплата", "2026-09-01")
    assert len(incomes) == 1
    assert isinstance(income, Income)
    assert income.id == 1


def test_find_income_by_id():
    """Поиск дохода по идентификатору."""
    incomes = []
    add_income(incomes, 60000, "Зарплата", "2026-09-01")

    found = find_income_by_id(incomes, 1)
    assert found is not None
    assert found.category == "Зарплата"

    assert find_income_by_id(incomes, 99) is None


def test_find_incomes_by_category():
    """Поиск доходов по подстроке категории."""
    incomes = []
    add_income(incomes, 60000, "Зарплата", "2026-09-01")
    add_income(incomes, 5000, "Подработка", "2026-09-10")

    found = find_incomes_by_category(incomes, "зар")
    assert len(found) == 1
    assert found[0].category == "Зарплата"


def test_sort_incomes_by_amount():
    """Сортировка доходов по сумме — по убыванию."""
    incomes = []
    add_income(incomes, 5000, "Подработка", "2026-09-10")
    add_income(incomes, 60000, "Зарплата", "2026-09-01")

    sorted_incomes = sort_incomes_by_amount(incomes)
    assert sorted_incomes[0].amount == 60000
    assert sorted_incomes[1].amount == 5000


def test_total_incomes():
    """Сумма всех доходов считается корректно."""
    incomes = []
    add_income(incomes, 60000, "Зарплата", "2026-09-01")
    add_income(incomes, 5000, "Подработка", "2026-09-10")

    assert total_incomes(incomes) == 65000
