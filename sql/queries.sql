-- ============================================
-- Finance Planner: SQL-запросы проекта
-- ============================================


-- --------------------------------------------
-- 1. Список всех доходов (SELECT)
-- --------------------------------------------
SELECT id, amount, category_id, date
FROM incomes
ORDER BY date DESC;


-- --------------------------------------------
-- 2. Список всех расходов (SELECT)
-- --------------------------------------------
SELECT id, amount, category_id, date
FROM expenses
ORDER BY date DESC;


-- --------------------------------------------
-- 3. Список всех бюджетов (SELECT)
-- --------------------------------------------
SELECT id, month, monthly_budget, current_expenses
FROM budgets
ORDER BY month DESC;


-- --------------------------------------------
-- 4. Доходы за период (WHERE + BETWEEN)
-- --------------------------------------------
SELECT id, amount, category_id, date
FROM incomes
WHERE date BETWEEN '2026-09-01' AND '2026-09-30'
ORDER BY date;


-- --------------------------------------------
-- 5. Расходы больше заданной суммы (WHERE)
-- --------------------------------------------
SELECT id, amount, category_id, date
FROM expenses
WHERE amount >= 10000
ORDER BY amount DESC;


-- --------------------------------------------
-- 6. Бюджеты с остатком больше 5000 (WHERE)
-- --------------------------------------------
SELECT id, month, monthly_budget, current_expenses,
       (monthly_budget - current_expenses) AS remaining
FROM budgets
WHERE (monthly_budget - current_expenses) > 5000
ORDER BY remaining DESC;


-- --------------------------------------------
-- 7. Доходы с названием категории (JOIN)
-- --------------------------------------------
SELECT i.id, i.amount, c.name AS category, i.date
FROM incomes i
JOIN categories c ON i.category_id = c.id
ORDER BY i.date DESC;


-- --------------------------------------------
-- 8. Расходы с названием категории (JOIN)
-- --------------------------------------------
SELECT e.id, e.amount, c.name AS category, e.date
FROM expenses e
JOIN categories c ON e.category_id = c.id
ORDER BY e.date DESC;


-- --------------------------------------------
-- 9. Общее количество доходов (COUNT)
-- --------------------------------------------
SELECT COUNT(*) AS incomes_count
FROM incomes;


-- --------------------------------------------
-- 10. Общая сумма расходов (SUM)
-- --------------------------------------------
SELECT SUM(amount) AS total_expenses
FROM expenses;


-- --------------------------------------------
-- 11. Средний размер дохода (AVG)
-- --------------------------------------------
SELECT AVG(amount) AS avg_income
FROM incomes;


-- --------------------------------------------
-- 12. Сумма расходов по категориям (GROUP BY)
-- --------------------------------------------
SELECT c.name AS category, SUM(e.amount) AS total
FROM expenses e
JOIN categories c ON e.category_id = c.id
GROUP BY c.id, c.name
ORDER BY total DESC;


-- --------------------------------------------
-- 13. Сумма доходов по категориям (GROUP BY)
-- --------------------------------------------
SELECT c.name AS category, SUM(i.amount) AS total
FROM incomes i
JOIN categories c ON i.category_id = c.id
GROUP BY c.id, c.name
ORDER BY total DESC;


-- --------------------------------------------
-- 14. Доходы по месяцам (GROUP BY)
-- --------------------------------------------
SELECT substr(date, 1, 7) AS month, SUM(amount) AS total
FROM incomes
GROUP BY month
ORDER BY month;


-- --------------------------------------------
-- 15. Категории с суммой расходов больше 5000 (HAVING)
-- --------------------------------------------
SELECT c.name AS category, SUM(e.amount) AS total
FROM expenses e
JOIN categories c ON e.category_id = c.id
GROUP BY c.id, c.name
HAVING SUM(e.amount) > 5000
ORDER BY total DESC;


-- --------------------------------------------
-- 16. Доходы за период (параметризованный — для Django)
-- --------------------------------------------
SELECT i.id, i.amount, c.name AS category, i.date
FROM incomes i
JOIN categories c ON i.category_id = c.id
WHERE i.date BETWEEN ? AND ?
ORDER BY i.date;
