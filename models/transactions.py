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


# ---------- Функции работы с коллекцией операций ----------

def add_transaction(transactions: list[Transaction], type_: str,
                    amount: float, category: str, date: str) -> Transaction:
    """Создать операцию, добавить её в коллекцию и вернуть."""
    transaction_id = max((t.id for t in transactions), default=0) + 1
    transaction = Transaction(transaction_id, type_, amount, category, date)
    transactions.append(transaction)
    return transaction


def find_transaction_by_id(transactions: list[Transaction],
                           transaction_id: int) -> Transaction | None:
    """Найти операцию по идентификатору. Вернуть None, если не найдена."""
    for t in transactions:
        if t.id == transaction_id:
            return t
    return None


def find_transactions_by_category(transactions: list[Transaction],
                                  query: str) -> list[Transaction]:
    """Найти операции, в категории которых есть подстрока query."""
    query_lower = query.lower()
    return [
        t for t in transactions
        if query_lower in t.category.lower()
    ]


def filter_transactions_by_date(transactions: list[Transaction],
                                start_date: str,
                                end_date: str):
    """Отобрать операции за период [start_date, end_date] (генератор)."""
    return (
        t for t in transactions
        if start_date <= t.date <= end_date
    )


def sort_transactions_by_amount(
    transactions: list[Transaction],
) -> list[Transaction]:
    """Отсортировать операции по сумме по убыванию."""
    return sorted(transactions, key=lambda t: t.amount, reverse=True)


def total_by_type(transactions: list[Transaction], type_: str) -> float:
    """Подсчитать сумму операций заданного типа."""
    return sum(t.amount for t in transactions if t.type == type_)


def category_statistics(
    transactions: list[Transaction],
) -> dict[str, float]:
    """Собрать статистику расходов по категориям."""
    stats: dict[str, float] = {}
    for t in transactions:
        if t.is_expense():
            stats[t.category] = stats.get(t.category, 0.0) + t.amount
    return stats
