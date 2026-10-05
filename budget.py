"""Модуль расчёта и проверки месячного бюджета."""


def calculate_budget(monthly_budget: float, current_expenses: float,
                     planned_expense: float) -> tuple[float, float]:
    """Рассчитать остаток бюджета и сумму после планируемой траты."""
    remaining_budget = monthly_budget - current_expenses
    budget_after_expense = remaining_budget - planned_expense
    return remaining_budget, budget_after_expense


def check_budget(planned_expense: float, remaining_budget: float,
                 budget_after_expense: float) -> tuple[str, str]:
    """Проверить, возможна ли трата. Вернуть статус и предупреждение."""
    if planned_expense <= remaining_budget:
        status = "Трата возможна: бюджет позволяет."
        if budget_after_expense < 5000:
            warning = "Внимание: после покупки останется менее 5000 руб."
        else:
            warning = "После покупки останется достаточно средств."
    else:
        overspend = planned_expense - remaining_budget
        status = f"Трата невозможна: превышение бюджета на {overspend:.2f} руб."
        warning = "Рекомендуется отложить покупку или пересмотреть бюджет."
    return status, warning


def format_report(user_name: str, expense_date: str, expense_category: str,
                  monthly_budget: float, current_expenses: float,
                  remaining_budget: float, planned_expense: float,
                  status: str, warning: str) -> str:
    """Сформировать текст отчёта о бюджете."""
    lines = [
        "=" * 50,
        f"Пользователь: {user_name}",
        f"Дата операции: {expense_date}",
        f"Категория: {expense_category}",
        "-" * 50,
        f"Месячный бюджет:      {monthly_budget:>10.2f} руб.",
        f"Текущие расходы:      {current_expenses:>10.2f} руб.",
        f"Остаток бюджета:      {remaining_budget:>10.2f} руб.",
        f"Планируемая трата:    {planned_expense:>10.2f} руб.",
        "-" * 50,
        f"Статус: {status}",
        f"Примечание: {warning}",
        "=" * 50,
    ]
    return "\n".join(lines)
