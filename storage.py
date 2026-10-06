"""Модуль сохранения и загрузки данных в JSON-файлах.

При загрузке словари преобразуются в объекты Income, Expense, Budget.
При сохранении объекты преобразуются обратно в словари для JSON.
"""

import json
import os

from models import Budget, Expense, Income


def _load_json(filename: str, default):
    """Загрузить JSON-файл. Вернуть default при отсутствии/ошибке."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён, данные не загружены.")
        return default


def _save_json(filename: str, data) -> None:
    """Сохранить данные в JSON-файл."""
    _ensure_dir(filename)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ensure_dir(filename: str) -> None:
    """Создать каталог для файла, если его ещё нет."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)


# ---------- Доходы ----------

def load_incomes(filename: str) -> list[Income]:
    """Загрузить доходы из JSON-файла."""
    data = _load_json(filename, [])
    return [Income.from_dict(item) for item in data]


def save_incomes(filename: str, incomes: list[Income]) -> None:
    """Сохранить доходы в JSON-файл."""
    data = [i.to_dict() for i in incomes]
    _save_json(filename, data)


# ---------- Расходы ----------

def load_expenses(filename: str) -> list[Expense]:
    """Загрузить расходы из JSON-файла."""
    data = _load_json(filename, [])
    return [Expense.from_dict(item) for item in data]


def save_expenses(filename: str, expenses: list[Expense]) -> None:
    """Сохранить расходы в JSON-файл."""
    data = [e.to_dict() for e in expenses]
    _save_json(filename, data)


# ---------- Бюджеты ----------

def load_budgets(filename: str) -> list[Budget]:
    """Загрузить бюджеты из JSON-файла."""
    data = _load_json(filename, [])
    return [Budget.from_dict(item) for item in data]


def save_budgets(filename: str, budgets: list[Budget]) -> None:
    """Сохранить бюджеты в JSON-файл."""
    data = [b.to_dict() for b in budgets]
    _save_json(filename, data)
