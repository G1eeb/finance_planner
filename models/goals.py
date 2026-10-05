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
