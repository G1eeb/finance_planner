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


def expense_filter(request):
    """Поиск расходов по диапазону дат (параметризованный SQL)."""
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    expenses_list = []
    if date_from and date_to:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        expenses_list = conn.execute("""
            SELECT e.id, e.amount, e.date,
                   c.name AS category_name
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.date BETWEEN ? AND ?
            ORDER BY e.date DESC
        """, (date_from, date_to)).fetchall()
        conn.close()

    return render(
        request,
        "expenses/expense_filter.html",
        {
            "expenses": expenses_list,
            "date_from": date_from,
            "date_to": date_to,
        },
    )


def expense_statistics(request):
    """Статистика расходов по категориям (GROUP BY + HAVING)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    stats = conn.execute("""
        SELECT c.name AS category_name,
               SUM(e.amount) AS total,
               COUNT(e.id) AS count
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        GROUP BY c.id, c.name
        ORDER BY total DESC
    """).fetchall()
    conn.close()

    return render(
        request,
        "expenses/expense_statistics.html",
        {"stats": stats},
    )
