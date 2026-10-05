"""Точка входа приложения Finance Planner."""

from budget import calculate_budget, check_budget, format_report
from models.transactions import (
    add_transaction,
    find_transactions_by_category,
    sort_transactions_by_amount,
    total_by_type,
    category_statistics,
)
from models.goals import (
    add_goal,
    add_to_goal,
    filter_achieved_goals,
    sort_goals_by_progress,
    total_saved,
)
from storage import (
    load_transactions, save_transactions,
    load_goals, save_goals,
)
from utils import input_int, input_float, input_date, input_choice

TRANSACTIONS_FILE = "data/transactions.json"
GOALS_FILE = "data/goals.json"


# ---------- Вывод данных ----------

def show_transactions(transactions: list) -> None:
    """Вывести список операций."""
    if not transactions:
        print("Операций пока нет.")
        return
    print("-" * 70)
    for t in transactions:
        print(t)
    print("-" * 70)


def show_goals(goals: list) -> None:
    """Вывести список целей."""
    if not goals:
        print("Целей пока нет.")
        return
    print("-" * 70)
    for g in goals:
        print(g)
    print("-" * 70)


# ---------- Интерактивные операции ----------

def add_transaction_interactive(transactions: list) -> None:
    """Запросить данные и добавить операцию."""
    print("\nТип операции: 1 — доход, 2 — расход")
    choice = input_choice("Выбор: ", ["1", "2"])
    type_ = "income" if choice == "1" else "expense"

    amount = input_float("Сумма: ")
    category = input("Категория: ").strip()
    d = input_date("Дата (ДД.ММ.ГГГГ): ")

    try:
        t = add_transaction(transactions, type_, amount,
                            category, d.isoformat())
        print(f"Операция добавлена: id={t.id}")
    except ValueError as e:
        print(f"Ошибка: {e}")


def add_goal_interactive(goals: list) -> None:
    """Запросить данные и добавить цель."""
    name = input("Название цели: ").strip()
    target = input_float("Целевая сумма: ")

    try:
        g = add_goal(goals, name, target)
        print(f"Цель добавлена: id={g.id}")
    except ValueError as e:
        print(f"Ошибка: {e}")


def add_to_goal_interactive(goals: list) -> None:
    """Пополнить существующую цель."""
    if not goals:
        print("Целей пока нет.")
        return

    show_goals(goals)
    goal_id = input_int("ID цели для пополнения: ")
    amount = input_float("Сумма пополнения: ")

    try:
        g = add_to_goal(goals, goal_id, amount)
        print(f"Цель «{g.name}»: накоплено {g.saved:.2f} "
              f"из {g.target:.2f}")
    except ValueError as e:
        print(f"Ошибка: {e}")


def find_transactions_interactive(transactions: list) -> None:
    """Найти операции по подстроке категории."""
    query = input("Подстрока категории: ").strip()
    found = find_transactions_by_category(transactions, query)
    show_transactions(found)


def show_goals_sorted(goals: list) -> None:
    """Показать цели, отсортированные по прогрессу."""
    if not goals:
        print("Целей пока нет.")
        return
    show_goals(sort_goals_by_progress(goals))


def show_total_saved(goals: list) -> None:
    """Показать суммарную накопленную сумму по всем целям."""
    if not goals:
        print("Целей пока нет.")
        return
    total = total_saved(goals)
    print(f"Всего накоплено по всем целям: {total:.2f} руб.")


def show_achieved_goals(goals: list) -> None:
    """Показать достигнутые цели."""
    achieved = list(filter_achieved_goals(goals))
    if not achieved:
        print("Достигнутых целей пока нет.")
        return
    print("\nДостигнутые цели:")
    for g in achieved:
        print(f"  {g.name} — {g.target:.2f} руб.")


# ---------- Отчёты ----------

def show_statistics(transactions: list) -> None:
    """Показать статистику по операциям."""
    if not transactions:
        print("Операций пока нет.")
        return

    income = total_by_type(transactions, "income")
    expense = total_by_type(transactions, "expense")
    balance = income - expense

    print("\n" + "=" * 50)
    print(f"Доходы:      {income:>12.2f} руб.")
    print(f"Расходы:     {expense:>12.2f} руб.")
    if balance < 0:
        print(f"Баланс:      {balance:>12.2f} руб.  (превышение расходов)")
    else:
        print(f"Баланс:      {balance:>12.2f} руб.")
    print("=" * 50)

    stats = category_statistics(transactions)
    if stats:
        print("Расходы по категориям:")
        for category, total in sorted(
            stats.items(), key=lambda item: item[1], reverse=True
        ):
            print(f"  {category:<25}{total:>12.2f} руб.")


def check_budget_interactive() -> None:
    """Проверить возможность планируемой траты (сценарий ПР1)."""
    print("\n--- Проверка бюджета ---")
    monthly_budget = input_float("Месячный бюджет: ")
    current_expenses = input_float("Текущие расходы: ")
    planned_expense = input_float("Планируемая трата: ")

    remaining, after = calculate_budget(
        monthly_budget, current_expenses, planned_expense
    )
    status, warning = check_budget(planned_expense, remaining, after)

    report = format_report(
        monthly_budget, current_expenses, remaining,
        planned_expense, status, warning,
    )
    print(report)


# ---------- Меню ----------

MENU = """
===== Finance Planner =====
1. Показать операции
2. Добавить операцию
3. Найти операции по категории
4. Сортировать операции по сумме
5. Статистика по операциям
6. Показать цели
7. Показать цели по прогрессу
8. Показать суммарные накопления
9. Добавить цель
10. Пополнить цель
11. Достигнутые цели
12. Проверить бюджет (планирование)
0. Выход
"""


def main() -> None:
    """Запустить приложение: загрузить данные, показать меню, обработать."""
    transactions = load_transactions(TRANSACTIONS_FILE)
    goals = load_goals(GOALS_FILE)

    actions = {
        "1": lambda: show_transactions(transactions),
        "2": lambda: add_transaction_interactive(transactions),
        "3": lambda: find_transactions_interactive(transactions),
        "4": lambda: show_transactions(
            sort_transactions_by_amount(transactions)
        ),
        "5": lambda: show_statistics(transactions),
        "6": lambda: show_goals(goals),
        "7": lambda: show_goals_sorted(goals),
        "8": lambda: show_total_saved(goals),
        "9": lambda: add_goal_interactive(goals),
        "10": lambda: add_to_goal_interactive(goals),
        "11": lambda: show_achieved_goals(goals),
        "12": check_budget_interactive,
    }

    while True:
        print(MENU)
        choice = input_choice(
            "Выберите действие: ",
            list(actions.keys()) + ["0"],
        )
        if choice == "0":
            break
        actions[choice]()

    save_transactions(TRANSACTIONS_FILE, transactions)
    save_goals(GOALS_FILE, goals)
    print("Данные сохранены. До свидания!")


if __name__ == "__main__":
    main()
