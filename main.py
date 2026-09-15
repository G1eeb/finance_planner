from datetime import date

# --- Входные данные (простые типы) ---
user_name = "Алексей"
monthly_budget = 60000.0          # месячный бюджет, руб.
current_expenses = 42500.0        # уже потрачено за месяц, руб.
planned_expense = 15000.0         # планируемая трата, руб.
expense_category = "Покупка техники"
expense_date = date(2026, 9, 15)

# --- Расчёты ---
remaining_budget = monthly_budget - current_expenses
budget_after_expense = remaining_budget - planned_expense

# --- Логика проверки (ветвления) ---
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

# --- Вывод результата ---
print("=" * 50)
print(f"Пользователь: {user_name}")
print(f"Дата операции: {expense_date}")
print(f"Категория: {expense_category}")
print("-" * 50)
print(f"Месячный бюджет:      {monthly_budget:>10.2f} руб.")
print(f"Текущие расходы:      {current_expenses:>10.2f} руб.")
print(f"Остаток бюджета:      {remaining_budget:>10.2f} руб.")
print(f"Планируемая трата:    {planned_expense:>10.2f} руб.")
print("-" * 50)
print(f"Статус: {status}")
print(f"Примечание: {warning}")
print("=" * 50)