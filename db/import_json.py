"""Перенос данных из JSON-файлов в SQLite."""

import json

from db.database import get_connection

INCOMES_FILE = "data/incomes.json"
EXPENSES_FILE = "data/expenses.json"
BUDGETS_FILE = "data/budgets.json"


def load_json(filename):
    """Прочитать JSON-файл и вернуть данные."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def collect_categories(incomes, expenses):
    """Собрать уникальные названия категорий из доходов и расходов."""
    names = set()
    for item in incomes:
        names.add(item["category"])
    for item in expenses:
        names.add(item["category"])
    return sorted(names)


def import_categories(conn, category_names):
    """Вставить категории. Вернуть словарь имя → id."""
    conn.executemany(
        "INSERT INTO categories (name) VALUES (?)",
        [(name,) for name in category_names],
    )
    rows = conn.execute("SELECT id, name FROM categories").fetchall()
    return {row["name"]: row["id"] for row in rows}


def import_incomes(conn, incomes, category_map):
    """Вставить доходы, подставив category_id по имени."""
    conn.executemany(
        """
        INSERT INTO incomes (id, amount, category_id, date)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["amount"],
                category_map[item["category"]],
                item["date"],
            )
            for item in incomes
        ],
    )


def import_expenses(conn, expenses, category_map):
    """Вставить расходы, подставив category_id по имени."""
    conn.executemany(
        """
        INSERT INTO expenses (id, amount, category_id, date)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["amount"],
                category_map[item["category"]],
                item["date"],
            )
            for item in expenses
        ],
    )


def import_budgets(conn, budgets):
    """Вставить бюджеты."""
    conn.executemany(
        """
        INSERT INTO budgets
            (id, month, monthly_budget, current_expenses)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["month"],
                item["monthly_budget"],
                item.get("current_expenses", 0.0),
            )
            for item in budgets
        ],
    )


def main():
    """Загрузить JSON и перенести данные в SQLite."""
    incomes = load_json(INCOMES_FILE)
    expenses = load_json(EXPENSES_FILE)
    budgets = load_json(BUDGETS_FILE)

    category_names = collect_categories(incomes, expenses)

    conn = get_connection()
    conn.row_factory = __import__("sqlite3").Row
    try:
        category_map = import_categories(conn, category_names)
        import_incomes(conn, incomes, category_map)
        import_expenses(conn, expenses, category_map)
        import_budgets(conn, budgets)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
