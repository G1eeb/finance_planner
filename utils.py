"""Модуль вспомогательных функций безопасного ввода."""

from datetime import date, datetime

DATE_FORMAT = "%d.%m.%Y"


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.
    При некорректном вводе повторяет запрос.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя число с плавающей точкой.
    При некорректном вводе повторяет запрос.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ.
    При некорректном вводе повторяет запрос.
    """
    while True:
        try:
            raw = input(prompt)
            return datetime.strptime(raw, DATE_FORMAT).date()
        except ValueError:
            print(f"Ошибка: неверный формат даты. "
                  f"Используйте {DATE_FORMAT}.")


def input_choice(prompt: str, options: list[str]) -> str:
    """Запросить у пользователя выбор из списка вариантов.
    При некорректном вводе повторяет запрос.
    """
    while True:
        raw = input(prompt).strip().lower()
        if raw in options:
            return raw
        print(f"Ошибка: допустимые варианты — {', '.join(options)}.")
