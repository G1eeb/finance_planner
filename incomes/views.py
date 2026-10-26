"""View-функции приложения incomes."""

import sqlite3

from django.shortcuts import render

DB_PATH = "data/finance_planner.sqlite"


def incomes(request):
    """Список доходов из БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    incomes_list = conn.execute("""
        SELECT i.id, i.amount, i.date,
               c.name AS category_name
        FROM incomes i
        JOIN categories c ON i.category_id = c.id
        ORDER BY i.date DESC
    """).fetchall()
    conn.close()

    return render(
        request,
        "incomes/income_list.html",
        {"incomes": incomes_list},
    )


def income_detail(request, income_id):
    """Карточка дохода из БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    income = conn.execute("""
        SELECT i.id, i.amount, i.date,
               c.name AS category_name
        FROM incomes i
        JOIN categories c ON i.category_id = c.id
        WHERE i.id = ?
    """, (income_id,)).fetchone()
    conn.close()

    return render(
        request,
        "incomes/income_detail.html",
        {"income": income},
        status=404 if income is None else 200,
    )
