"""Модуль сохранения и загрузки данных в JSON-файлах.

При загрузке словари преобразуются в объекты Transaction и Goal.
При сохранении объекты преобразуются обратно в словари для JSON.
"""

import json
import os

from models import Transaction, Goal


def load_transactions(filename: str) -> list[Transaction]:
    """Загрузить операции из JSON-файла.

    Если файла нет или он повреждён — вернуть пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён, данные не загружены.")
        return []

    return [Transaction.from_dict(item) for item in data]


def save_transactions(filename: str,
                      transactions: list[Transaction]) -> None:
    """Сохранить операции в JSON-файл."""
    _ensure_dir(filename)
    data = [t.to_dict() for t in transactions]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_goals(filename: str) -> list[Goal]:
    """Загрузить цели из JSON-файла.

    Если файла нет или он повреждён — вернуть пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён, данные не загружены.")
        return []

    return [Goal.from_dict(item) for item in data]


def save_goals(filename: str, goals: list[Goal]) -> None:
    """Сохранить цели в JSON-файл."""
    _ensure_dir(filename)
    data = [g.to_dict() for g in goals]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ensure_dir(filename: str) -> None:
    """Создать каталог для файла, если его ещё нет."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
