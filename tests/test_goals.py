"""Тесты функций модуля goals."""

from goals import add_goal, add_to_goal, get_goal_progress


def test_add_goal():
    """Цель добавляется с нулевым накоплением."""
    goals = []
    g = add_goal(goals, "Отпуск", 100000)
    assert len(goals) == 1
    assert g["id"] == 1
    assert g["saved"] == 0.0


def test_add_to_goal_and_progress():
    """Пополнение увеличивает saved и прогресс."""
    goals = []
    add_goal(goals, "Отпуск", 100000)
    add_to_goal(goals, 1, 25000)

    assert goals[0]["saved"] == 25000
    assert get_goal_progress(goals[0]) == 25.0
