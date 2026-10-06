"""Точка входа консольного приложения Finance Planner."""

from models.incomes import (
    add_income,
    find_incomes_by_category,
    sort_incomes_by_amount,
    total_incomes,
)
from models.expenses import (
    add_expense,
    expenses_by_category,
    find_expenses_by_category,
    sort_expenses_by_amount,
    total_expenses,
)
from models.budgets import (
    add_budget,
    find_budget_by_id,
)
from storage import (
    load_budgets, save_budgets,
    load_expenses, save_expenses,
    load_incomes, save_incomes,
)
from utils import input_int, input_float, input_date, input_choice

INCOMES_FILE = "data/incomes.json"
EXPENSES_FILE = "data/expenses.json"
BUDGETS_FILE = "data/budgets.json"


# ---------- Вывод ----------

def show_incomes(incomes: list) -> None:
    """Вывести список доходов."""
    if not incomes:
        print("Доходов пока нет.")
        return
    print("-" * 60)
    for i in incomes:
        print(i)
    print("-" * 60)


def show_expenses(expenses: list) -> None:
    """Вывести список расходов."""
    if not expenses:
        print("Расходов пока нет.")
        return
    print("-" * 60)
    for e in expenses:
        print(e)
    print("-" * 60)


def show_budgets(budgets: list) -> None:
    """Вывести список бюджетов."""
    if not budgets:
        print("Бюджетов пока нет.")
        return
    print("-" * 60)
    for b in budgets:
        print(b)
    print("-" * 60)


# ---------- Интерактивные операции ----------

def add_income_interactive(incomes: list) -> None:
    """Добавить доход."""
    amount = input_float("Сумма дохода: ")
    category = input("Категория: ").strip()
    d = input_date("Дата (ДД.ММ.ГГГГ): ")
    try:
        i = add_income(incomes, amount, category, d.isoformat())
        print(f"Доход добавлен: id={i.id}")
    except ValueError as e:
        print(f"Ошибка: {e}")


def add_expense_interactive(expenses: list) -> None:
    """Добавить расход."""
    amount = input_float("Сумма расхода: ")
    category = input("Категория: ").strip()
    d = input_date("Дата (ДД.ММ.ГГГГ): ")
    try:
        e = add_expense(expenses, amount, category, d.isoformat())
        print(f"Расход добавлен: id={e.id}")
    except ValueError as err:
        print(f"Ошибка: {err}")


def add_budget_interactive(budgets: list) -> None:
    """Добавить бюджет."""
    month = input("Месяц (ГГГГ-ММ): ").strip()
    amount = input_float("Сумма бюджета: ")
    try:
        b = add_budget(budgets, month, amount)
        print(f"Бюджет добавлен: id={b.id}")
    except ValueError as e:
        print(f"Ошибка: {e}")


def find_incomes_interactive(incomes: list) -> None:
    """Найти доходы по категории."""
    query = input("Подстрока категории: ").strip()
    show_incomes(find_incomes_by_category(incomes, query))


def find_expenses_interactive(expenses: list) -> None:
    """Найти расходы по категории."""
    query = input("Подстрока категории: ").strip()
    show_expenses(find_expenses_by_category(expenses, query))


def show_statistics(incomes: list, expenses: list) -> None:
    """Показать статистику по доходам и расходам."""
    total_inc = total_incomes(incomes)
    total_exp = total_expenses(expenses)
    balance = total_inc - total_exp

    print("\n" + "=" * 50)
    print(f"Доходы:   {total_inc:>12.2f} руб.")
    print(f"Расходы:  {total_exp:>12.2f} руб.")
    if balance < 0:
        print(f"Баланс:   {balance:>12.2f} руб.  (превышение расходов)")
    else:
        print(f"Баланс:   {balance:>12.2f} руб.")
    print("=" * 50)

    stats = expenses_by_category(expenses)
    if stats:
        print("Расходы по категориям:")
        for category, total in sorted(
            stats.items(), key=lambda item: item[1], reverse=True
        ):
            print(f"  {category:<25}{total:>12.2f} руб.")


def check_budget_interactive(budgets: list) -> None:
    """Проверить бюджет: возможна ли планируемая трата."""
    if not budgets:
        print("Сначала добавьте бюджет.")
        return
    show_budgets(budgets)
    budget_id = input_int("ID бюджета: ")
    budget = find_budget_by_id(budgets, budget_id)
    if budget is None:
        print("Бюджет не найден.")
        return
    amount = input_float("Планируемая трата: ")
    if budget.can_afford(amount):
        remaining = budget.get_remaining_after(amount)
        print(f"Трата возможна. Остаток после: {remaining:.2f} руб.")
        if remaining < 5000:
            print("Внимание: останется менее 5000 руб.")
    else:
        overspend = amount - budget.get_remaining()
        print(f"Трата невозможна. Превышение на {overspend:.2f} руб.")


# ---------- Меню ----------

MENU = """
===== Finance Planner =====
1. Показать доходы
2. Добавить доход
3. Найти доходы по категории
4. Сортировать доходы по сумме
5. Показать расходы
6. Добавить расход
7. Найти расходы по категории
8. Сортировать расходы по сумме
9. Показать бюджеты
10. Добавить бюджет
11. Проверить бюджет
12. Статистика
0. Выход
"""


def main() -> None:
    """Запустить консольное приложение."""
    incomes = load_incomes(INCOMES_FILE)
    expenses = load_expenses(EXPENSES_FILE)
    budgets = load_budgets(BUDGETS_FILE)

    actions = {
        "1": lambda: show_incomes(incomes),
        "2": lambda: add_income_interactive(incomes),
        "3": lambda: find_incomes_interactive(incomes),
        "4": lambda: show_incomes(sort_incomes_by_amount(incomes)),
        "5": lambda: show_expenses(expenses),
        "6": lambda: add_expense_interactive(expenses),
        "7": lambda: find_expenses_interactive(expenses),
        "8": lambda: show_expenses(sort_expenses_by_amount(expenses)),
        "9": lambda: show_budgets(budgets),
        "10": lambda: add_budget_interactive(budgets),
        "11": lambda: check_budget_interactive(budgets),
        "12": lambda: show_statistics(incomes, expenses),
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

    save_incomes(INCOMES_FILE, incomes)
    save_expenses(EXPENSES_FILE, expenses)
    save_budgets(BUDGETS_FILE, budgets)
    print("Данные сохранены. До свидания!")


if __name__ == "__main__":
    main()
