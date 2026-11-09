"""Перенос данных из старой базы (ПР7) в Django-БД через ORM."""

import os
import sqlite3
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "finance_planner_django.settings",
)
django.setup()

from budgets.models import Budget  # noqa: E402
from categories.models import Category  # noqa: E402
from expenses.models import Expense  # noqa: E402
from incomes.models import Income  # noqa: E402

SOURCE_DB = BASE_DIR / "data" / "finance_planner.sqlite"


def main():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row

        categories = conn.execute(
            "SELECT id, name FROM categories ORDER BY id"
        ).fetchall()

        incomes = conn.execute(
            "SELECT id, amount, category_id, date "
            "FROM incomes ORDER BY id"
        ).fetchall()

        expenses = conn.execute(
            "SELECT id, amount, category_id, date "
            "FROM expenses ORDER BY id"
        ).fetchall()

        budgets = conn.execute(
            "SELECT id, month, monthly_budget, current_expenses "
            "FROM budgets ORDER BY id"
        ).fetchall()

    with transaction.atomic():
        # 1. Категории (независимая сущность)
        for row in categories:
            Category.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )

        # 2. Доходы (зависят от категорий)
        for row in incomes:
            Income.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "amount": Decimal(str(row["amount"])),
                    "category_id": row["category_id"],
                    "date": date.fromisoformat(row["date"]),
                },
            )

        # 3. Расходы (зависят от категорий)
        for row in expenses:
            Expense.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "amount": Decimal(str(row["amount"])),
                    "category_id": row["category_id"],
                    "date": date.fromisoformat(row["date"]),
                },
            )

        # 4. Бюджеты (независимая сущность)
        for row in budgets:
            Budget.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "month": row["month"],
                    "monthly_budget": Decimal(
                        str(row["monthly_budget"])
                    ),
                    "current_expenses": Decimal(
                        str(row["current_expenses"])
                    ),
                },
            )

    print("Перенос данных завершён.")
    print(f"Категорий:    {Category.objects.count()}")
    print(f"Доходов:      {Income.objects.count()}")
    print(f"Расходов:     {Expense.objects.count()}")
    print(f"Бюджетов:     {Budget.objects.count()}")


if __name__ == "__main__":
    main()
