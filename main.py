"""Точка входа приложения Finance Planner."""

from datetime import date

from budget import calculate_budget, check_budget, format_report


def main() -> None:
    """Запустить сценарий с использованием модуля budget."""
    user_name = "Алексей"
    monthly_budget = 60000.0
    current_expenses = 42500.0
    planned_expense = 15000.0
    expense_category = "Покупка техники"
    expense_date = date(2026, 9, 15)

    remaining_budget, budget_after_expense = calculate_budget(
        monthly_budget, current_expenses, planned_expense
    )
    status, warning = check_budget(
        planned_expense, remaining_budget, budget_after_expense
    )
    report = format_report(
        user_name, str(expense_date), expense_category,
        monthly_budget, current_expenses, remaining_budget,
        planned_expense, status, warning
    )
    print(report)


if __name__ == "__main__":
    main()
