"""Класс Goal и функции работы с коллекцией финансовых целей."""

from __future__ import annotations


class Goal:
    """Финансовая цель (накопление на покупку)."""

    def __init__(self, goal_id: int, name: str, target: float,
                 saved: float = 0.0) -> None:
        """Создать финансовую цель.

        Проверяет корректность целевой суммы и накопленной суммы.
        """
        if not self.validate_target(target):
            raise ValueError("Целевая сумма должна быть положительной.")
        if saved < 0:
            raise ValueError("Накопленная сумма не может быть отрицательной.")

        self.id = goal_id
        self.name = name
        self.target = target
        self.saved = saved

    def __str__(self) -> str:
        """Вернуть строковое представление цели."""
        progress = self.get_progress()
        status = "достигнута" if self.is_achieved() else "в процессе"
        return (f"[{self.id}] {self.name}: {self.saved:.2f} / "
                f"{self.target:.2f} руб. ({progress:.1f}%, {status})")

    def add_to_goal(self, amount: float) -> None:
        """Пополнить цель на указанную сумму."""
        if not self.validate_target(amount):
            raise ValueError("Сумма пополнения должна быть положительной.")
        self.saved += amount

    def get_progress(self) -> float:
        """Вернуть процент выполнения цели (0–100)."""
        if self.target == 0:
            return 0.0
        progress = self.saved / self.target * 100
        return min(progress, 100.0)

    def is_achieved(self) -> bool:
        """Проверить, достигнута ли цель."""
        return self.saved >= self.target

    @staticmethod
    def validate_target(target: float) -> bool:
        """Проверить, что сумма положительна."""
        return target > 0

    @classmethod
    def from_dict(cls, data: dict) -> "Goal":
        """Создать цель из словаря (например, из JSON)."""
        return cls(
            goal_id=data["id"],
            name=data["name"],
            target=data["target"],
            saved=data.get("saved", 0.0),
        )

    def to_dict(self) -> dict:
        """Преобразовать цель в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "target": self.target,
            "saved": self.saved,
        }


# ---------- Функции работы с коллекцией целей ----------

def add_goal(goals: list[Goal], name: str, target: float) -> Goal:
    """Создать цель, добавить её в коллекцию и вернуть."""
    goal_id = max((g.id for g in goals), default=0) + 1
    goal = Goal(goal_id, name, target)
    goals.append(goal)
    return goal


def find_goal_by_id(goals: list[Goal], goal_id: int) -> Goal | None:
    """Найти цель по идентификатору. Вернуть None, если не найдена."""
    for goal in goals:
        if goal.id == goal_id:
            return goal
    return None


def add_to_goal(goals: list[Goal], goal_id: int, amount: float) -> Goal:
    """Пополнить цель по идентификатору.

    Возвращает обновлённую цель.
    Вызывает ValueError, если цель не найдена.
    """
    goal = find_goal_by_id(goals, goal_id)
    if goal is None:
        raise ValueError(f"Цель с id={goal_id} не найдена.")

    goal.add_to_goal(amount)
    return goal


def filter_achieved_goals(goals: list[Goal]):
    """Вернуть генератор достигнутых целей."""
    return (g for g in goals if g.is_achieved())


def sort_goals_by_progress(goals: list[Goal]) -> list[Goal]:
    """Отсортировать цели по проценту выполнения по убыванию."""
    return sorted(goals, key=Goal.get_progress, reverse=True)


def total_saved(goals: list[Goal]) -> float:
    """Подсчитать суммарно накопленную сумму по всем целям."""
    return sum(g.saved for g in goals)
