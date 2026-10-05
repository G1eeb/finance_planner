"""Модуль работы с финансовыми целями."""


def add_goal(goals: list[dict], name: str, target: float) -> dict:
    """Добавить финансовую цель и вернуть её.
    Проверяет положительность целевой суммы.
    """
    if target <= 0:
        raise ValueError("Целевая сумма должна быть положительной.")

    goal_id = max((g["id"] for g in goals), default=0) + 1
    goal = {
        "id": goal_id,
        "name": name,
        "target": target,
        "saved": 0.0,
    }
    goals.append(goal)
    return goal


def find_goal_by_id(goals: list[dict], goal_id: int) -> dict | None:
    """Найти цель по её идентификатору. Вернуть None, если не найдена."""
    for goal in goals:
        if goal["id"] == goal_id:
            return goal
    return None


def add_to_goal(goals: list[dict], goal_id: int, amount: float) -> dict:
    """Пополнить цель на указанную сумму.
    Возвращает обновлённую цель.
    Вызывает ValueError, если цель не найдена или сумма неположительна.
    """
    if amount <= 0:
        raise ValueError("Сумма пополнения должна быть положительной.")

    goal = find_goal_by_id(goals, goal_id)
    if goal is None:
        raise ValueError(f"Цель с id={goal_id} не найдена.")

    goal["saved"] += amount
    return goal


def get_goal_progress(goal: dict) -> float:
    """Вернуть процент выполнения цели (0–100)."""
    if goal["target"] == 0:
        return 0.0
    progress = goal["saved"] / goal["target"] * 100
    return min(progress, 100.0)


def filter_achieved_goals(goals: list[dict]):
    """Вернуть генератор достигнутых целей (saved >= target)."""
    return (
        g for g in goals
        if g["saved"] >= g["target"]
    )


def sort_goals_by_progress(goals: list[dict]) -> list[dict]:
    """Отсортировать цели по проценту выполнения по убыванию."""
    return sorted(goals, key=get_goal_progress, reverse=True)


def total_saved(goals: list[dict]) -> float:
    """Подсчитать суммарно накопленную сумму по всем целям."""
    return sum(g["saved"] for g in goals)
