"""Класс Transaction и функции работы с коллекцией операций."""

from __future__ import annotations

INCOME = "income"
EXPENSE = "expense"


class Transaction:
    """Операция (доход или расход)."""

    def __init__(self, transaction_id: int, type_: str, amount: float,
                 category: str, date: str) -> None:
        """Создать операцию.

        Проверяет корректность типа и суммы.
        """
        if not self.validate_type(type_):
            raise ValueError(f"Недопустимый тип операции: {type_}")
        if not self.validate_amount(amount):
            raise ValueError("Сумма должна быть положительной.")

        self.id = transaction_id
        self.type = type_
        self.amount = amount
        self.category = category
        self.date = date

    def __str__(self) -> str:
        """Вернуть строковое представление операции."""
        type_ru = "Доход" if self.is_income() else "Расход"
        return (f"[{self.id}] {type_ru}: {self.amount:.2f} руб. "
                f"({self.category}, {self.date})")

    def is_income(self) -> bool:
        """Проверить, является ли операция доходом."""
        return self.type == INCOME

    def is_expense(self) -> bool:
        """Проверить, является ли операция расходом."""
        return self.type == EXPENSE

    @staticmethod
    def validate_type(type_: str) -> bool:
        """Проверить, что тип операции допустим."""
        return type_ in (INCOME, EXPENSE)

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Проверить, что сумма положительна."""
        return amount > 0

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Создать операцию из словаря (например, из JSON)."""
        return cls(
            transaction_id=data["id"],
            type_=data["type"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
        )

    def to_dict(self) -> dict:
        """Преобразовать операцию в словарь для JSON."""
        return {
            "id": self.id,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }
