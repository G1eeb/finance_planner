"""Модуль сохранения и загрузки данных в JSON-файлах."""

import json
import os


def load_transactions(filename: str) -> list[dict]:
    """Загрузить операции из JSON-файла.
    Если файла нет или он повреждён — вернуть пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён, данные не загружены.")
        return []


def save_transactions(filename: str, transactions: list[dict]) -> None:
    """Сохранить операции в JSON-файл."""
    _ensure_dir(filename)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(transactions, f, ensure_ascii=False, indent=2)


def load_goals(filename: str) -> list[dict]:
    """Загрузить цели из JSON-файла.
    Если файла нет или он повреждён — вернуть пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} повреждён, данные не загружены.")
        return []


def save_goals(filename: str, goals: list[dict]) -> None:
    """Сохранить цели в JSON-файл."""
    _ensure_dir(filename)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(goals, f, ensure_ascii=False, indent=2)


def _ensure_dir(filename: str) -> None:
    """Создать каталог для файла, если его ещё нет."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
