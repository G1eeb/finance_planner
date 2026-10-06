"""Тесты класса Budget и функций работы с бюджетами."""

import pytest

from models import Budget
from models.budgets import (
    add_budget,
    find_budget_by_id,
    find_budget_by_month,
)


# ---------- Тесты класса Budget ----------

def test_budget_creation():
    """Объект Budget создаётся с корректными атрибутами."""
    budget = Budget(1, "2026-09", 60000, 42500)
    assert budget.id == 1
    assert budget.month == "2026-09"
    assert budget.monthly_budget == 60000
    assert budget.current_expenses == 42500


def test_budget_str():
    """__str__ возвращает читаемое представление."""
    budget = Budget(1, "2026-09", 60000, 42500)
    text = str(budget)
    assert "2026-09" in text
    assert "60000.00" in text
    assert "17500.00" in text  # остаток


def test_budget_validation():
    """Некорректные данные вызывают ValueError."""
    with pytest.raises(ValueError):
        Budget(1, "2026-09", -1000)

    with pytest.raises(ValueError):
        Budget(1, "2026-09", 60000, -100)


def test_budget_get_remaining():
    """Остаток считается корректно."""
    budget = Budget(1, "2026-09", 60000, 42500)
    assert budget.get_remaining() == 17500


def test_budget_can_afford():
    """Проверка возможности траты."""
    budget = Budget(1, "2026-09", 60000, 42500)
    assert budget.can_afford(15000)
    assert not budget.can_afford(20000)


def test_budget_get_remaining_after():
    """Остаток после планируемой траты."""
    budget = Budget(1, "2026-09", 60000, 42500)
    assert budget.get_remaining_after(15000) == 2500


def test_budget_from_dict_to_dict():
    """from_dict и to_dict корректно преобразуют данные."""
    data = {
        "id": 1, "month": "2026-09",
        "monthly_budget": 60000, "current_expenses": 42500,
    }
    budget = Budget.from_dict(data)
    assert budget.id == 1
    assert budget.to_dict() == data


# ---------- Тесты функций работы с коллекцией ----------

def test_add_budget():
    """add_budget создаёт объект и добавляет его в коллекцию."""
    budgets = []
    budget = add_budget(budgets, "2026-09", 60000)
    assert len(budgets) == 1
    assert isinstance(budget, Budget)
    assert budget.id == 1
    assert budget.current_expenses == 0.0


def test_find_budget_by_id():
    """Поиск бюджета по идентификатору."""
    budgets = []
    add_budget(budgets, "2026-09", 60000)

    found = find_budget_by_id(budgets, 1)
    assert found is not None
    assert found.month == "2026-09"

    assert find_budget_by_id(budgets, 99) is None


def test_find_budget_by_month():
    """Поиск бюджета по месяцу."""
    budgets = []
    add_budget(budgets, "2026-09", 60000)
    add_budget(budgets, "2026-10", 50000)

    found = find_budget_by_month(budgets, "2026-10")
    assert found is not None
    assert found.monthly_budget == 50000

    assert find_budget_by_month(budgets, "2026-11") is None
