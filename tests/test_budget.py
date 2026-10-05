"""Тесты функций модуля budget."""

from budget import calculate_budget, check_budget


def test_calculate_budget_basic():
    """Остаток и сумма после траты считаются правильно."""
    remaining, after = calculate_budget(60000, 42500, 15000)
    assert remaining == 17500
    assert after == 2500


def test_check_budget_allows_expense():
    """Трата в пределах остатка разрешена."""
    status, warning = check_budget(
        planned_expense=15000,
        remaining_budget=17500,
        budget_after_expense=2500,
    )
    assert "возможна" in status
    assert "менее 5000" in warning


def test_check_budget_blocks_expense():
    """Трата сверх остатка запрещена, указывается превышение."""
    status, _ = check_budget(
        planned_expense=30000,
        remaining_budget=17500,
        budget_after_expense=-12500,
    )
    assert "невозможна" in status
    assert "12500" in status
