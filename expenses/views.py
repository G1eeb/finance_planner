"""View-функции приложения expenses."""

import sqlite3

from django.shortcuts import render

DB_PATH = "data/finance_planner.sqlite"


def expenses(request):
    """Список расходов из БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    expenses_list = conn.execute("""
        SELECT e.id, e.amount, e.date,
               c.name AS category_name
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        ORDER BY e.date DESC
    """).fetchall()
    conn.close()

    return render(
        request,
        "expenses/expense_list.html",
        {"expenses": expenses_list},
    )


def expense_detail(request, expense_id):
    """Карточка расхода из БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    expense = conn.execute("""
        SELECT e.id, e.amount, e.date,
               c.name AS category_name
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.id = ?
    """, (expense_id,)).fetchone()
    conn.close()

    return render(
        request,
        "expenses/expense_detail.html",
        {"expense": expense},
        status=404 if expense is None else 200,
    )
