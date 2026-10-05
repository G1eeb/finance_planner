"""Тесты класса Goal и функций работы с целями."""

import pytest

from models import Goal
from models.goals import (
    add_goal,
    add_to_goal,
    find_goal_by_id,
    filter_achieved_goals,
    sort_goals_by_progress,
    total_saved,
)


# ---------- Тесты класса Goal ----------

def test_goal_creation():
    """Объект Goal создаётся с корректными атрибутами."""
    g = Goal(1, "Отпуск", 100000)
    assert g.id == 1
    assert g.name == "Отпуск"
    assert g.target == 100000
    assert g.saved == 0.0


def test_goal_str():
    """__str__ возвращает читаемое представление."""
    g = Goal(1, "Отпуск", 100000, 25000)
    s = str(g)
    assert "Отпуск" in s
    assert "25000.00" in s
    assert "25.0%" in s


def test_goal_add_to_goal():
    """Метод add_to_goal увеличивает saved."""
    g = Goal(1, "Отпуск", 100000)
    g.add_to_goal(25000)
    assert g.saved == 25000


def test_goal_get_progress():
    """Прогресс считается корректно и не превышает 100%."""
    g = Goal(1, "Отпуск", 100000)
    g.add_to_goal(25000)
    assert g.get_progress() == 25.0

    g.add_to_goal(100000)   # накоплено больше цели
    assert g.get_progress() == 100.0


def test_goal_is_achieved():
    """Метод is_achieved корректно определяет достижение."""
    g = Goal(1, "Отпуск", 100000)
    assert not g.is_achieved()

    g.add_to_goal(100000)
    assert g.is_achieved()


def test_goal_validation():
    """Некорректные суммы вызывают ValueError."""
    with pytest.raises(ValueError):
        Goal(1, "Плохая", -100)

    g = Goal(1, "Отпуск", 100000)
    with pytest.raises(ValueError):
        g.add_to_goal(-500)


def test_goal_from_dict_to_dict():
    """from_dict и to_dict корректно преобразуют данные."""
    data = {"id": 1, "name": "Отпуск", "target": 100000, "saved": 25000}
    g = Goal.from_dict(data)

    assert g.id == 1
    assert g.name == "Отпуск"
    assert g.to_dict() == data


# ---------- Тесты функций работы с коллекцией ----------

def test_add_goal():
    """add_goal создаёт объект и добавляет в коллекцию."""
    goals = []
    g = add_goal(goals, "Отпуск", 100000)
    assert len(goals) == 1
    assert isinstance(g, Goal)
    assert g.id == 1
    assert g.saved == 0.0


def test_find_goal_by_id():
    """Поиск цели по идентификатору."""
    goals = []
    add_goal(goals, "Отпуск", 100000)
    add_goal(goals, "Ноутбук", 80000)

    found = find_goal_by_id(goals, 1)
    assert found is not None
    assert found.name == "Отпуск"

    assert find_goal_by_id(goals, 99) is None


def test_add_to_goal_function():
    """add_to_goal находит цель и вызывает её метод."""
    goals = []
    add_goal(goals, "Отпуск", 100000)
    g = add_to_goal(goals, 1, 25000)

    assert g.saved == 25000
    assert goals[0].saved == 25000


def test_add_to_goal_not_found():
    """Пополнение несуществующей цели вызывает ValueError."""
    goals = []
    with pytest.raises(ValueError):
        add_to_goal(goals, 99, 1000)


def test_filter_achieved_goals():
    """Фильтр возвращает только достигнутые цели."""
    goals = []
    add_goal(goals, "Отпуск", 100000)
    add_goal(goals, "Ноутбук", 80000)
    add_to_goal(goals, 2, 80000)

    achieved = list(filter_achieved_goals(goals))
    assert len(achieved) == 1
    assert achieved[0].name == "Ноутбук"


def test_sort_goals_by_progress():
    """Сортировка целей по прогрессу — по убыванию."""
    goals = []
    add_goal(goals, "Отпуск", 100000)
    add_goal(goals, "Ноутбук", 80000)
    add_goal(goals, "Книга", 2000)

    add_to_goal(goals, 1, 25000)   # 25%
    add_to_goal(goals, 2, 80000)   # 100%
    add_to_goal(goals, 3, 500)     # 25%

    sorted_gs = sort_goals_by_progress(goals)
    assert sorted_gs[0].name == "Ноутбук"


def test_total_saved():
    """Суммарное накопление по всем целям."""
    goals = []
    add_goal(goals, "Отпуск", 100000)
    add_goal(goals, "Ноутбук", 80000)
    add_to_goal(goals, 1, 25000)
    add_to_goal(goals, 2, 80000)

    assert total_saved(goals) == 105000
