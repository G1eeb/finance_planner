"""Класс Budget и функции работы с месячными бюджетами."""

from __future__ import annotations


class Budget:
    """Месячный бюджет — план на конкретный месяц."""

    def __init__(self, budget_id: int, month: str,
                 monthly_budget: float,
                 current_expenses: float = 0.0) -> None:
        """Создать бюджет.

        :param budget_id: идентификатор
        :param month: месяц в формате "YYYY-MM" (например, "2026-09")
        :param monthly_budget: сумма бюджета на месяц
        :param current_expenses: уже потрачено за месяц
        """
        if not self.validate_budget(monthly_budget):
            raise ValueError("Месячный бюджет должен быть положительным.")
        if current_expenses < 0:
            raise ValueError("Расходы не могут быть отрицательными.")

        self.id = budget_id
        self.month = month
        self.monthly_budget = monthly_budget
        self.current_expenses = current_expenses

    def __str__(self) -> str:
        """Вернуть строковое представление бюджета."""
        remaining = self.get_remaining()
        return (f"[{self.id}] Бюджет {self.month}: "
                f"{self.monthly_budget:.2f} руб., "
                f"потрачено {self.current_expenses:.2f} руб., "
                f"остаток {remaining:.2f} руб.")

    def get_remaining(self) -> float:
        """Вернуть остаток бюджета (доход минус расходы)."""
        return self.monthly_budget - self.current_expenses

    def get_remaining_after(self, amount: float) -> float:
        """Вернуть остаток после планируемой траты."""
        return self.get_remaining() - amount

    def can_afford(self, amount: float) -> bool:
        """Проверить, возможна ли трата без превышения бюджета."""
        return amount <= self.get_remaining()

    @staticmethod
    def validate_budget(amount: float) -> bool:
        """Проверить, что сумма бюджета положительна."""
        return amount > 0

    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        """Создать бюджет из словаря (например, из JSON)."""
        return cls(
            budget_id=data["id"],
            month=data["month"],
            monthly_budget=data["monthly_budget"],
            current_expenses=data.get("current_expenses", 0.0),
        )

    def to_dict(self) -> dict:
        """Преобразовать бюджет в словарь для JSON."""
        return {
            "id": self.id,
            "month": self.month,
            "monthly_budget": self.monthly_budget,
            "current_expenses": self.current_expenses,
        }


# ---------- Функции работы с коллекцией бюджетов ----------

def add_budget(budgets: list[Budget], month: str,
               monthly_budget: float) -> Budget:
    """Создать бюджет, добавить в коллекцию и вернуть."""
    budget_id = max((b.id for b in budgets), default=0) + 1
    budget = Budget(budget_id, month, monthly_budget)
    budgets.append(budget)
    return budget


def find_budget_by_id(budgets: list[Budget],
                      budget_id: int) -> Budget | None:
    """Найти бюджет по идентификатору."""
    for budget in budgets:
        if budget.id == budget_id:
            return budget
    return None


def find_budget_by_month(budgets: list[Budget],
                         month: str) -> Budget | None:
    """Найти бюджет по месяцу (например, '2026-09')."""
    for budget in budgets:
        if budget.month == month:
            return budget
    return None
