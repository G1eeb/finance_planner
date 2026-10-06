# models/expenses.py
"""Класс Expense и функции работы с расходами."""

from __future__ import annotations


class Expense:
    """Расход — списание денежных средств."""

    def __init__(self, expense_id: int, amount: float,
                 category: str, date: str) -> None:
        """Создать расход.

        Проверяет, что сумма положительна.
        """
        if not self.validate_amount(amount):
            raise ValueError("Сумма расхода должна быть положительной.")

        self.id = expense_id
        self.amount = amount
        self.category = category
        self.date = date

    def __str__(self) -> str:
        """Вернуть строковое представление расхода."""
        return (f"[{self.id}] Расход: {self.amount:.2f} руб. "
                f"({self.category}, {self.date})")

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Проверить, что сумма положительна."""
        return amount > 0

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Создать расход из словаря (например, из JSON)."""
        return cls(
            expense_id=data["id"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
        )

    def to_dict(self) -> dict:
        """Преобразовать расход в словарь для JSON."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }


# ---------- Функции работы с коллекцией расходов ----------

def add_expense(expenses: list[Expense], amount: float,
                category: str, date: str) -> Expense:
    """Создать расход, добавить в коллекцию и вернуть."""
    expense_id = max((e.id for e in expenses), default=0) + 1
    expense = Expense(expense_id, amount, category, date)
    expenses.append(expense)
    return expense


def find_expense_by_id(expenses: list[Expense],
                       expense_id: int) -> Expense | None:
    """Найти расход по идентификатору."""
    for expense in expenses:
        if expense.id == expense_id:
            return expense
    return None


def find_expenses_by_category(expenses: list[Expense],
                              query: str) -> list[Expense]:
    """Найти расходы, в категории которых есть подстрока query."""
    query_lower = query.lower()
    return [
        e for e in expenses
        if query_lower in e.category.lower()
    ]


def sort_expenses_by_amount(expenses: list[Expense]) -> list[Expense]:
    """Отсортировать расходы по сумме по убыванию."""
    return sorted(expenses, key=lambda e: e.amount, reverse=True)


def total_expenses(expenses: list[Expense]) -> float:
    """Подсчитать сумму всех расходов."""
    return sum(e.amount for e in expenses)


def expenses_by_category(expenses: list[Expense]) -> dict[str, float]:
    """Собрать статистику расходов по категориям."""
    stats: dict[str, float] = {}
    for e in expenses:
        stats[e.category] = stats.get(e.category, 0.0) + e.amount
    return stats
