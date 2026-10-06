"""Класс Income и функции работы с доходами."""

from __future__ import annotations


class Income:
    """Доход — поступление денежных средств."""

    def __init__(self, income_id: int, amount: float,
                 category: str, date: str) -> None:
        """Создать доход.

        Проверяет, что сумма положительна.
        """
        if not self.validate_amount(amount):
            raise ValueError("Сумма дохода должна быть положительной.")

        self.id = income_id
        self.amount = amount
        self.category = category
        self.date = date

    def __str__(self) -> str:
        """Вернуть строковое представление дохода."""
        return (f"[{self.id}] Доход: {self.amount:.2f} руб. "
                f"({self.category}, {self.date})")

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Проверить, что сумма положительна."""
        return amount > 0

    @classmethod
    def from_dict(cls, data: dict) -> "Income":
        """Создать доход из словаря (например, из JSON)."""
        return cls(
            income_id=data["id"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
        )

    def to_dict(self) -> dict:
        """Преобразовать доход в словарь для JSON."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }


# ---------- Функции работы с коллекцией доходов ----------

def add_income(incomes: list[Income], amount: float,
               category: str, date: str) -> Income:
    """Создать доход, добавить в коллекцию и вернуть."""
    income_id = max((i.id for i in incomes), default=0) + 1
    income = Income(income_id, amount, category, date)
    incomes.append(income)
    return income


def find_income_by_id(incomes: list[Income],
                      income_id: int) -> Income | None:
    """Найти доход по идентификатору."""
    for income in incomes:
        if income.id == income_id:
            return income
    return None


def find_incomes_by_category(incomes: list[Income],
                             query: str) -> list[Income]:
    """Найти доходы, в категории которых есть подстрока query."""
    query_lower = query.lower()
    return [
        i for i in incomes
        if query_lower in i.category.lower()
    ]


def sort_incomes_by_amount(incomes: list[Income]) -> list[Income]:
    """Отсортировать доходы по сумме по убыванию."""
    return sorted(incomes, key=lambda i: i.amount, reverse=True)


def total_incomes(incomes: list[Income]) -> float:
    """Подсчитать сумму всех доходов."""
    return sum(i.amount for i in incomes)
